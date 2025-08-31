import bpy
from .operators.generate_vmt import WM_OT_generate_vmt
from .operators.rename_textures import RenameTexturesOperator
from .operators.materials_convert import ConvertMaterialsOperator, cancel_conversion

TEXTURE_RESOLUTIONS = [
    ("256", "256", ""),
    ("512", "512", ""),
    ("1024", "1024", ""),
    ("2048", "2048", ""),
    ("4096", "4096", "")
]

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
        layout.operator("wm.generate_vmt", text="Generate VMT")
        layout.operator(RenameTexturesOperator.bl_idname, text="Rename Textures")

        layout.separator()
        layout.prop(wm, "texture_max_height", text="Resolution")

        if not wm.conversion_running:
            layout.operator(ConvertMaterialsOperator.bl_idname, text="Convert to VTF")
        else:
            layout.operator("wm.cancel_conversion", text="Cancel Conversion")

        layout.label(text=f"{wm.conversion_progress}% - {wm.conversion_log}")


class CancelConversionOperator(bpy.types.Operator):
    bl_idname = "wm.cancel_conversion"
    bl_label = "Cancel Conversion"

    def execute(self, context):
        cancel_conversion()
        return {'FINISHED'}


def register():
    bpy.types.WindowManager.output_path = bpy.props.StringProperty(name="Path to addon", subtype='DIR_PATH', default="//")
    bpy.types.WindowManager.vmt_path = bpy.props.StringProperty(name="Materials Path", default="models")
    bpy.types.WindowManager.vmt_lightwarp = bpy.props.StringProperty(name="Lightwarp", default="")
    bpy.types.WindowManager.texture_max_height = bpy.props.EnumProperty(name="Max Texture Height",
        items=TEXTURE_RESOLUTIONS, default="1024")
    bpy.types.WindowManager.conversion_progress = bpy.props.IntProperty(default=0, min=0, max=100)
    bpy.types.WindowManager.conversion_log = bpy.props.StringProperty(default="")
    bpy.types.WindowManager.current_texture = bpy.props.StringProperty(default="")
    bpy.types.WindowManager.conversion_running = bpy.props.BoolProperty(default=False)

    bpy.utils.register_class(ConvertMaterialsOperator)
    bpy.utils.register_class(WM_OT_generate_vmt)
    bpy.utils.register_class(RenameTexturesOperator)
    bpy.utils.register_class(SSS_PT_materials_panel)
    bpy.utils.register_class(CancelConversionOperator)


def unregister():
    bpy.utils.unregister_class(SSS_PT_materials_panel)
    bpy.utils.unregister_class(WM_OT_generate_vmt)
    bpy.utils.unregister_class(RenameTexturesOperator)
    bpy.utils.unregister_class(ConvertMaterialsOperator)
    bpy.utils.unregister_class(CancelConversionOperator)

    del bpy.types.WindowManager.output_path
    del bpy.types.WindowManager.vmt_path
    del bpy.types.WindowManager.vmt_lightwarp
    del bpy.types.WindowManager.texture_max_height
    del bpy.types.WindowManager.conversion_progress
    del bpy.types.WindowManager.conversion_log
    del bpy.types.WindowManager.current_texture
    del bpy.types.WindowManager.conversion_running
