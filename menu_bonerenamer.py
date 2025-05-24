import bpy
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import EnumProperty, StringProperty, PointerProperty
from .operators.bonerenamer import (
    SSS_OT_AutofillBoneNames,
    SSS_OT_RenameBones,
    SSS_BoneMapProperties,
    SSS_BonePropertyGroup,
    BONE_POSITIONS
)

class SSS_PT_BoneRenamer(Panel):
    bl_label = "bone renamer"
    bl_idname = "SSS_PT_bone_renamer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SSS'

    def draw(self, context):
        layout = self.layout
        props = context.scene.sss_bone_map

        layout.prop(props, "armature_obj")
        layout.prop(props, "target_standard")

        layout.operator("sss.autofill_bone_names", text="Autofill")
        layout.operator("sss.rename_bones", text="Rename Bones")

        box = layout.box()
        for pos in BONE_POSITIONS:
            bone_prop = getattr(props, pos, None)
            if bone_prop:
                if pos in ['Pelvis', 'Spine1', 'Spine2', 'Spine3', 'Spine4', 'Neck', 'Head']:
                    row = box.row(align=True)
                    row.label(text=pos)
                    row.prop(bone_prop, "bone_enum", text="")
                else:
                    row = box.row(align=True)
                    row.label(text=pos)
                    row.prop(bone_prop, "bone_enum_left", text="")
                    row.prop(bone_prop, "bone_enum_right", text="")

classes = [
    SSS_BonePropertyGroup,
    SSS_BoneMapProperties,
    SSS_OT_AutofillBoneNames,
    SSS_OT_RenameBones,
    SSS_PT_BoneRenamer
]

def register():
    # Удаляем старую регистрацию, если была
    if hasattr(bpy.types.Scene, 'sss_bone_map'):
        del bpy.types.Scene.sss_bone_map

    # Регистрируем классы
    for cls in classes:
        bpy.utils.register_class(cls)

    # Регистрируем PropertyGroup
    bpy.types.Scene.sss_bone_map = PointerProperty(type=SSS_BoneMapProperties)

    # Динамически добавляем PointerProperty для каждой позиции кости
    for pos in BONE_POSITIONS:
        setattr(SSS_BoneMapProperties, pos, PointerProperty(type=SSS_BonePropertyGroup))

def unregister():
    for pos in BONE_POSITIONS:
        if hasattr(SSS_BoneMapProperties, pos):
            delattr(SSS_BoneMapProperties, pos)

    del bpy.types.Scene.sss_bone_map

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
