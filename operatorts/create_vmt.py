import bpy
import os

class WM_OT_create_vmt(bpy.types.Operator):
    bl_label = "VMT generation"
    bl_idname = "wm.create_vmt"
    bl_description = "Generate VMT files for each material in the blend file (Principled BSDF only)"
    
    def create_vmt(self, material_name, base_texture, bump_map, output_dir, relative_path, lightwarp, halflambert=False, nocull=False, use_bump=False, use_alpha=False, color=None, is_metallic=False):
        relative_path = relative_path.replace("materials/", "")
        
        vmt_content = f'''"VertexlitGeneric"
{{
    "$basetexture" "{base_texture}"'''
        if use_bump:
            vmt_content += f'''
    "$bumpmap" "{relative_path}/{bump_map}"'''
        if lightwarp:
            vmt_content += f'''
    "$lightwarptexture" "{relative_path}/{lightwarp}"'''
        if color:
            vmt_content += f'''
    "$color2" "{{{color[0]} {color[1]} {color[2]}}}"'''
        if use_alpha:
            vmt_content += '''
    "$translucent" "1"'''
        if halflambert:
            vmt_content += '''
    "$halflambert" "1"'''
        if nocull:
            vmt_content += '''
    "$nocull" "1"'''
        
        # Добавляем дополнительные параметры, если Roughness == 0
        if is_metallic:
            vmt_content += '''
    "$additive" "1"
    "$envmap" "env_cubemap"
    "$envmaptint" "[0.50 0.50 0.50]"
    "$phong" "1"
    "$phongfresnelranges" "[0.5 0.75 1]"
    "$halflambert" "1"
    "$phongexponent" "5"'''
        
        vmt_content += '''
}'''
        
        vmt_filename = os.path.join(output_dir, f"{material_name}.vmt")
        with open(vmt_filename, 'w') as file:
            file.write(vmt_content)
        return vmt_filename

    def execute(self, context):
        blend_filepath = bpy.data.filepath
        blend_dir = os.path.dirname(blend_filepath)

        output_path = bpy.path.abspath(context.window_manager.output_path)
        vmt_path = context.window_manager.vmt_path
        lightwarp = context.window_manager.vmt_lightwarp
        halflambert = context.window_manager.vmt_halflambert
        nocull = context.window_manager.vmt_nocull
        
        relative_path = os.path.join("materials", vmt_path).replace("\\", "/")
        
        output_dir = os.path.join(output_path, relative_path)
        os.makedirs(output_dir, exist_ok=True)

        created_vmt_files = []

        for material in bpy.data.materials:
            if material.node_tree:
                base_texture = None
                bump_map = None
                use_bump = False
                use_alpha = False
                color = None
                is_metallic = False
                
                for node in material.node_tree.nodes:
                    if node.type == 'BSDF_PRINCIPLED':
                        roughness_value = node.inputs['Roughness'].default_value
                        if roughness_value == 0:
                            is_metallic = True
                        
                        for input in node.inputs:
                            if input.name == 'Base Color':
                                if input.is_linked:
                                    base_color_node = input.links[0].from_node
                                    if base_color_node.type == 'TEX_IMAGE' and base_color_node.image:
                                        if base_color_node.image.packed_file:
                                            base_texture = base_color_node.image.name
                                        else:
                                            base_texture_path = bpy.path.abspath(base_color_node.image.filepath)
                                            base_texture_with_extension = os.path.basename(base_texture_path)
                                            base_texture_root, _ = os.path.splitext(base_texture_with_extension)
                                            base_texture = base_texture_root
                                else:
                                    base_texture = "white"
                                    color = tuple(round(c * 255) for c in input.default_value[:3])
                            if input.name == 'Normal' and input.is_linked:
                                normal_map_node = input.links[0].from_node
                                if normal_map_node.type == 'NORMAL_MAP':
                                    if normal_map_node.inputs['Color'].is_linked:
                                        normal_image_node = normal_map_node.inputs['Color'].links[0].from_node
                                        if normal_image_node.type == 'TEX_IMAGE' and normal_image_node.image:
                                            if normal_image_node.image.packed_file:
                                                bump_map = normal_image_node.image.name
                                            else:
                                                bump_map_path = bpy.path.abspath(normal_image_node.image.filepath)
                                                bump_map = os.path.splitext(os.path.basename(bump_map_path))[0]
                                            use_bump = True
                            if input.name == 'Alpha' and input.is_linked:
                                use_alpha = True
                
                if base_texture:
                    if base_texture != "white":
                        relative_path = relative_path.replace("materials/", "")
                        base_texture = f"{relative_path}/{base_texture}"
                    vmt_filename = self.create_vmt(material.name, base_texture, bump_map, output_dir, relative_path, lightwarp, halflambert, nocull, use_bump, use_alpha, color, is_metallic)
                    created_vmt_files.append(material.name)
                else:
                    self.report({'WARNING'}, f"No textures found for material: {material.name}")
                    
        if created_vmt_files:
            message = "Created VMT files:" + "\n".join(f"  {file}\n" for file in created_vmt_files)
            bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text=message), title="Info", icon='INFO')

        return {'FINISHED'}
