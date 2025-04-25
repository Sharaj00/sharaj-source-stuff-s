import bpy

class BoneAdjustOperator(bpy.types.Operator):
    bl_idname = "object.bone_adjust_operator"
    bl_label = "Fix jigglebones"
    bl_description = "Point selected bones in -X direction and rotates the bone to -Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selection = bpy.context.selected_bones
        active_object = bpy.context.active_object
        bone_length = 0.0

        bones_to_deselect = [
            'ValveBiped.Bip01_Pelvis',
            'ValveBiped.Bip01_Spine',
            'ValveBiped.Bip01_Spine1',
            'ValveBiped.Bip01_Spine2',
            'ValveBiped.Bip01_Spine4',
            'ValveBiped.Bip01_Neck1',
            'ValveBiped.Bip01_Head1',
            'ValveBiped.Bip01_R_Thigh',
            'ValveBiped.Bip01_R_Calf',
            'ValveBiped.Bip01_R_Foot',
            'ValveBiped.Bip01_R_Toe0',
            'ValveBiped.Bip01_L_Thigh',
            'ValveBiped.Bip01_L_Calf',
            'ValveBiped.Bip01_L_Foot',
            'ValveBiped.Bip01_L_Toe0',
            'ValveBiped.Bip01_R_Clavicle',
            'ValveBiped.Bip01_R_UpperArm',
            'ValveBiped.Bip01_R_Forearm',
            'ValveBiped.Bip01_R_Hand',
            'ValveBiped.Bip01_R_Finger0',
            'ValveBiped.Bip01_R_Finger01',
            'ValveBiped.Bip01_R_Finger02',
            'ValveBiped.Bip01_R_Finger1',
            'ValveBiped.Bip01_R_Finger11',
            'ValveBiped.Bip01_R_Finger12',
            'ValveBiped.Bip01_R_Finger2',
            'ValveBiped.Bip01_R_Finger21',
            'ValveBiped.Bip01_R_Finger22',
            'ValveBiped.Bip01_R_Finger3',
            'ValveBiped.Bip01_R_Finger31',
            'ValveBiped.Bip01_R_Finger32',
            'ValveBiped.Bip01_R_Finger4',
            'ValveBiped.Bip01_R_Finger41',
            'ValveBiped.Bip01_R_Finger42',
            'ValveBiped.Bip01_L_Clavicle',
            'ValveBiped.Bip01_L_UpperArm',
            'ValveBiped.Bip01_L_Forearm',
            'ValveBiped.Bip01_L_Hand',
            'ValveBiped.Bip01_L_Finger0',
            'ValveBiped.Bip01_L_Finger01',
            'ValveBiped.Bip01_L_Finger02',
            'ValveBiped.Bip01_L_Finger1',
            'ValveBiped.Bip01_L_Finger11',
            'ValveBiped.Bip01_L_Finger12',
            'ValveBiped.Bip01_L_Finger2',
            'ValveBiped.Bip01_L_Finger21',
            'ValveBiped.Bip01_L_Finger22',
            'ValveBiped.Bip01_L_Finger3',
            'ValveBiped.Bip01_L_Finger31',
            'ValveBiped.Bip01_L_Finger32',
            'ValveBiped.Bip01_L_Finger4',
            'ValveBiped.Bip01_L_Finger41',
            'ValveBiped.Bip01_L_Finger42'
        ]

        if active_object and active_object.type == 'ARMATURE' and active_object.mode == 'EDIT':
            if selection:
                if any(bone.name in bones_to_deselect for bone in selection):
                    bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="One of the bones from Valve.Biped is selected. Aborting script execution."), title="Warning", icon='ERROR')
                else:
                    for bone in selection:
                        bone_tail = bone.tail
                        bone_length = (bone_tail - bone.head).length

                    for bone in selection:
                        bone.length = 0

                    for bone in selection:
                        bone.tail.x -= bone_length

                    bpy.ops.object.mode_set(mode='POSE')
                    selected_bones = bpy.context.selected_pose_bones

                    for bone in selected_bones:
                        bpy.ops.object.mode_set(mode='EDIT')
                        bpy.context.object.data.bones.active = bone.bone
                        bpy.ops.armature.calculate_roll(type='GLOBAL_NEG_Z')
                    bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Bone adjustment completed."))
        else:
            bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Select some bones in EDIT or POSE mode first."), title="Warning", icon='ERROR')
        return {'FINISHED'}