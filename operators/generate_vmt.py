import bpy
import os
from bpy.types import Operator

def format_float(f):
    """Округление до трёх знаков после точки"""
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
        out_dir = os.path.join(blend_dir, vmt_path)
        os.makedirs(out_dir, exist_ok=True)

        generated_materials = []

        for mat in bpy.data.materials:
            if not mat.use_nodes:
                continue

            nt = mat.node_tree
            shader_node = None
            for n in nt.nodes:
                if n.type in {'BSDF_PRINCIPLED', 'EMISSION', 'BSDF_DIFFUSE', 'BSDF_GLASS'}:
                    shader_node = n
                    break
            if not shader_node:
                continue

            shader_type = "VertexlitGeneric"
            if shader_node.type == 'EMISSION':
                shader_type = "UnlitGeneric"

            vmt_lines = [f'"{shader_type}"', '{']

            # ---------- Base Color ----------
            base_color_input = shader_node.inputs.get("Base Color")
            base_tex = "white"
            if base_color_input and base_color_input.is_linked:
                from_node = base_color_input.links[0].from_node
                if from_node.type == "TEX_IMAGE" and from_node.image:
                    base_tex = os.path.splitext(os.path.basename(from_node.image.filepath))[0]

            if base_tex != "white":
                vmt_lines.append(f'\t"$basetexture" "{vmt_path}\\{base_tex}"')
            else:
                vmt_lines.append(f'\t"$basetexture" "white"')
                if base_color_input:
                    val = base_color_input.default_value[:3]
                    vmt_lines.append(f'\t"$color2" "[ {format_float(val[0])} {format_float(val[1])} {format_float(val[2])} ]"')

            # ---------- Normal ----------
            bumpmap = None
            normal_input = shader_node.inputs.get("Normal")
            if normal_input and normal_input.is_linked:
                normal_node = normal_input.links[0].from_node
                if normal_node.type == "NORMAL_MAP":
                    color_input = normal_node.inputs.get("Color")
                    if color_input and color_input.is_linked:
                        tex_node = color_input.links[0].from_node
                        if tex_node.type == "TEX_IMAGE" and tex_node.image:
                            bumpmap = os.path.splitext(os.path.basename(tex_node.image.filepath))[0]
            if bumpmap:
                vmt_lines.append(f'\t"$bumpmap" "{vmt_path}\\{bumpmap}"')

            # ---------- Roughness ----------
            rough_input = shader_node.inputs.get("Roughness")
            phongtex = None
            if rough_input and rough_input.is_linked:
                vmt_lines.append("\n\t// Phong")
                rough_node = rough_input.links[0].from_node
                if rough_node.type == "TEX_IMAGE" and rough_node.image:
                    phongtex = os.path.splitext(os.path.basename(rough_node.image.filepath))[0]
            if phongtex:
                vmt_lines.append(f'\t"$phong" "1"')
                vmt_lines.append(f'\t"$phongexponenttexture" "{vmt_path}\\{phongtex}"')
                vmt_lines.append(f'\t"$phongboost" "2"')
                vmt_lines.append(f'\t"$phongfresnelranges" "[0.05 0.5 1.0]"')

            # ---------- Emission ----------
            if shader_node.type == 'BSDF_PRINCIPLED':
                vmt_lines.append("\n\t// Emission")
                em_color_input = shader_node.inputs.get("Emission Color")
                em_strength_input = shader_node.inputs.get("Emission Strength")
                em_strength = em_strength_input.default_value if em_strength_input else 0
                if em_strength > 0:
                    em_tex = "white"
                    if em_color_input and em_color_input.is_linked:
                        from_node = em_color_input.links[0].from_node
                        if from_node.type == "TEX_IMAGE" and from_node.image:
                            em_tex = os.path.splitext(os.path.basename(from_node.image.filepath))[0]

                    vmt_lines.append('\t"$EmissiveBlendEnabled" "1"')
                    if em_tex != "white":
                        vmt_lines.append(f'\t"$EmissiveBlendBaseTexture" "{vmt_path}\\{em_tex}"')
                    else:
                        vmt_lines.append('\t"$EmissiveBlendBaseTexture" "white"')
                    vmt_lines.append(f'\t"$EmissiveBlendStrength" "{format_float(em_strength)}"')
                    vmt_lines.append('\t"$EmissiveBlendTexture" "white"')
            elif shader_node.type == 'EMISSION':
                col_input = shader_node.inputs.get("Color")
                tex_name = "white"
                if col_input and col_input.is_linked:
                    from_node = col_input.links[0].from_node
                    if from_node.type == "TEX_IMAGE" and from_node.image:
                        tex_name = os.path.splitext(os.path.basename(from_node.image.filepath))[0]

                if tex_name != "white":
                    vmt_lines.append(f'\t"$basetexture" "{vmt_path}\\{tex_name}"')
                else:
                    vmt_lines.append(f'\t"$basetexture" "white"')
                    val = col_input.default_value[:3]
                    vmt_lines.append(f'\t"$color2" "[ {format_float(val[0])} {format_float(val[1])} {format_float(val[2])} ]"')

            # ---------- Glass ----------
            if shader_node.type == 'BSDF_PRINCIPLED':
                trans_weight_input = shader_node.inputs.get("Transmission Weight")
                metallic_input = shader_node.inputs.get("Metallic")
                metallic_val = metallic_input.default_value if metallic_input else 0
                transmission_val = trans_weight_input.default_value if trans_weight_input else 0

                # Стекло только если Transmission Weight > 0 и Metallic == 0
                if transmission_val > 0.0001 and metallic_val <= 0.0001:
                    vmt_lines.append("\n\t// Glass")
                    vmt_lines.append('\t"$additive" "1"')
                    vmt_lines.append('\t"$envmap" "env_cubemap"')
                    col_input = shader_node.inputs.get("Base Color")
                    tex_linked = col_input.is_linked if col_input else False
                    if tex_linked:
                        vmt_lines.append('\t"$envmaptint" "[ 0.5 0.5 0.5 ]"')
                    elif col_input:
                        val = col_input.default_value[:3]
                        vmt_lines.append(f'\t"$envmaptint" "[ {format_float(val[0])} {format_float(val[1])} {format_float(val[2])} ]"')

            # ---------- Metallic ----------
            if metallic_val > 0:
                vmt_lines.append("\n\t// Metallic")
                mval = metallic_val / 2
                vmt_lines.append('\t"$envmap" "env_cubemap"')
                col_input = shader_node.inputs.get("Base Color")
                tex_linked = col_input.is_linked if col_input else False
                if tex_linked:
                    vmt_lines.append('\t"$envmaptint" "[ 0.01 0.01 0.01 ]"')
                elif col_input:
                    val = col_input.default_value[:3]
                    vmt_lines.append(f'\t"$envmaptint" "[ {format_float(val[0])} {format_float(val[1])} {format_float(val[2])} ]"')
                vmt_lines.append('\t"$normalmapalphaenvmapmask" "1"')
                
            vmt_lines.append('}\n')
            file_path = os.path.join(out_dir, f"{mat.name}.vmt")
            with open(file_path, "w") as f:
                f.write("\n".join(vmt_lines))

            generated_materials.append(mat.name)

        # Выводим сообщение о сгенерированных материалах
        if generated_materials:
            show_generated_vmt_popup(generated_materials)

        return {'FINISHED'}
