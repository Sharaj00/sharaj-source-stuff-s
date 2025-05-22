import bpy

from .operators.eye_qc import (
    SSS_OT_SetEyeLeft,
    SSS_OT_SetEyeRight,
    SSS_OT_GenerateEyesQC
)

class SSS_PT_eyes_panel(bpy.types.Panel):
    bl_label = "eyes tools"
    bl_idname = "SSS_PT_eyes_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SSS'
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        col = layout.column(align=True)
    
        col.prop(wm, "eye_left_coord", text="Left Eye XYZ")
        col.operator("sss.set_eye_left", text="Set from 3D Cursor")
        col.prop(wm, "eye_left_material", text="Material")

        col.prop(wm, "eye_right_coord", text="Right Eye XYZ")
        col.operator("sss.set_eye_right", text="Set from 3D Cursor")
        col.prop(wm, "eye_right_material", text="Material")
        
        col.operator("sss.generate_eyes_qc", text="Generate")

def register():
    bpy.utils.register_class(SSS_PT_eyes_panel)

    bpy.utils.register_class(SSS_OT_SetEyeLeft)
    bpy.utils.register_class(SSS_OT_SetEyeRight)
    bpy.utils.register_class(SSS_OT_GenerateEyesQC)

    bpy.types.WindowManager.eye_left_coord = bpy.props.FloatVectorProperty(
        name="Left Eye", subtype='XYZ', size=3, default=(0.0, 0.0, 0.0)
    )
    bpy.types.WindowManager.eye_right_coord = bpy.props.FloatVectorProperty(
        name="Right Eye", subtype='XYZ', size=3, default=(0.0, 0.0, 0.0)
    )
    
    def get_materials(self, context):
        return [(mat.name, mat.name, "") for mat in bpy.data.materials]
        
    bpy.types.WindowManager.eye_left_material = bpy.props.EnumProperty(
        name="Left Eye Material",
        description="Material name for left eye",
        items=get_materials
    )
    bpy.types.WindowManager.eye_right_material = bpy.props.EnumProperty(
        name="Right Eye Material",
        description="Material name for right eye",
        items=get_materials
    )


def unregister():
    bpy.utils.unregister_class(SSS_PT_eyes_panel)

    bpy.utils.unregister_class(SSS_OT_SetEyeLeft)
    bpy.utils.unregister_class(SSS_OT_SetEyeRight)
    bpy.utils.unregister_class(SSS_OT_GenerateEyesQC)
    
    del bpy.types.WindowManager.eye_left_coord
    del bpy.types.WindowManager.eye_right_coord
    
    del bpy.types.WindowManager.eye_left_material
    del bpy.types.WindowManager.eye_right_material
