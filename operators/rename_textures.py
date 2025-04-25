import bpy
import os

class RenameTexturesOperator(bpy.types.Operator):
    bl_idname = "object.rename_textures"
    bl_label = "Rename Textures"
    bl_description = "Renames texture names in blend file to material name, also renames actual filenames"

    def execute(self, context):
        messages = []

        blend_filepath = bpy.data.filepath
        blend_dir = os.path.dirname(blend_filepath)
        
        for material in bpy.data.materials:
            if material.node_tree:
                for node in material.node_tree.nodes:
                    if node.type in {'BSDF_PRINCIPLED', 'EMISSION'}:
                        for input_slot in node.inputs:
                            if input_slot.is_linked:
                                from_node = input_slot.links[0].from_node
                                if from_node.type == 'TEX_IMAGE':
                                    if input_slot.name == 'Base Color':
                                        messages.extend(self.rename_texture(material, from_node.image, material.name + '_d', blend_dir))
                                    elif node.type == 'EMISSION' and input_slot.name == 'Color':
                                        messages.extend(self.rename_texture(material, from_node.image, material.name + '_em', blend_dir))
                                    elif input_slot.name == 'Roughness':
                                        messages.extend(self.rename_texture(material, from_node.image, material.name + '_r', blend_dir))
                                    elif input_slot.name == 'Metallic':
                                        messages.extend(self.rename_texture(material, from_node.image, material.name + '_m', blend_dir))
                                    # elif input_slot.name == 'Alpha':
                                        # messages.extend(self.rename_texture(material, from_node.image, material.name + '_op', blend_dir))
                                    elif input_slot.name == 'Subsurface':
                                        messages.extend(self.rename_texture(material, from_node.image, material.name + '_sss', blend_dir))
                                elif from_node.type == 'NORMAL_MAP':
                                    normal_map_node = from_node
                                    if normal_map_node.inputs['Color'].is_linked:
                                        texture_node = normal_map_node.inputs['Color'].links[0].from_node
                                        if texture_node.type == 'TEX_IMAGE':
                                            messages.extend(self.rename_texture(material, texture_node.image, material.name + '_n', blend_dir))
                                elif from_node.type == 'BUMP':
                                    bump_map_node = from_node
                                    if bump_map_node.inputs['Height'].is_linked:
                                        texture_node = bump_map_node.inputs['Height'].links[0].from_node
                                        if texture_node.type == 'TEX_IMAGE':
                                            messages.extend(self.rename_texture(material, texture_node.image, material.name + '_bump', blend_dir))
                                elif from_node.type == 'MIX_RGB' and from_node.blend_type == 'MULTIPLY':
                                    if input_slot.name == 'Base Color':
                                        if from_node.inputs['Color1'].is_linked and from_node.inputs['Color2'].is_linked:
                                            base_color_node = from_node.inputs['Color1'].links[0].from_node
                                            ao_node = from_node.inputs['Color2'].links[0].from_node
                                            if base_color_node.type == 'TEX_IMAGE':
                                                messages.extend(self.rename_texture(material, base_color_node.image, material.name + '_d', blend_dir))
                                            if ao_node.type == 'TEX_IMAGE':
                                                messages.extend(self.rename_texture(material, ao_node.image, material.name + '_ao', blend_dir))
        if messages:
            bpy.context.window_manager.popup_menu(lambda popup, context: self.display_messages(popup, context, messages), title="Renaming Results")

        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        return {'FINISHED'}

    def rename_texture(self, material, texture, new_name, blend_dir):
        messages = []
        
        if texture:
            old_texture_name = texture.name
            texture.name = new_name

            if texture.packed_file:
                messages.append(f'Packed textures renamed: {texture.filepath}')
                return messages

            old_filepath = bpy.path.abspath(texture.filepath)
            new_filepath = os.path.join(os.path.dirname(old_filepath), new_name + os.path.splitext(old_filepath)[1])

            old_filepath = os.path.normpath(old_filepath)
            new_filepath = os.path.normpath(new_filepath)
            
            if old_filepath != new_filepath:
                try:
                    if os.path.exists(new_filepath):
                        os.remove(new_filepath)
                    if os.path.exists(old_filepath):
                        os.rename(old_filepath, new_filepath)
                        texture.filepath = bpy.path.relpath(new_filepath)
                        messages.append(f'Renamed texture file: {old_filepath} -> {new_filepath}')
                    else:
                        messages.append(f'File not found: {old_filepath}')
                except FileNotFoundError:
                    messages.append(f'File not found: {old_filepath}')
                except PermissionError:
                    messages.append(f'Not enough permissions to rename: {old_filepath}')
                except Exception as e:
                    messages.append(f'Error during file renaming: {e}')
        
        return messages

    def display_messages(self, popup, context, messages):
        layout = popup.layout
        for message in messages:
            layout.label(text=message)

def register():
    bpy.utils.register_class(RenameTexturesOperator)

def unregister():
    bpy.utils.unregister_class(RenameTexturesOperator)

if __name__ == "__main__":
    register()

    # Test call
    bpy.ops.object.rename_textures()
