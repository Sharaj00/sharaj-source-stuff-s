import bpy

from .operators.create_vmt import WM_OT_create_vmt
from .operators.rename_textures import RenameTexturesOperator

from .operators.deselect_biped import DeselectBipedOperator
from .operators.bone_move import BoneMoveOperator
from .operators.bone_adjust import BoneAdjustOperator

from .operators.generate_jigglebones import (
    GenerateJigglebonesSet1Operator,
    GenerateJigglebonesSet2Operator,
    GenerateJigglebonesToClipboardOperator
)

from .operators.generate_qc import GenerateQCOperator
from .operators.bodygroup_to_clipboard import BodygroupToClipboardOperator

from .operators.proportion_trick import (
    ProportionTrick,
    ContinueOperator,
    CancelOperator
)

from .operators.export_selected_bones import ExportSelectedBonesOperator

from .operators.copy_transforms_from_selected import CopyTransformsFromSelectedOperator

class SSS_main_panel(bpy.types.Panel):
    bl_label = "some stuff's"
    bl_idname = "SSS_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SSS'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        armatures = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']

        layout.prop(wm, "output_path")
        layout.prop(wm, "vmt_path")
        layout.prop(wm, "vmt_lightwarp")
        
        row = layout.row()
        row.prop(wm, "vmt_halflambert", text="Halflambert")
        row.prop(wm, "vmt_nocull", text="NoCull")

        layout.operator(WM_OT_create_vmt.bl_idname)
        layout.operator(RenameTexturesOperator.bl_idname, text="Rename Textures")
        layout.separator()
        layout.operator(BoneMoveOperator.bl_idname, text="Point Bones")
        layout.operator(DeselectBipedOperator.bl_idname, text="Deselect Biped")
        layout.operator(BoneAdjustOperator.bl_idname, text="Fix jigglebones")
        layout.operator(ExportSelectedBonesOperator.bl_idname, text="LOD Merge selected bones")
        layout.separator()

        row = layout.row(align=True)
        row.operator("object.generate_jigglebones_set1", text="Pitch limited")
        small_row = row.row(align=True)
        small_row.scale_x = 0.3  # Делаем кнопку меньше
        button = small_row.operator("object.generate_jigglebones_clipboard", text="📋")
        button.mode = "limited"
        
        row = layout.row(align=True)
        row.operator("object.generate_jigglebones_set2", text="Free")
        small_row = row.row(align=True)
        small_row.scale_x = 0.3  # Делаем кнопку меньше
        button = small_row.operator("object.generate_jigglebones_clipboard", text="📋")
        button.mode = "free"

        layout.separator()
        layout.separator()
        layout.operator(GenerateQCOperator.bl_idname, text="Generate .qc for props")
        layout.operator(BodygroupToClipboardOperator.bl_idname, text="Bodygroups to clipboard")
        
        row = layout.row(align=True)
        row.prop(wm, "sss_target_armature", text="To")
        row.prop(wm, "sss_source_armature", text="From")
        layout.operator("object.copy_transforms_from_selected", text="Copy Transforms")
        
        layout.separator()
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
    bpy.utils.register_class(SSS_main_panel)

    bpy.utils.register_class(WM_OT_create_vmt)
    bpy.utils.register_class(RenameTexturesOperator)
    
    bpy.utils.register_class(BoneMoveOperator)
    bpy.utils.register_class(DeselectBipedOperator)
    bpy.utils.register_class(BoneAdjustOperator)
    
    bpy.utils.register_class(GenerateJigglebonesSet1Operator)
    bpy.utils.register_class(GenerateJigglebonesSet2Operator)
    bpy.utils.register_class(GenerateJigglebonesToClipboardOperator)
    bpy.utils.register_class(GenerateQCOperator)
    bpy.utils.register_class(BodygroupToClipboardOperator)

    bpy.utils.register_class(ProportionTrick)
    bpy.utils.register_class(ContinueOperator)
    bpy.utils.register_class(CancelOperator)
    
    bpy.utils.register_class(ExportSelectedBonesOperator)
    
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
    bpy.types.WindowManager.is_male = bpy.props.BoolProperty(
        name="Male?",
        description="Gender of reference armature",
        default=False
    )
    
    bpy.types.WindowManager.script_executed = bpy.props.BoolProperty(default=False)
    
    bpy.utils.register_class(CopyTransformsFromSelectedOperator)
    
    bpy.types.WindowManager.sss_source_armature = bpy.props.PointerProperty(
        name="Source Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    bpy.types.WindowManager.sss_target_armature = bpy.props.PointerProperty(
        name="Target Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )

    
def unregister():
    bpy.utils.unregister_class(SSS_main_panel)
    
    bpy.utils.unregister_class(WM_OT_create_vmt)
    bpy.utils.unregister_class(RenameTexturesOperator)
    
    bpy.utils.unregister_class(BoneMoveOperator)
    bpy.utils.unregister_class(DeselectBipedOperator)
    bpy.utils.unregister_class(BoneAdjustOperator)
    
    bpy.utils.unregister_class(GenerateJigglebonesSet1Operator)
    bpy.utils.unregister_class(GenerateJigglebonesSet2Operator)
    bpy.utils.unregister_class(GenerateJigglebonesToClipboardOperator)
    bpy.utils.unregister_class(GenerateQCOperator)
    bpy.utils.unregister_class(BodygroupToClipboardOperator)
    
    bpy.utils.unregister_class(ProportionTrick)
    bpy.utils.unregister_class(ContinueOperator)
    bpy.utils.unregister_class(CancelOperator)
    
    bpy.utils.unregister_class(ExportSelectedBonesOperator)

    del bpy.types.WindowManager.output_path
    del bpy.types.WindowManager.vmt_path
    del bpy.types.WindowManager.vmt_lightwarp
    del bpy.types.WindowManager.vmt_halflambert
    del bpy.types.WindowManager.vmt_nocull
    del bpy.types.WindowManager.script_executed
    del bpy.types.WindowManager.is_male
    
    del bpy.types.WindowManager.sss_source_armature
    del bpy.types.WindowManager.sss_target_armature
