import bpy

class SSS_OT_SetEyeLeft(bpy.types.Operator):
    bl_idname = "sss.set_eye_left"
    bl_label = "Set Left Eye from Cursor"

    def execute(self, context):
        context.window_manager.eye_left_coord = context.scene.cursor.location
        return {'FINISHED'}


class SSS_OT_SetEyeRight(bpy.types.Operator):
    bl_idname = "sss.set_eye_right"
    bl_label = "Set Right Eye from Cursor"

    def execute(self, context):
        context.window_manager.eye_right_coord = context.scene.cursor.location
        return {'FINISHED'}


class SSS_OT_GenerateEyesQC(bpy.types.Operator):
    bl_idname = "sss.generate_eyes_qc"
    bl_label = "Generate Eyes QC"

    def execute(self, context):
        wm = context.window_manager
        left = wm.eye_left_coord
        right = wm.eye_right_coord
        mat_left = wm.eye_left_material
        mat_right = wm.eye_right_material

        left_str = f"{left[0]:.3f} {left[1]:.3f} {left[2]:.3f}"
        right_str = f"{right[0]:.3f} {right[1]:.3f} {right[2]:.3f}"

        qc_text = (
                f'eyeball "eye_right" "ValveBiped.Bip01_Head1" {right_str} "{mat_right}" 0 4 "iris_unused" 0.5\n'
                f'eyeball "eye_left" "ValveBiped.Bip01_Head1" {left_str} "{mat_left}" 0 -4 "iris_unused" 0.5\n'
                f'flexcontroller eyes range -10 10 "eyes_updown"\n'
                f'flexcontroller eyes range -10 10 "eyes_rightleft"\n'
        )

        wm.clipboard = qc_text
        self.report({'INFO'}, "QC copied to clipboard.")
        return {'FINISHED'}
