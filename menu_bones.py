import bpy

from .operators.deselect_biped import DeselectBipedOperator
from .operators.bone_move import BoneMoveOperator
from .operators.bone_adjust import BoneAdjustOperator

from .operators.generate_jigglebones import (
    GenerateJigglebonesSet1Operator,
    GenerateJigglebonesSet2Operator,
    GenerateJigglebonesToClipboardOperator
)

from .operators.lod_merge import LodMergeOperator
from .operators.copy_transforms_from_selected import CopyTransformsFromSelectedOperator

class SSS_PT_bones_panel(bpy.types.Panel):
    bl_label = "bone tools"
    bl_idname = "SSS_PT_bones_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SSS'
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.operator(DeselectBipedOperator.bl_idname, text="Deselect Biped")
        layout.operator(BoneAdjustOperator.bl_idname, text="Fix jigglebones")
        layout.operator(BoneMoveOperator.bl_idname, text="Point Bones")
        layout.operator(LodMergeOperator.bl_idname, text="LOD Merge selected bones")

        layout.separator()
        layout.label(text="Generate parameters for selected bones")
        row = layout.row(align=True)
        row.operator("object.generate_jigglebones_set1", text="Pitch limited")
        small_row = row.row(align=True)
        small_row.scale_x = 0.3
        button = small_row.operator("object.generate_jigglebones_clipboard", text="📋")
        button.mode = "limited"
        row = layout.row(align=True)
        row.operator("object.generate_jigglebones_set2", text="Free")
        small_row = row.row(align=True)
        small_row.scale_x = 0.3
        button = small_row.operator("object.generate_jigglebones_clipboard", text="📋")
        button.mode = "free"

        layout.separator()
        row = layout.row(align=True)
        row.label(text="Target:")
        row.label(text="Source:")
        
        row = layout.row(align=True)
        row.prop(wm, "target_armature", text="")
        row.prop(wm, "source_armature", text="")
        
        layout.operator("object.copy_transforms_from_selected", text="Copy Transforms")

def register():
    bpy.utils.register_class(SSS_PT_bones_panel)

    bpy.utils.register_class(BoneMoveOperator)
    bpy.utils.register_class(DeselectBipedOperator)
    bpy.utils.register_class(BoneAdjustOperator)

    bpy.utils.register_class(GenerateJigglebonesSet1Operator)
    bpy.utils.register_class(GenerateJigglebonesSet2Operator)
    bpy.utils.register_class(GenerateJigglebonesToClipboardOperator)
    bpy.utils.register_class(LodMergeOperator)
    bpy.utils.register_class(CopyTransformsFromSelectedOperator)

    bpy.types.WindowManager.source_armature = bpy.props.PointerProperty(
        name="Source Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )
    bpy.types.WindowManager.target_armature = bpy.props.PointerProperty(
        name="Target Armature",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )

def unregister():
    bpy.utils.unregister_class(SSS_PT_bones_panel)
    bpy.utils.unregister_class(BoneMoveOperator)
    bpy.utils.unregister_class(DeselectBipedOperator)
    bpy.utils.unregister_class(BoneAdjustOperator)

    bpy.utils.unregister_class(GenerateJigglebonesSet1Operator)
    bpy.utils.unregister_class(GenerateJigglebonesSet2Operator)
    bpy.utils.unregister_class(GenerateJigglebonesToClipboardOperator)
    bpy.utils.unregister_class(LodMergeOperator)
    bpy.utils.unregister_class(CopyTransformsFromSelectedOperator)

    del bpy.types.WindowManager.source_armature
    del bpy.types.WindowManager.target_armature
