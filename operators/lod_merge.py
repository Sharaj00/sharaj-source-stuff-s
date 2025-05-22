import bpy

class LodMergeOperator(bpy.types.Operator):
    bl_idname = "export.selected_bones"
    bl_label = "LOD Bones"
    bl_description = "Generates LOD merging parameters for selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        if obj is None or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Select armature")
            return {'CANCELLED'}
        
        if obj.mode not in {'POSE', 'EDIT'}:
            self.report({'ERROR'}, "You need to be in edit/pose mode")
            return {'CANCELLED'}
        
        bones = []
        if obj.mode == 'POSE':
            bones = [bone for bone in obj.pose.bones if bone.bone.select]
        elif obj.mode == 'EDIT':
            bones = [bone for bone in obj.data.edit_bones if bone.select]

        if not bones:
            self.report({'WARNING'}, "No selected bones")
            return {'CANCELLED'}

        lines = []
        for bone in bones:
            bone_name = bone.name
            parent_name = bone.parent.name if bone.parent else "None"
            lines.append(f'replacebone "{bone_name}" "{parent_name}"')

        result_text = "\n".join(lines)
        bpy.context.window_manager.clipboard = result_text

        self.report({'INFO'}, f"{len(bones)} bones copied to clipboard")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(LodMergeOperator)

def unregister():
    bpy.utils.unregister_class(LodMergeOperator)
