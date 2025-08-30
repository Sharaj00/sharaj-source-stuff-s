import bpy
import os
import subprocess
import threading
from bpy.types import Operator
from bpy.props import BoolProperty
from PIL import Image
from queue import Queue

def run_vtfcmd(input_path, output_dir, fmt, flags=None, errors=None):
    try:
        addon_dir = os.path.dirname(os.path.dirname(__file__))
        vtfcmd_path = os.path.join(addon_dir, "operators", "VTFCmd.exe")

        input_abs = os.path.abspath(input_path)
        output_abs = os.path.abspath(output_dir)
        os.makedirs(output_abs, exist_ok=True)

        args = [f'"{vtfcmd_path}"', "-file", f'"{input_abs}"', "-output", f'"{output_abs}"', "-format", fmt]
        if flags:
            for f in flags:
                args.extend(["-flag", f])

        subprocess.run(" ".join(args), check=True, shell=True, cwd=os.path.dirname(vtfcmd_path))
    except subprocess.CalledProcessError as e:
        if errors is not None:
            errors.append(f"Failed {os.path.basename(input_path)}: {e}")

def resize_texture(image_path, max_height):
    img = Image.open(image_path)
    if img.height > max_height:
        scale = max_height / img.height
        new_size = (int(img.width * scale), max_height)
        img = img.resize(new_size, Image.LANCZOS)
        img.save(image_path)

def combine_normal_roughness(normal_path, rough_path, out_path):
    normal = Image.open(normal_path).convert("RGBA")
    rough = Image.open(rough_path).convert("L").resize(normal.size, Image.LANCZOS)
    r, g, b, _ = normal.split()
    combined = Image.merge("RGBA", (r, g, b, rough))
    combined.save(out_path)

class ConvertMaterialsOperator(Operator):
    bl_idname = "wm.convert_materials_to_vtf"
    bl_label = "Convert Materials to VTF"

    cancel: BoolProperty(default=False)

    _thread = None
    _queue = None

    def execute(self, context):
        wm = context.window_manager
        wm.conversion_running = True
        wm.conversion_progress = 0
        wm.conversion_log = ""
        wm.current_texture = ""
        self.cancel = False

        blend_dir = bpy.path.abspath(wm.output_path)
        vmt_path = wm.vmt_path
        out_dir = os.path.join(blend_dir, vmt_path)
        os.makedirs(out_dir, exist_ok=True)

        max_height = int(wm.texture_max_height)
        tasks = []

        # Собираем задачи по материалам
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            nt = mat.node_tree
            bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
            if not bsdf:
                continue

            # Base Color
            if bsdf.inputs["Base Color"].is_linked:
                tex_node = bsdf.inputs["Base Color"].links[0].from_node
                if tex_node.type == "TEX_IMAGE" and tex_node.image:
                    tasks.append(('Base Color', tex_node.image))

            # Normal + Roughness
            if bsdf.inputs["Normal"].is_linked:
                normal_node = bsdf.inputs["Normal"].links[0].from_node
                if normal_node.type == "NORMAL_MAP" and normal_node.inputs["Color"].is_linked:
                    tex_node = normal_node.inputs["Color"].links[0].from_node
                    if tex_node.type == "TEX_IMAGE" and tex_node.image:
                        tasks.append(('Normal', tex_node.image, bsdf))

            # Emission
            if bsdf.inputs["Emission Color"].is_linked:
                tex_node = bsdf.inputs["Emission Color"].links[0].from_node
                if tex_node.type == "TEX_IMAGE" and tex_node.image:
                    tasks.append(('Emission', tex_node.image, bsdf))

        self._queue = Queue()
        errors = []

        def worker():
            total = len(tasks)
            for idx, task in enumerate(tasks, 1):
                if self.cancel:
                    self._queue.put((wm.conversion_progress, "Conversion canceled", ""))
                    break
                try:
                    img = task[1]
                    img_name = os.path.basename(bpy.path.abspath(img.filepath))
                    wm.current_texture = f"{idx}/{total}: {img_name}"
                    self._queue.put((int(idx/total*100), f"Processing {img_name}", wm.current_texture))

                    # Base Color
                    if task[0] == 'Base Color':
                        img_path = bpy.path.abspath(img.filepath)
                        resize_texture(img_path, max_height)
                        fmt = "DXT5" if img.has_data and img.depth == 32 else "DXT1"
                        run_vtfcmd(img_path, out_dir, fmt, errors=errors)

                    # Normal + Roughness
                    elif task[0] == 'Normal':
                        bsdf = task[2]
                        normal_path = bpy.path.abspath(img.filepath)
                        resize_texture(normal_path, max_height)
                        fmt = "DXT5" if img.has_data and img.depth == 32 else "DXT1"

                        # Roughness в альфу
                        if bsdf.inputs["Roughness"].is_linked:
                            rough_node = bsdf.inputs["Roughness"].links[0].from_node
                            if rough_node.type == "TEX_IMAGE" and rough_node.image:
                                rough_path = bpy.path.abspath(rough_node.image.filepath)
                                resize_texture(rough_path, max_height)
                                combine_normal_roughness(normal_path, rough_path, normal_path)
                                run_vtfcmd(rough_path, out_dir, "DXT1", errors=errors)

                        run_vtfcmd(normal_path, out_dir, fmt, flags=["Normal"], errors=errors)

                    # Emission
                    elif task[0] == 'Emission':
                        bsdf = task[2]
                        img_path = bpy.path.abspath(img.filepath)
                        resize_texture(img_path, max_height)
                        run_vtfcmd(img_path, out_dir, "DXT1", errors=errors)

                except Exception as e:
                    errors.append(f"Unexpected error: {e}")

            self._queue.put((100, "Conversion finished", ""))
            if errors:
                self._queue.put((100, "ERRORS: " + "; ".join(errors), ""))

        self._thread = threading.Thread(target=worker, daemon=True)
        self._thread.start()
        bpy.app.timers.register(self._modal_update)
        return {'RUNNING_MODAL'}

    def _modal_update(self):
        wm = bpy.context.window_manager
        updated = False
        while not self._queue.empty():
            progress, log, current_texture = self._queue.get()
            wm.conversion_progress = progress
            wm.conversion_log = log
            wm.current_texture = current_texture
            updated = True
        if updated:
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        if self._thread.is_alive():
            return 0.1
        else:
            wm.conversion_running = False
            wm.current_texture = ""
            return None
