import bpy

class BoneMergeOperator(bpy.types.Operator):
    bl_idname = "object.bone_merge_operator"
    bl_label = "Merge Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        active_object = bpy.context.active_object
        selected_bones = bpy.context.selected_editable_bones
        armature = active_object.data

        if len(selected_bones) < 2:
            self.report({'WARNING'}, "Select at least two bones to merge.")
            return {'CANCELLED'}

        for i in range(len(selected_bones) - 1):
            bone1 = selected_bones[i]
            bone2 = selected_bones[i + 1]

            if bone1.parent == bone2:
                merge_bone = bone1
                parent_bone = bone2
            elif bone2.parent == bone1:
                merge_bone = bone2
                parent_bone = bone1
            else:
                self.report({'WARNING'}, f"Bones {bone1.name} and {bone2.name} are not in a direct parent-child relationship.")
                continue

            new_length = (parent_bone.head - merge_bone.tail).length
            parent_bone.tail = merge_bone.head + (merge_bone.tail - merge_bone.head).normalized() * new_length

            for child in merge_bone.children:
                child.parent = parent_bone

            armature.edit_bones.remove(merge_bone)

        return {'FINISHED'}
