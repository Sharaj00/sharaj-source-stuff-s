import bpy

from .operators.generate_qc import GenerateQCOperator
from .operators.bodygroup_to_clipboard import BodygroupToClipboardOperator

class SSS_PT_qc_panel(bpy.types.Panel):
    bl_label = "QC tools"
    bl_idname = "SSS_PT_qc_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SSS'
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.operator(GenerateQCOperator.bl_idname, text="Generate .qc for props")
        layout.operator(BodygroupToClipboardOperator.bl_idname, text="Bodygroups to clipboard")

def register():
    bpy.utils.register_class(SSS_PT_qc_panel)
    bpy.utils.register_class(GenerateQCOperator)
    bpy.utils.register_class(BodygroupToClipboardOperator)

def unregister():
    bpy.utils.unregister_class(SSS_PT_qc_panel)
    bpy.utils.unregister_class(GenerateQCOperator)
    bpy.utils.unregister_class(BodygroupToClipboardOperator)
