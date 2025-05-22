import bpy

class DeselectBipedOperator(bpy.types.Operator):
    bl_idname = "object.deselect_biped"
    bl_label = "Deselect Valve.Biped"
    bl_description = "Deselect all bones that involved in Source animations"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        active_object = bpy.context.active_object

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
            'ValveBiped.Bip01_L_Finger42',
            'ValveBiped.forward',
            'ValveBiped.weapon_hand_R',
            'ValveBiped.weapon_hand_L',
            'ValveBiped.weapon_bone',
            'ValveBiped.Bip01_R_Ulna',
            'ValveBiped.Bip01_L_Ulna',
            'ValveBiped.Bip01_L_ForeTwist',
            'ValveBiped.Bip01_R_ForeTwist',
            'ValveBiped.Bip01_L_Elbow',
            'ValveBiped.Bip01_R_Elbow',
            'ValveBiped.Bip01_L_Hand_Twist',
            'ValveBiped.Bip01_R_Hand_Twist'
        ]

        if active_object and active_object.type == 'ARMATURE':
            if active_object.mode == 'EDIT':
                bones = active_object.data.edit_bones
                for bone in bones:
                    if bone.name in bones_to_deselect:
                        bone.select_head = False
                        bone.select_tail = False
                        bone.select = False
            elif active_object.mode == 'POSE':
                if bpy.context.selected_pose_bones:
                    for bone in bpy.context.selected_pose_bones:
                        if bone.name in bones_to_deselect:
                            bone.bone.select = False
            else:
                bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Select some bones in EDIT or POSE mode first."), title="Warning", icon='ERROR')

        return {'FINISHED'}
