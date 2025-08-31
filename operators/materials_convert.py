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

def invert_grayscale(image_path, save_path=None):
    img = Image.open(image_path).convert("L")
    inverted = Image.eval(img, lambda px: 255 - px)
    if save_path:
        inverted.save(save_path)
    return inverted

def combine_normal_roughness(normal_path, rough_path, out_path):
    normal = Image.open(normal_path).convert("RGBA")
    gloss = invert_grayscale(rough_path)
    gloss = gloss.resize(normal.size, Image.LANCZOS)

    r, g, b, _ = normal.split()
    combined = Image.merge("RGBA", (r, g, b, gloss))
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
        rel_output_dir = os.path.join(blend_dir, "materials", vmt_path)
        os.makedirs(rel_output_dir, exist_ok=True)

        max_height = int(wm.texture_max_height)
        tasks = []

        # Собираем задачи
        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue
            nt = mat.node_tree
            shader_node = next((n for n in nt.nodes if n.type in {'BSDF_PRINCIPLED', 'EMISSION'}), None)
            if not shader_node:
                continue

            # Base Color
            base_input = shader_node.inputs.get("Base Color")
            if base_input and base_input.is_linked:
                tex_node = base_input.links[0].from_node
                if tex_node.type == "TEX_IMAGE" and tex_node.image:
                    tasks.append(('Base Color', tex_node.image))

            # Normal + Roughness
            normal_input = shader_node.inputs.get("Normal")
            if normal_input and normal_input.is_linked:
                normal_node = normal_input.links[0].from_node
                if normal_node.type == "NORMAL_MAP" and normal_node.inputs.get("Color") and normal_node.inputs["Color"].is_linked:
                    tex_node = normal_node.inputs["Color"].links[0].from_node
                    if tex_node.type == "TEX_IMAGE" and tex_node.image:
                        tasks.append(('Normal', tex_node.image, shader_node))

            # Roughness
            rough_input = shader_node.inputs.get("Roughness")
            if rough_input and rough_input.is_linked:
                rough_node = rough_input.links[0].from_node
                if rough_node.type == "TEX_IMAGE" and rough_node.image:
                    tasks.append(('Roughness', rough_node.image, shader_node))

            # Emission
            em_input = shader_node.inputs.get("Emission Color")
            if em_input and em_input.is_linked:
                tex_node = em_input.links[0].from_node
                if tex_node.type == "TEX_IMAGE" and tex_node.image:
                    tasks.append(('Emission', tex_node.image, shader_node))

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
                    img_path = bpy.path.abspath(img.filepath)
                    wm.current_texture = f"{idx}/{total}: {os.path.basename(img_path)}"
                    self._queue.put((int(idx/total*100), f"Processing {os.path.basename(img_path)}", wm.current_texture))
                    resize_texture(img_path, max_height)

                    # Base Color
                    if task[0] == 'Base Color':
                        fmt = "DXT5" if img.has_data and img.depth == 32 else "DXT1"
                        run_vtfcmd(img_path, rel_output_dir, fmt, errors=errors)

                    # Normal + Roughness
                    elif task[0] == 'Normal':
                        bsdf = task[2]
                        normal_path = img_path
                        fmt = "DXT5" if img.has_data and img.depth == 32 else "DXT1"

                        rough_input = bsdf.inputs.get("Roughness")
                        if rough_input and rough_input.is_linked:
                            rough_node = rough_input.links[0].from_node
                            if rough_node.type == "TEX_IMAGE" and rough_node.image:
                                rough_path = bpy.path.abspath(rough_node.image.filepath)
                                resize_texture(rough_path, max_height)
                                combine_normal_roughness(normal_path, rough_path, normal_path)
                                run_vtfcmd(rough_path, rel_output_dir, "DXT1", errors=errors)

                        run_vtfcmd(normal_path, rel_output_dir, fmt, flags=["Normal"], errors=errors)

                    # Roughness
                    elif task[0] == 'Roughness':
                        rough_path = img_path
                        temp_phong_png = os.path.join(rel_output_dir, os.path.basename(rough_path))
                        invert_grayscale(rough_path, temp_phong_png)
                        run_vtfcmd(temp_phong_png, rel_output_dir, "DXT1", errors=errors)
                        if os.path.exists(temp_phong_png):
                            os.remove(temp_phong_png)

                    # Emission
                    elif task[0] == 'Emission':
                        fmt = "DXT1"
                        run_vtfcmd(img_path, rel_output_dir, fmt, errors=errors)

                except Exception as e:
                    errors.append(f"Unexpected error: {e}")

            self._queue.put((100, "Conversion finished", ""))
            if errors:
                print("Errors during conversion:")
                for err in errors:
                    print(err)
                self._queue.put((100, "Conversion finished with errors. See console for details.", ""))

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

# Функция для внешнего вызова отмены
def cancel_conversion():
    for w in bpy.context.window_manager.operators:
        if isinstance(w, ConvertMaterialsOperator):
            w.cancel = True
