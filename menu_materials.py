import bpy

from .operators.generate_vmt import WM_OT_generate_vmt
from .operators.rename_textures import RenameTexturesOperator
from .operators.materials_convert import ConvertMaterialsOperator

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
            op = layout.operator(ConvertMaterialsOperator.bl_idname, text="Cancel Conversion")
            op.cancel = True

        layout.label(text=f"{wm.conversion_progress}% - {wm.current_texture}")
        layout.label(text=wm.conversion_log)



def register():
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
    bpy.types.WindowManager.texture_max_height = bpy.props.EnumProperty(
        name="Max Texture Height",
        description="Limit the height of textures on export",
        items=TEXTURE_RESOLUTIONS,
        default="1024"
    )
    bpy.types.WindowManager.conversion_progress = bpy.props.IntProperty(
        name="Conversion Progress",
        default=0,
        min=0,
        max=100
    )
    bpy.types.WindowManager.conversion_log = bpy.props.StringProperty(default="")
    bpy.types.WindowManager.current_texture = bpy.props.StringProperty(default="")
    bpy.types.WindowManager.conversion_running = bpy.props.BoolProperty(default=False)

    bpy.utils.register_class(ConvertMaterialsOperator)
    bpy.utils.register_class(WM_OT_generate_vmt)
    bpy.utils.register_class(RenameTexturesOperator)

    bpy.utils.register_class(SSS_PT_materials_panel)


def unregister():
    bpy.utils.unregister_class(SSS_PT_materials_panel)
    bpy.utils.unregister_class(WM_OT_generate_vmt)
    bpy.utils.unregister_class(RenameTexturesOperator)
    bpy.utils.unregister_class(ConvertMaterialsOperator)

    del bpy.types.WindowManager.output_path
    del bpy.types.WindowManager.vmt_path
    del bpy.types.WindowManager.vmt_lightwarp
    del bpy.types.WindowManager.texture_max_height
    del bpy.types.WindowManager.conversion_progress
    del bpy.types.WindowManager.conversion_log
    del bpy.types.WindowManager.current_texture
    del bpy.types.WindowManager.conversion_running
