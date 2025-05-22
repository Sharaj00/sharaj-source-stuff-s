import bpy

from .operators.create_vmt import WM_OT_create_vmt
from .operators.rename_textures import RenameTexturesOperator

class SSS_PT_materials_panel(bpy.types.Panel):
    bl_label = "materials tools"
    bl_idname = "SSS_PT_materials_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SSS'
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.prop(wm, "output_path")
        layout.prop(wm, "vmt_path")
        layout.prop(wm, "vmt_lightwarp")

        row = layout.row()
        row.prop(wm, "vmt_halflambert", text="Halflambert")
        row.prop(wm, "vmt_nocull", text="NoCull")
        layout.operator(WM_OT_create_vmt.bl_idname)
        layout.operator(RenameTexturesOperator.bl_idname, text="Rename Textures")

def register():
    bpy.utils.register_class(SSS_PT_materials_panel)
    bpy.utils.register_class(WM_OT_create_vmt)
    bpy.utils.register_class(RenameTexturesOperator)
    
    bpy.types.WindowManager.output_path = bpy.props.StringProperty(
        name="Path to addon",
        description="Absolute path (Leave // for relative to .blend)",
        subtype='DIR_PATH',
        default="//"
    )
    bpy.types.WindowManager.vmt_path = bpy.props.StringProperty(
        name="Materials Path",
        description="Relative path",
        default="models"
    )
    bpy.types.WindowManager.vmt_lightwarp = bpy.props.StringProperty(
        name="Lightwarp",
        description="Lightwarp texture name",
        default=""
    )
    bpy.types.WindowManager.vmt_halflambert = bpy.props.BoolProperty(
        name="Halflambert",
        description="Enable halflambert",
        default=False
    )
    bpy.types.WindowManager.vmt_nocull = bpy.props.BoolProperty(
        name="NoCull",
        description="Disable culling",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(SSS_PT_materials_panel)
    bpy.utils.unregister_class(WM_OT_create_vmt)
    bpy.utils.unregister_class(RenameTexturesOperator)
    
    del bpy.types.WindowManager.output_path
    del bpy.types.WindowManager.vmt_path
    del bpy.types.WindowManager.vmt_lightwarp
    del bpy.types.WindowManager.vmt_halflambert
    del bpy.types.WindowManager.vmt_nocull
