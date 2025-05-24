import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import EnumProperty, StringProperty, PointerProperty
from .bone_standards import BONE_STANDARD_MAPS, BONE_STANDARDS, BONE_POSITIONS


def get_standard_reverse_map(standard_map):
    reverse_map = {}
    for label, bone_data in standard_map.items():
        if isinstance(bone_data, dict):
            for side, bone_name in bone_data.items():
                if bone_name and bone_name != 'none':
                    reverse_map[bone_name.lower().replace("_", "").replace(".", "")] = label
        else:
            if bone_data and bone_data != 'none':
                reverse_map[bone_data.lower().replace("_", "").replace(".", "")] = label
    return reverse_map

def detect_bone_standard(armature):
    bone_names = {bone.name.lower().replace("_", "").replace(".", "") for bone in armature.data.bones}
    
    best_match = None
    best_score = 0
    
    for std_name, std_map in BONE_STANDARD_MAPS.items():
        score = 0
        for pos in BONE_POSITIONS:
            if pos in ['Pelvis', 'Spine1', 'Spine2', 'Spine3', 'Spine4', 'Neck', 'Head']:
                std_bone = std_map.get(pos, "").lower().replace("_", "").replace(".", "")
                if std_bone and any(std_bone in bn for bn in bone_names):
                    score += 1
            else:
                left_std = std_map.get(pos, {}).get('left', "").lower().replace("_", "").replace(".", "")
                right_std = std_map.get(pos, {}).get('right', "").lower().replace("_", "").replace(".", "")
                
                left_match = any(left_std in bn and ('l' in bn or 'left' in bn) for bn in bone_names) if left_std else False
                right_match = any(right_std in bn and ('r' in bn or 'right' in bn) for bn in bone_names) if right_std else False
                
                if left_match or right_match:
                    score += 1
                    
        if score > best_score:
            best_score = score
            best_match = std_name
            
    return best_match if best_score > 5 else None


def update_bone_enum(self, context):
    props = context.scene.sss_bone_map
    if not props.armature_obj:
        return []

    armature = props.armature_obj
    if armature.type != 'ARMATURE':
        return []

    return [(bone.name, bone.name, "", i) for i, bone in enumerate(armature.data.bones)]


class SSS_BonePropertyGroup(PropertyGroup):
    bone_enum: EnumProperty(
        name="Bone",
        items=update_bone_enum,
        description="Select a bone from the armature"
    )
    bone_enum_left: EnumProperty(
        name="Left Bone",
        items=update_bone_enum,
        description="Select a left bone from the armature"
    )
    bone_enum_right: EnumProperty(
        name="Right Bone",
        items=update_bone_enum,
        description="Select a right bone from the armature"
    )


class SSS_BoneMapProperties(PropertyGroup):
    armature_obj: PointerProperty(
        name="Armature",
        description="Select the armature object",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == 'ARMATURE'
    )

    target_standard: EnumProperty(
        name="Rename To",
        items=BONE_STANDARDS
    )


class SSS_OT_AutofillBoneNames(Operator):
    bl_idname = "sss.autofill_bone_names"
    bl_label = "Autofill Bone Names"
    bl_description = "Autofill bone names based on detected standard"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.sss_bone_map
        if not props.armature_obj:
            self.report({'WARNING'}, "Armature not selected")
            return {'CANCELLED'}

        armature = props.armature_obj
        detected_standard = detect_bone_standard(armature)
        if not detected_standard:
            self.report({'WARNING'}, "No matching bone standard detected")
            return {'CANCELLED'}

        # Создаем словарь всех костей арматуры в нижнем регистре без спецсимволов
        bone_names_map = {
            bone.name.lower().replace("_", "").replace(".", ""): bone.name
            for bone in armature.data.bones
        }

        # Получаем стандарт для сравнения
        standard_map = BONE_STANDARD_MAPS[detected_standard]
        
        # Проходим по всем позициям костей в стандарте
        for bone_pos in BONE_POSITIONS:
            prop = getattr(props, bone_pos, None)
            if not prop:
                continue
                
            # Для одиночных костей
            if bone_pos in ['Pelvis', 'Spine1', 'Spine2', 'Spine3', 'Spine4', 'Neck', 'Head']:
                standard_name = standard_map.get(bone_pos, "").lower().replace("_", "").replace(".", "")
                if not standard_name:
                    continue
                    
                # Ищем наиболее похожее название кости
                for bone_lc, bone_name in bone_names_map.items():
                    if standard_name in bone_lc:
                        prop.bone_enum = bone_name
                        break
                        
            # Для парных костей
            else:
                # Левая сторона
                left_std = standard_map.get(bone_pos, {}).get('left', "").lower().replace("_", "").replace(".", "")
                if left_std:
                    for bone_lc, bone_name in bone_names_map.items():
                        if left_std in bone_lc and ('l' in bone_lc or 'left' in bone_lc):
                            if hasattr(prop, 'bone_enum_left'):
                                prop.bone_enum_left = bone_name
                            break
                            
                # Правая сторона
                right_std = standard_map.get(bone_pos, {}).get('right', "").lower().replace("_", "").replace(".", "")
                if right_std:
                    for bone_lc, bone_name in bone_names_map.items():
                        if right_std in bone_lc and ('r' in bone_lc or 'right' in bone_lc):
                            if hasattr(prop, 'bone_enum_right'):
                                prop.bone_enum_right = bone_name
                            break

        self.report({'INFO'}, f"Autofill completed using {detected_standard} standard")
        return {'FINISHED'}



class SSS_OT_RenameBones(Operator):
    bl_idname = "sss.rename_bones"
    bl_label = "Rename Bones"

    @classmethod
    def poll(cls, context):
        return context.scene.sss_bone_map.armature_obj is not None

    def execute(self, context):
        props = context.scene.sss_bone_map
        if not props.armature_obj:
            self.report({'WARNING'}, "Armature not selected")
            return {'CANCELLED'}

        armature = props.armature_obj
        if armature.type != 'ARMATURE':
            self.report({'WARNING'}, "Selected object is not an armature")
            return {'CANCELLED'}

        target_standard = props.target_standard
        bone_map = BONE_STANDARD_MAPS.get(target_standard)
        if not bone_map:
            self.report({'ERROR'}, "Unknown bone standard selected")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        for bone_pos in BONE_POSITIONS:
            prop = getattr(props, bone_pos, None)
            if prop:
                if bone_pos in ['Pelvis', 'Spine1', 'Spine2', 'Spine3', 'Spine4', 'Neck', 'Head']:
                    if prop.bone_enum:
                        bone = armature.data.edit_bones.get(prop.bone_enum)
                        if bone:
                            new_bone_name = bone_map.get(bone_pos)
                            if new_bone_name:
                                bone.name = new_bone_name
                else:
                    if hasattr(prop, 'bone_enum_left') and prop.bone_enum_left:
                        bone = armature.data.edit_bones.get(prop.bone_enum_left)
                        if bone:
                            new_bone_name = bone_map.get(bone_pos, {}).get('left')
                            if new_bone_name:
                                bone.name = new_bone_name
                    if hasattr(prop, 'bone_enum_right') and prop.bone_enum_right:
                        bone = armature.data.edit_bones.get(prop.bone_enum_right)
                        if bone:
                            new_bone_name = bone_map.get(bone_pos, {}).get('right')
                            if new_bone_name:
                                bone.name = new_bone_name

        bpy.ops.object.mode_set(mode='POSE')
        self.report({'INFO'}, "Bones renamed")
        return {'FINISHED'}


classes = [
    SSS_BonePropertyGroup,
    SSS_BoneMapProperties,
    SSS_OT_AutofillBoneNames,
    SSS_OT_RenameBones
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.sss_bone_map = PointerProperty(type=SSS_BoneMapProperties)

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
