import bpy
import os
from bpy.types import Operator

def format_float(f):
    return f"{f:.3f}".rstrip('0').rstrip('.') if '.' in f"{f:.3f}" else f"{f:.3f}"

def show_generated_vmt_popup(materials):
    def draw(self, context):
        for mat in materials:
            self.layout.label(text=mat)
    bpy.context.window_manager.popup_menu(draw, title="Generated VMTs", icon='MATERIAL')

class WM_OT_generate_vmt(Operator):
    bl_idname = "wm.generate_vmt"
    bl_label = "Generate VMT"

    def execute(self, context):
        wm = context.window_manager
        vmt_path = wm.vmt_path
        blend_dir = bpy.path.abspath(wm.output_path)
        out_dir = os.path.join(blend_dir, "materials", vmt_path)
        os.makedirs(out_dir, exist_ok=True)

        generated_materials = []

        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue

            # Определяем активный шейдер
            shader_node = None
            for n in mat.node_tree.nodes:
                if n.type in {'BSDF_PRINCIPLED', 'EMISSION', 'BSDF_DIFFUSE', 'BSDF_GLASS'}:
                    shader_node = n
                    break
            if not shader_node:
                continue

            vmt_lines = []
            if shader_node.type == 'EMISSION':
                vmt_lines.append('"UnlitGeneric"')
            else:
                vmt_lines.append('"VertexlitGeneric"')
            vmt_lines.append('{')

            # ------------------- PRINCIPLED -------------------
            if shader_node.type == 'BSDF_PRINCIPLED':
                # Base Color
                base_color_input = shader_node.inputs.get("Base Color")
                base_tex = "white"
                color_val = None
                if base_color_input:
                    if base_color_input.is_linked:
                        from_node = base_color_input.links[0].from_node
                        if from_node.type == "TEX_IMAGE" and from_node.image:
                            base_tex = os.path.splitext(os.path.basename(from_node.image.filepath))[0]
                    else:
                        color_val = base_color_input.default_value[:3]
                        
                if base_tex != "white":
                    vmt_lines.append(f'\t"$basetexture" "{vmt_path}\\{base_tex}"')
                else:
                    vmt_lines.append(f'\t"$basetexture" "white"')
                    if color_val:
                        vmt_lines.append(f'\t"$color2" "[ {format_float(color_val[0])} {format_float(color_val[1])} {format_float(color_val[2])} ]"')

                # Normal Map
                normal_input = shader_node.inputs.get("Normal")
                if normal_input and normal_input.is_linked:
                    normal_node = normal_input.links[0].from_node
                    if normal_node.type == "NORMAL_MAP":
                        color_input = normal_node.inputs.get("Color")
                        if color_input and color_input.is_linked:
                            tex_node = color_input.links[0].from_node
                            if tex_node.type == "TEX_IMAGE" and tex_node.image:
                                bumpmap = os.path.splitext(os.path.basename(tex_node.image.filepath))[0]
                                vmt_lines.append(f'\t"$bumpmap" "{vmt_path}\\{bumpmap}"')

                # Roughness / Phong
                rough_input = shader_node.inputs.get("Roughness")
                rough_val = rough_input.default_value if rough_input else None
                phongtex = None
                if rough_input and rough_input.is_linked:
                    rough_node = rough_input.links[0].from_node
                    if rough_node.type == "TEX_IMAGE" and rough_node.image:
                        phongtex = os.path.splitext(os.path.basename(rough_node.image.filepath))[0]

                if phongtex or (rough_input and not rough_input.is_linked and rough_val < 0.5):
                    vmt_lines.append(f'\t"$phong" "1"')
                    if phongtex:
                        vmt_lines.append(f'\t"$phongexponenttexture" "{vmt_path}\\{phongtex}"')
                    else:
                        vmt_lines.append(f'\t"$phongexponent" "32"')
                    vmt_lines.append('\t"$phongboost" "2"')
                    vmt_lines.append('\t"$phongfresnelranges" "[0.05 0.5 1.0]"')

                # Emission
                em_color_input = shader_node.inputs.get("Emission Color")
                em_strength_input = shader_node.inputs.get("Emission Strength")
                em_strength = em_strength_input.default_value if em_strength_input else 0
                em_tex = "white"
                if em_color_input and em_color_input.is_linked:
                    from_node = em_color_input.links[0].from_node
                    if from_node.type == "TEX_IMAGE" and from_node.image:
                        em_tex = os.path.splitext(os.path.basename(from_node.image.filepath))[0]
                if em_strength > 0:
                    em_texture_path = f'{vmt_path}\\{em_tex}' if em_tex != "white" else "white"
                    vmt_lines.append(f'\t"$EmissiveBlendEnabled" "1"')
                    vmt_lines.append(f'\t"$EmissiveBlendBaseTexture" "{em_texture_path}"')
                    vmt_lines.append(f'\t"$EmissiveBlendStrength" "{format_float(em_strength)}"')
                    vmt_lines.append('\t"$EmissiveBlendTexture" "white"')

                # Glass / Metallic
                trans_weight_input = shader_node.inputs.get("Transmission Weight")
                transmission_val = trans_weight_input.default_value if trans_weight_input else 0
                metallic_input = shader_node.inputs.get("Metallic")
                metallic_val = metallic_input.default_value if metallic_input else 0

                if transmission_val > 0 and metallic_val <= 0:
                    vmt_lines.append('\t"$additive" "1"')
                    vmt_lines.append('\t"$envmap" "env_cubemap"')
                    col_input = shader_node.inputs.get("Base Color")
                    if col_input and col_input.is_linked:
                        vmt_lines.append('\t"$envmaptint" "[0.5 0.5 0.5]"')
                    elif col_input:
                        val = col_input.default_value[:3]
                        vmt_lines.append(f'\t"$envmaptint" "[ {format_float(val[0])} {format_float(val[1])} {format_float(val[2])} ]"')
                elif metallic_val > 0:
                    vmt_lines.append('\t"$envmap" "env_cubemap"')
                    col_input = shader_node.inputs.get("Base Color")
                    if col_input and col_input.is_linked:
                        vmt_lines.append('\t"$envmaptint" "[0.01 0.01 0.01]"')
                    elif col_input:
                        val = col_input.default_value[:3]
                        vmt_lines.append(f'\t"$envmaptint" "[ {format_float(val[0])} {format_float(val[1])} {format_float(val[2])} ]"')
                    vmt_lines.append('\t"$normalmapalphaenvmapmask" "1"')

            # ------------------- GLASS BSDF -------------------
            elif shader_node.type == 'BSDF_GLASS':
                col_input = shader_node.inputs.get("Color")
                color_val_glass = (1.0, 1.0, 1.0)
                if col_input:
                    color_val_glass = col_input.default_value[:3]

                vmt_lines.append(f'\t"$basetexture" "white"')
                vmt_lines.append(f'\t"$color2" "[ {format_float(color_val_glass[0])} {format_float(color_val_glass[1])} {format_float(color_val_glass[2])} ]"')
                vmt_lines.append('\t"$additive" "1"')
                vmt_lines.append('\t"$envmap" "env_cubemap"')
                vmt_lines.append(f'\t"$envmaptint" "[ {format_float(color_val_glass[0])} {format_float(color_val_glass[1])} {format_float(color_val_glass[2])} ]"')

            # ------------------- EMISSION NODE -------------------
            elif shader_node.type == 'EMISSION':
                col_input = shader_node.inputs.get("Color")
                tex_name = "white"
                color_val_em = None
                if col_input:
                    if col_input.is_linked:
                        from_node = col_input.links[0].from_node
                        if from_node.type == "TEX_IMAGE" and from_node.image:
                            tex_name = os.path.splitext(os.path.basename(from_node.image.filepath))[0]
                    else:
                        color_val_em = col_input.default_value[:3]

                # Генерация параметров
                if tex_name != "white":
                    vmt_lines.append(f'\t"$basetexture" "{vmt_path}\\{tex_name}"')
                else:
                    vmt_lines.append(f'\t"$basetexture" "white"')
                    if color_val_em:
                        vmt_lines.append(f'\t"$color2" "[ {format_float(color_val_em[0])} {format_float(color_val_em[1])} {format_float(color_val_em[2])} ]"')

            vmt_lines.append('}\n')

            file_path = os.path.join(out_dir, f"{mat.name}.vmt")
            with open(file_path, "w") as f:
                f.write("\n".join(vmt_lines))

            generated_materials.append(mat.name)

        if generated_materials:
            show_generated_vmt_popup(generated_materials)

        return {'FINISHED'}
