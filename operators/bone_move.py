import bpy

class BoneMoveOperator(bpy.types.Operator):
    bl_idname = "object.bone_move_operator"
    bl_label = "Point bones"
    bl_description = "Points tail of selected bones to 3D cursor in flat dimension"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = bpy.context.selected_editable_bones
        cursor_location = bpy.context.scene.cursor.location
        bone_lengths = {}

        if bpy.context.active_object and bpy.context.active_object.type == 'ARMATURE' and bpy.context.active_object.mode == 'EDIT':
            if selection:
                for bone in selection:
                    bone_lengths[bone.name] = (bone.tail - bone.head).length

                for bone in selection:
                    bone.tail.x = cursor_location.x
                    bone.tail.y = cursor_location.y

                for bone in selection:
                    original_length = bone_lengths[bone.name]
                    direction = (bone.tail - bone.head).normalized()
                    bone.tail = bone.head + direction * original_length
                bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Bone adjustment completed."))
            else:
                bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="No bones are selected."), title="Warning", icon='ERROR')
        else:
            bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Select some bones in EDIT or POSE mode first."), title="Warning", icon='ERROR')
        return {'FINISHED'}
