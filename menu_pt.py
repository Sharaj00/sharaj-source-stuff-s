import bpy

from .operators.proportion_trick import (
    ProportionTrick,
    ContinueOperator,
    CancelOperator
)

class SSS_PT_pt_panel(bpy.types.Panel):
    bl_label = "proportion trick"
    bl_idname = "SSS_PT_pt_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SSS'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        armatures = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']
        
        if wm.script_executed:
            layout.operator("object.continue", text="Continue")
            layout.operator("object.cancel", text="Cancel")
        elif armatures:  
            row = layout.row(align=True)
            row.operator("object.proportion_trick", text="Proportion trick")
            row.prop(wm, "is_male", text="Male?")
        else:
            layout.label(text="Select armature to start proportion trick.")

def register():
    bpy.utils.register_class(SSS_PT_pt_panel)

    bpy.utils.register_class(ProportionTrick)
    bpy.utils.register_class(ContinueOperator)
    bpy.utils.register_class(CancelOperator)
    bpy.types.WindowManager.script_executed = bpy.props.BoolProperty(default=False)

    bpy.types.WindowManager.is_male = bpy.props.BoolProperty(
        name="Male?",
        description="Gender of reference armature",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(SSS_PT_pt_panel)

    bpy.utils.unregister_class(ProportionTrick)
    bpy.utils.unregister_class(ContinueOperator)
    bpy.utils.unregister_class(CancelOperator)
    del bpy.types.WindowManager.script_executed
    del bpy.types.WindowManager.is_male