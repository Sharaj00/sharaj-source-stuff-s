BONE_STANDARDS = [
    ('VALVEBIPED', 'ValveBiped', ''),
    ('VRM', 'VRM', ''),
    ('RIGIFY', 'Rigify', ''),
    ('SFM', 'SFM', ''),
    ('MMD_ENGLISH', 'MMD English', ''),
    ('XNA_LARA', 'XNA Lara', ''),
    ('DAZ_POSER', 'DAZ Poser', ''),
    ('BLENDER_RIGIFY', 'Blender Rigify', ''),
    ('SIMS_2', 'Sims 2', ''),
    ('MOTION_BUILDER', 'Motion Builder', ''),
    ('3DS_MAX', '3DS Max', ''),
    ('TYPE_X', 'Type X', ''),
    ('BEPU', 'Bepu', '')
]

VALVEBIPED_MAP = {
    'Pelvis': 'ValveBiped.Bip01_Pelvis',
    'Spine1': 'ValveBiped.Bip01_Spine',
    'Spine2': 'ValveBiped.Bip01_Spine1',
    'Spine3': 'ValveBiped.Bip01_Spine2',
    'Spine4': 'ValveBiped.Bip01_Spine4',
    'Neck': 'ValveBiped.Bip01_Neck1',
    'Head': 'ValveBiped.Bip01_Head1',
    
    'Clavicle': {
        'left': 'ValveBiped.Bip01_L_Clavicle',
        'right': 'ValveBiped.Bip01_R_Clavicle'
    },
    'UpperArm': {
        'left': 'ValveBiped.Bip01_L_UpperArm',
        'right': 'ValveBiped.Bip01_R_UpperArm'
    },
    'LowerArm': {
        'left': 'ValveBiped.Bip01_L_Forearm',
        'right': 'ValveBiped.Bip01_R_Forearm'
    },
    'Hand': {
        'left': 'ValveBiped.Bip01_L_Hand',
        'right': 'ValveBiped.Bip01_R_Hand'
    },
    'Thumb1': {
        'left': 'ValveBiped.Bip01_L_Finger0',
        'right': 'ValveBiped.Bip01_R_Finger0'
    },
    'Thumb2': {
        'left': 'ValveBiped.Bip01_L_Finger01',
        'right': 'ValveBiped.Bip01_R_Finger01'
    },
    'Thumb3': {
        'left': 'ValveBiped.Bip01_L_Finger02',
        'right': 'ValveBiped.Bip01_R_Finger02'
    },
    'Index1': {
        'left': 'ValveBiped.Bip01_L_Finger1',
        'right': 'ValveBiped.Bip01_R_Finger1'
    },
    'Index2': {
        'left': 'ValveBiped.Bip01_L_Finger11',
        'right': 'ValveBiped.Bip01_R_Finger11'
    },
    'Index3': {
        'left': 'ValveBiped.Bip01_L_Finger12',
        'right': 'ValveBiped.Bip01_R_Finger12'
    },
    'Middle1': {
        'left': 'ValveBiped.Bip01_L_Finger2',
        'right': 'ValveBiped.Bip01_R_Finger2'
    },
    'Middle2': {
        'left': 'ValveBiped.Bip01_L_Finger21',
        'right': 'ValveBiped.Bip01_R_Finger21'
    },
    'Middle3': {
        'left': 'ValveBiped.Bip01_L_Finger22',
        'right': 'ValveBiped.Bip01_R_Finger22'
    },
    'Ring1': {
        'left': 'ValveBiped.Bip01_L_Finger3',
        'right': 'ValveBiped.Bip01_R_Finger3'
    },
    'Ring2': {
        'left': 'ValveBiped.Bip01_L_Finger31',
        'right': 'ValveBiped.Bip01_R_Finger31'
    },
    'Ring3': {
        'left': 'ValveBiped.Bip01_L_Finger32',
        'right': 'ValveBiped.Bip01_R_Finger32'
    },
    'Little1': {
        'left': 'ValveBiped.Bip01_L_Finger4',
        'right': 'ValveBiped.Bip01_R_Finger4'
    },
    'Little2': {
        'left': 'ValveBiped.Bip01_L_Finger41',
        'right': 'ValveBiped.Bip01_R_Finger41'
    },
    'Little3': {
        'left': 'ValveBiped.Bip01_L_Finger42',
        'right': 'ValveBiped.Bip01_R_Finger42'
    },
    'Thigh': {
        'left': 'ValveBiped.Bip01_L_Thigh',
        'right': 'ValveBiped.Bip01_R_Thigh'
    },
    'Calf': {
        'left': 'ValveBiped.Bip01_L_Calf',
        'right': 'ValveBiped.Bip01_R_Calf'
    },
    'Foot': {
        'left': 'ValveBiped.Bip01_L_Foot',
        'right': 'ValveBiped.Bip01_R_Foot'
    },
    'Toe': {
        'left': 'ValveBiped.Bip01_L_Toe0',
        'right': 'ValveBiped.Bip01_R_Toe0'
    }
}

VRM_MAP = {
    'Pelvis': 'hips',
    'Spine1': 'spine',
    'Spine2': 'none',
    'Spine3': 'chest',
    'Spine4': 'none',
    'Neck': 'neck',
    'Head': 'head',
    
    'Clavicle': {
        'left': 'shoulder.L',
        'right': 'shoulder.R'
    },
    'UpperArm': {
        'left': 'upper_arm.L',
        'right': 'upper_arm.R'
    },
    'LowerArm': {
        'left': 'lower_arm.L',
        'right': 'lower_arm.R'
    },
    'Hand': {
        'left': 'hand.L',
        'right': 'hand.R'
    },
    'Thumb1': {
        'left': 'thumb_proximal.L',
        'right': 'thumb_proximal.R'
    },
    'Thumb2': {
        'left': 'thumb_intermediate.L',
        'right': 'thumb_intermediate.R'
    },
    'Thumb3': {
        'left': 'thumb_distal.L',
        'right': 'thumb_distal.R'
    },
    'Index1': {
        'left': 'index_proximal.L',
        'right': 'index_proximal.R'
    },
    'Index2': {
        'left': 'index_intermediate.L',
        'right': 'index_intermediate.R'
    },
    'Index3': {
        'left': 'index_distal.L',
        'right': 'index_distal.R'
    },
    'Middle1': {
        'left': 'middle_proximal.L',
        'right': 'middle_proximal.R'
    },
    'Middle2': {
        'left': 'middle_intermediate.L',
        'right': 'middle_intermediate.R'
    },
    'Middle3': {
        'left': 'middle_distal.L',
        'right': 'middle_distal.R'
    },
    'Ring1': {
        'left': 'ring_proximal.L',
        'right': 'ring_proximal.R'
    },
    'Ring2': {
        'left': 'ring_intermediate.L',
        'right': 'ring_intermediate.R'
    },
    'Ring3': {
        'left': 'ring_distal.L',
        'right': 'ring_distal.R'
    },
    'Little1': {
        'left': 'little_proximal.L',
        'right': 'little_proximal.R'
    },
    'Little2': {
        'left': 'little_intermediate.L',
        'right': 'little_intermediate.R'
    },
    'Little3': {
        'left': 'little_distal.L',
        'right': 'little_distal.R'
    },
    'Thigh': {
        'left': 'upper_leg.L',
        'right': 'upper_leg.R'
    },
    'Calf': {
        'left': 'lower_leg.L',
        'right': 'lower_leg.R'
    },
    'Foot': {
        'left': 'foot.L',
        'right': 'foot.R'
    },
    'Toe': {
        'left': 'toes.L',
        'right': 'toes.R'
    }
}

RIGIFY_MAP = {
    'Pelvis': 'hips',
    'Spine1': 'spine',
    'Spine2': 'spine.001',
    'Spine3': 'spine.002',
    'Spine4': 'spine.003',
    'Neck': 'spine.004',
    'Head': 'spine.006',
    
    'Clavicle': {
        'left': 'shoulder.L',
        'right': 'shoulder.R'
    },
    'UpperArm': {
        'left': 'upper_arm.L',
        'right': 'upper_arm.R'
    },
    'LowerArm': {
        'left': 'forearm.L',
        'right': 'forearm.R'
    },
    'Hand': {
        'left': 'hand.L',
        'right': 'hand.R'
    },
    'Thumb1': {
        'left': 'thumb.01.L',
        'right': 'thumb.01.R'
    },
    'Thumb2': {
        'left': 'thumb.02.L',
        'right': 'thumb.02.R'
    },
    'Thumb3': {
        'left': 'thumb.03.L',
        'right': 'thumb.03.R'
    },
    'Index1': {
        'left': 'f_index.01.L',
        'right': 'f_index.01.R'
    },
    'Index2': {
        'left': 'f_index.02.L',
        'right': 'f_index.02.R'
    },
    'Index3': {
        'left': 'f_index.03.L',
        'right': 'f_index.03.R'
    },
    'Middle1': {
        'left': 'f_middle.01.L',
        'right': 'f_middle.01.R'
    },
    'Middle2': {
        'left': 'f_middle.02.L',
        'right': 'f_middle.02.R'
    },
    'Middle3': {
        'left': 'f_middle.03.L',
        'right': 'f_middle.03.R'
    },
    'Ring1': {
        'left': 'f_ring.01.L',
        'right': 'f_ring.01.R'
    },
    'Ring2': {
        'left': 'f_ring.02.L',
        'right': 'f_ring.02.R'
    },
    'Ring3': {
        'left': 'f_ring.03.L',
        'right': 'f_ring.03.R'
    },
    'Little1': {
        'left': 'f_pinky.01.L',
        'right': 'f_pinky.01.R'
    },
    'Little2': {
        'left': 'f_pinky.02.L',
        'right': 'f_pinky.02.R'
    },
    'Little3': {
        'left': 'f_pinky.03.L',
        'right': 'f_pinky.03.R'
    },
    'Thigh': {
        'left': 'thigh.L',
        'right': 'thigh.R'
    },
    'Calf': {
        'left': 'shin.L',
        'right': 'shin.R'
    },
    'Foot': {
        'left': 'foot.L',
        'right': 'foot.R'
    },
    'Toe': {
        'left': 'toe.L',
        'right': 'toe.R'
    }
}

SFM_MAP = {
    'Pelvis': 'bip_pelvis',
    'Spine1': 'bip_spine_0',
    'Spine2': 'bip_spine_1',
    'Spine3': 'bip_spine_2',
    'Spine4': 'bip_spine_3',
    'Neck': 'bip_neck',
    'Head': 'bip_head',
    
    'Clavicle': {
        'left': 'bip_collar_L',
        'right': 'bip_collar_R'
    },
    'UpperArm': {
        'left': 'bip_upperArm_L',
        'right': 'bip_upperArm_R'
    },
    'LowerArm': {
        'left': 'bip_lowerArm_L',
        'right': 'bip_lowerArm_R'
    },
    'Hand': {
        'left': 'bip_hand_L',
        'right': 'bip_hand_R'
    },
    'Thumb1': {
        'left': 'bip_thumb_0_L',
        'right': 'bip_thumb_0_R'
    },
    'Thumb2': {
        'left': 'bip_thumb_1_L',
        'right': 'bip_thumb_1_R'
    },
    'Thumb3': {
        'left': 'bip_thumb_2_L',
        'right': 'bip_thumb_2_R'
    },
    'Index1': {
        'left': 'bip_index_0_L',
        'right': 'bip_index_0_R'
    },
    'Index2': {
        'left': 'bip_index_1_L',
        'right': 'bip_index_1_R'
    },
    'Index3': {
        'left': 'bip_index_2_L',
        'right': 'bip_index_2_R'
    },
    'Middle1': {
        'left': 'bip_middle_0_L',
        'right': 'bip_middle_0_R'
    },
    'Middle2': {
        'left': 'bip_middle_1_L',
        'right': 'bip_middle_1_R'
    },
    'Middle3': {
        'left': 'bip_middle_2_L',
        'right': 'bip_middle_2_R'
    },
    'Ring1': {
        'left': 'bip_ring_0_L',
        'right': 'bip_ring_0_R'
    },
    'Ring2': {
        'left': 'bip_ring_1_L',
        'right': 'bip_ring_1_R'
    },
    'Ring3': {
        'left': 'bip_ring_2_L',
        'right': 'bip_ring_2_R'
    },
    'Little1': {
        'left': 'bip_pinky_0_L',
        'right': 'bip_pinky_0_R'
    },
    'Little2': {
        'left': 'bip_pinky_1_L',
        'right': 'bip_pinky_1_R'
    },
    'Little3': {
        'left': 'bip_pinky_2_L',
        'right': 'bip_pinky_2_R'
    },
    'Thigh': {
        'left': 'bip_hip_L',
        'right': 'bip_hip_R'
    },
    'Calf': {
        'left': 'bip_knee_L',
        'right': 'bip_knee_R'
    },
    'Foot': {
        'left': 'bip_foot_L',
        'right': 'bip_foot_R'
    },
    'Toe': {
        'left': 'bip_toe_L',
        'right': 'bip_toe_R'
    }
}

MMD_ENGLISH_MAP = {
    'Pelvis': 'lower body',
    'Spine1': 'upper body',
    'Spine2': 'upper body 2',
    'Neck': 'neck',
    'Head': 'head',
    
    'Clavicle': {
        'left': 'shoulder_L',
        'right': 'shoulder_R'
    },
    'UpperArm': {
        'left': 'arm_L',
        'right': 'arm_R'
    },
    'LowerArm': {
        'left': 'elbow_L',
        'right': 'elbow_R'
    },
    'Hand': {
        'left': 'wrist_L',
        'right': 'wrist_R'
    },
    'Thigh': {
        'left': 'leg_L',
        'right': 'leg_R'
    },
    'Calf': {
        'left': 'knee_L',
        'right': 'knee_R'
    },
    'Foot': {
        'left': 'ankle_L',
        'right': 'ankle_R'
    },
    'Toe': {
        'left': 'toe_L',
        'right': 'toe_R'
    },
    'Thumb1': {
        'left': 'thumb0_L',
        'right': 'thumb0_R'
    },
    'Thumb2': {
        'left': 'thumb1_L',
        'right': 'thumb1_R'
    },
    'Thumb3': {
        'left': 'thumb2_L',
        'right': 'thumb2_R'
    },
    'Index1': {
        'left': 'fore1_L',
        'right': 'fore1_R'
    },
    'Index2': {
        'left': 'fore2_L',
        'right': 'fore2_R'
    },
    'Index3': {
        'left': 'fore3_L',
        'right': 'fore3_R'
    },
    'Middle1': {
        'left': 'middle1_L',
        'right': 'middle1_R'
    },
    'Middle2': {
        'left': 'middle2_L',
        'right': 'middle2_R'
    },
    'Middle3': {
        'left': 'middle3_L',
        'right': 'middle3_R'
    },
    'Ring1': {
        'left': 'third1_L',
        'right': 'third1_R'
    },
    'Ring2': {
        'left': 'third2_L',
        'right': 'third2_R'
    },
    'Ring3': {
        'left': 'third3_L',
        'right': 'third3_R'
    },
    'Little1': {
        'left': 'little1_L',
        'right': 'little1_R'
    },
    'Little2': {
        'left': 'little2_L',
        'right': 'little2_R'
    },
    'Little3': {
        'left': 'little3_L',
        'right': 'little3_R'
    }
}

XNA_LARA_MAP = {
    'Pelvis': 'root hips',
    'Spine1': 'spine lower',
    'Spine2': 'spine upper',
    'Neck': 'head neck lower',
    'Head': 'head neck upper',
    
    'Clavicle': {
        'left': 'arm left shoulder 1',
        'right': 'arm right shoulder 1'
    },
    'UpperArm': {
        'left': 'arm left shoulder 2',
        'right': 'arm right shoulder 2'
    },
    'LowerArm': {
        'left': 'arm left elbow',
        'right': 'arm right elbow'
    },
    'Hand': {
        'left': 'arm left wrist',
        'right': 'arm right wrist'
    },
    'Thigh': {
        'left': 'leg left thigh',
        'right': 'leg right thigh'
    },
    'Calf': {
        'left': 'leg left knee',
        'right': 'leg right knee'
    },
    'Foot': {
        'left': 'leg left ankle',
        'right': 'leg right ankle'
    },
    'Toe': {
        'left': 'leg left toes',
        'right': 'leg right toes'
    },
    'Thumb1': {
        'left': 'arm left finger 1a',
        'right': 'arm right finger 1a'
    },
    'Thumb2': {
        'left': 'arm left finger 1b',
        'right': 'arm right finger 1b'
    },
    'Thumb3': {
        'left': 'arm left finger 1c',
        'right': 'arm right finger 1c'
    },
    'Index1': {
        'left': 'arm left finger 2a',
        'right': 'arm right finger 2a'
    },
    'Index2': {
        'left': 'arm left finger 2b',
        'right': 'arm right finger 2b'
    },
    'Index3': {
        'left': 'arm left finger 2c',
        'right': 'arm right finger 2c'
    },
    'Middle1': {
        'left': 'arm left finger 3a',
        'right': 'arm right finger 3a'
    },
    'Middle2': {
        'left': 'arm left finger 3b',
        'right': 'arm right finger 3b'
    },
    'Middle3': {
        'left': 'arm left finger 3c',
        'right': 'arm right finger 3c'
    },
    'Ring1': {
        'left': 'arm left finger 4a',
        'right': 'arm right finger 4a'
    },
    'Ring2': {
        'left': 'arm left finger 4b',
        'right': 'arm right finger 4b'
    },
    'Ring3': {
        'left': 'arm left finger 4c',
        'right': 'arm right finger 4c'
    },
    'Little1': {
        'left': 'arm left finger 5a',
        'right': 'arm right finger 5a'
    },
    'Little2': {
        'left': 'arm left finger 5b',
        'right': 'arm right finger 5b'
    },
    'Little3': {
        'left': 'arm left finger 5c',
        'right': 'arm right finger 5c'
    }
}

DAZ_POSER_MAP = {
    'Pelvis': 'hip',
    'Spine1': 'abdomen',
    'Spine2': 'chest',
    'Neck': 'neck',
    'Head': 'head',
    
    'Clavicle': {
        'left': 'lCollar',
        'right': 'rCollar'
    },
    'UpperArm': {
        'left': 'lShldr',
        'right': 'rShldr'
    },
    'LowerArm': {
        'left': 'lForeArm',
        'right': 'rForeArm'
    },
    'Hand': {
        'left': 'lHand',
        'right': 'rHand'
    },
    'Thigh': {
        'left': 'lThigh',
        'right': 'rThigh'
    },
    'Calf': {
        'left': 'lShin',
        'right': 'rShin'
    },
    'Foot': {
        'left': 'lFoot',
        'right': 'rFoot'
    },
    'Toe': {
        'left': 'lToe',
        'right': 'rToe'
    },
    'Thumb1': {
        'left': 'lThumb1',
        'right': 'rThumb1'
    },
    'Thumb2': {
        'left': 'lThumb2',
        'right': 'rThumb2'
    },
    'Thumb3': {
        'left': 'lThumb3',
        'right': 'rThumb3'
    },
    'Index1': {
        'left': 'lIndex1',
        'right': 'rIndex1'
    },
    'Index2': {
        'left': 'lIndex2',
        'right': 'rIndex2'
    },
    'Index3': {
        'left': 'lIndex3',
        'right': 'rIndex3'
    },
    'Middle1': {
        'left': 'lMid1',
        'right': 'rMid1'
    },
    'Middle2': {
        'left': 'lMid2',
        'right': 'rMid2'
    },
    'Middle3': {
        'left': 'lMid3',
        'right': 'rMid3'
    },
    'Ring1': {
        'left': 'lRing1',
        'right': 'rRing1'
    },
    'Ring2': {
        'left': 'lRing2',
        'right': 'rRing2'
    },
    'Ring3': {
        'left': 'lRing3',
        'right': 'rRing3'
    },
    'Little1': {
        'left': 'lPinky1',
        'right': 'rPinky1'
    },
    'Little2': {
        'left': 'lPinky2',
        'right': 'rPinky2'
    },
    'Little3': {
        'left': 'lPinky3',
        'right': 'rPinky3'
    }
}

# BEPU
BEPU_MAP = {
    'Pelvis': '',
    'Spine1': 'spine',
    'Spine2': 'chest',
    'Neck': 'neck',
    'Head': 'head',
    
    'Clavicle': {
        'left': '',
        'right': ''
    },
    'UpperArm': {
        'left': '',
        'right': ''
    },
    'LowerArm': {
        'left': '',
        'right': ''
    },
    'Hand': {
        'left': '',
        'right': ''
    },
    'Thigh': {
        'left': '',
        'right': ''
    },
    'Calf': {
        'left': '',
        'right': ''
    },
    'Foot': {
        'left': '',
        'right': ''
    },
    'Toe': {
        'left': '',
        'right': ''
    },
    'Thumb1': {
        'left': '',
        'right': ''
    },
    'Thumb2': {
        'left': '',
        'right': ''
    },
    'Thumb3': {
        'left': '',
        'right': ''
    },
    'Index1': {
        'left': '',
        'right': ''
    },
    'Index2': {
        'left': '',
        'right': ''
    },
    'Index3': {
        'left': '',
        'right': ''
    },
    'Middle1': {
        'left': '',
        'right': ''
    },
    'Middle2': {
        'left': '',
        'right': ''
    },
    'Middle3': {
        'left': '',
        'right': ''
    },
    'Ring1': {
        'left': '',
        'right': ''
    },
    'Ring2': {
        'left': '',
        'right': ''
    },
    'Ring3': {
        'left': '',
        'right': ''
    },
    'Little1': {
        'left': '',
        'right': ''
    },
    'Little2': {
        'left': '',
        'right': ''
    },
    'Little3': {
        'left': '',
        'right': ''
    }
}

# TYPE X
TYPE_X_MAP = {
    'Pelvis': '',
    'Spine1': '',
    'Spine2': '',
    'Neck': 'neck',
    'Head': 'head',
    
    'Clavicle': {
        'left': 'shoulder.L',
        'right': 'shoulder.R'
    },
    'UpperArm': {
        'left': 'uparm.L',
        'right': 'uparm.R'
    },
    'LowerArm': {
        'left': 'loarm.L',
        'right': 'loarm.R'
    },
    'Hand': {
        'left': 'finger3-1.L',
        'right': 'finger3-1.R'
    },
    'Thigh': {
        'left': 'upleg.L',
        'right': 'upleg.R'
    },
    'Calf': {
        'left': 'loleg.L',
        'right': 'loleg.R'
    },
    'Foot': {
        'left': 'foot.L',
        'right': 'foot.R'
    },
    'Toe': {
        'left': 'toe1-1.L',
        'right': 'toe1-1.R'
    },
    'Thumb1': {
        'left': 'finger1-2.L',
        'right': 'finger1-2.R'
    },
    'Thumb2': {
        'left': 'finger1-3.L',
        'right': 'finger1-3.R'
    },
    'Thumb3': {
        'left': 'finger1-4.L',
        'right': 'finger1-4.R'
    },
    'Index1': {
        'left': 'finger2-2.L',
        'right': 'finger2-2.R'
    },
    'Index2': {
        'left': 'finger2-3.L',
        'right': 'finger2-3.R'
    },
    'Index3': {
        'left': 'finger2-4.L',
        'right': 'finger2-4.R'
    },
    'Middle1': {
        'left': 'finger3-2.L',
        'right': 'finger3-2.R'
    },
    'Middle2': {
        'left': 'finger3-3.L',
        'right': 'finger3-3.R'
    },
    'Middle3': {
        'left': 'finger3-4.L',
        'right': 'finger3-4.R'
    },
    'Ring1': {
        'left': 'finger4-2.L',
        'right': 'finger4-2.R'
    },
    'Ring2': {
        'left': 'finger4-3.L',
        'right': 'finger4-3.R'
    },
    'Ring3': {
        'left': 'finger4-4.L',
        'right': 'finger4-4.R'
    },
    'Little1': {
        'left': 'finger5-2.L',
        'right': 'finger5-2.R'
    },
    'Little2': {
        'left': 'finger5-3.L',
        'right': 'finger5-3.R'
    },
    'Little3': {
        'left': 'finger5-4.L',
        'right': 'finger5-4.R'
    }
}

# 3DS Max
MAX_3DS_MAP = {
    'Pelvis': 'Hips',
    'Spine1': 'Chest',
    'Spine2': 'Chest3',
    'Neck': 'Neck',
    'Head': 'Head',
    
    'Clavicle': {
        'left': 'LeftCollar',
        'right': 'RightCollar'
    },
    'UpperArm': {
        'left': 'LeftShoulder',
        'right': 'RightShoulder'
    },
    'LowerArm': {
        'left': 'LeftElbow',
        'right': 'RightElbow'
    },
    'Hand': {
        'left': 'LeftWrist',
        'right': 'RightWrist'
    },
    'Thigh': {
        'left': 'LeftHip',
        'right': 'RightHip'
    },
    'Calf': {
        'left': 'LeftKnee',
        'right': 'RightKnee'
    },
    'Foot': {
        'left': 'LeftAnkle',
        'right': 'RightAnkle'
    },
    'Toe': {
        'left': 'LeftToe',
        'right': 'RightToe'
    },
    'Thumb1': {
        'left': 'LeftFinger0',
        'right': 'RightFinger0'
    },
    'Thumb2': {
        'left': 'LeftFinger01',
        'right': 'RightFinger01'
    },
    'Thumb3': {
        'left': 'LeftFinger02',
        'right': 'RightFinger02'
    },
    'Index1': {
        'left': 'LeftFinger1',
        'right': 'RightFinger1'
    },
    'Index2': {
        'left': 'LeftFinger11',
        'right': 'RightFinger11'
    },
    'Index3': {
        'left': 'LeftFinger12',
        'right': 'RightFinger12'
    },
    'Middle1': {
        'left': 'LeftFinger2',
        'right': 'RightFinger2'
    },
    'Middle2': {
        'left': 'LeftFinger21',
        'right': 'RightFinger21'
    },
    'Middle3': {
        'left': 'LeftFinger22',
        'right': 'RightFinger22'
    },
    'Ring1': {
        'left': 'LeftFinger3',
        'right': 'RightFinger3'
    },
    'Ring2': {
        'left': 'LeftFinger31',
        'right': 'RightFinger31'
    },
    'Ring3': {
        'left': 'LeftFinger32',
        'right': 'RightFinger32'
    },
    'Little1': {
        'left': 'LeftFinger4',
        'right': 'RightFinger4'
    },
    'Little2': {
        'left': 'LeftFinger41',
        'right': 'RightFinger41'
    },
    'Little3': {
        'left': 'LeftFinger42',
        'right': 'RightFinger42'
    }
}

# Motion Builder
MOTION_BUILDER_MAP = {
    'Pelvis': 'Hips',
    'Spine1': 'chest',
    'Spine2': 'Spine2',
    'Neck': 'Neck',
    'Head': 'Head',
    
    'Clavicle': {
        'left': 'LeftShoulder',
        'right': 'RightShoulder'
    },
    'UpperArm': {
        'left': 'LeftUpArm',
        'right': 'RightUpArm'
    },
    'LowerArm': {
        'left': 'LeftLowArm',
        'right': 'RightLowArm'
    },
    'Hand': {
        'left': 'LeftHand',
        'right': 'RightHand'
    },
    'Thigh': {
        'left': 'LeftUpLeg',
        'right': 'RightUpLeg'
    },
    'Calf': {
        'left': 'LeftLowLeg',
        'right': 'RightLowLeg'
    },
    'Foot': {
        'left': 'LeftFoot',
        'right': 'RightFoot'
    },
    'Toe': {
        'left': 'LeftToeBase',
        'right': 'RightToeBase'
    },
    'Thumb1': {
        'left': 'LeftHandThumb1',
        'right': 'RightHandThumb1'
    },
    'Thumb2': {
        'left': 'LeftHandThumb2',
        'right': 'RightHandThumb2'
    },
    'Thumb3': {
        'left': 'LeftHandThumb3',
        'right': 'RightHandThumb3'
    },
    'Index1': {
        'left': 'LeftHandIndex1',
        'right': 'RightHandIndex1'
    },
    'Index2': {
        'left': 'LeftHandIndex2',
        'right': 'RightHandIndex2'
    },
    'Index3': {
        'left': 'LeftHandIndex3',
        'right': 'RightHandIndex3'
    },
    'Middle1': {
        'left': 'LeftHandMiddle1',
        'right': 'RightHandMiddle1'
    },
    'Middle2': {
        'left': 'LeftHandMiddle2',
        'right': 'RightHandMiddle2'
    },
    'Middle3': {
        'left': 'LeftHandMiddle3',
        'right': 'RightHandMiddle3'
    },
    'Ring1': {
        'left': 'LeftHandRing1',
        'right': 'RightHandRing1'
    },
    'Ring2': {
        'left': 'LeftHandRing2',
        'right': 'RightHandRing2'
    },
    'Ring3': {
        'left': 'LeftHandRing3',
        'right': 'RightHandRing3'
    },
    'Little1': {
        'left': 'LeftHandPinky1',
        'right': 'RightHandPinky1'
    },
    'Little2': {
        'left': 'LeftHandPinky2',
        'right': 'RightHandPinky2'
    },
    'Little3': {
        'left': 'LeftHandPinky3',
        'right': 'RightHandPinky3'
    }
}

# Sims 2
SIMS_2_MAP = {
    'Pelvis': 'root_rot',
    'Spine1': 'spine0',
    'Spine2': 'spine2',
    'Neck': 'neck',
    'Head': 'head',
    
    'Clavicle': {
        'left': 'l_clavicle',
        'right': 'r_clavicle'
    },
    'UpperArm': {
        'left': 'l_upperarm',
        'right': 'r_upperarm'
    },
    'LowerArm': {
        'left': 'l_forearm',
        'right': 'r_forearm'
    },
    'Hand': {
        'left': 'l_hand',
        'right': 'r_hand'
    },
    'Thigh': {
        'left': 'l_thigh',
        'right': 'r_thigh'
    },
    'Calf': {
        'left': 'l_calf',
        'right': 'r_calf'
    },
    'Foot': {
        'left': 'l_foot',
        'right': 'r_foot'
    },
    'Toe': {
        'left': 'l_toe',
        'right': 'r_toe'
    },
    'Thumb1': {
        'left': 'l_thumb0',
        'right': 'r_thumb0'
    },
    'Thumb2': {
        'left': 'l_thumb1',
        'right': 'r_thumb1'
    },
    'Thumb3': {
        'left': 'l_thumb2',
        'right': 'r_thumb2'
    },
    'Index1': {
        'left': 'l_index0',
        'right': 'r_index0'
    },
    'Index2': {
        'left': 'l_index1',
        'right': 'r_index1'
    },
    'Index3': {
        'left': 'l_index2',
        'right': 'r_index2'
    },
    'Middle1': {
        'left': 'l_mid0',
        'right': 'r_mid0'
    },
    'Middle2': {
        'left': 'l_mid1',
        'right': 'r_mid1'
    },
    'Middle3': {
        'left': 'l_mid2',
        'right': 'r_mid2'
    },
    'Ring1': {
        'left': 'l_ring0',
        'right': 'r_ring0'
    },
    'Ring2': {
        'left': 'l_ring1',
        'right': 'r_ring1'
    },
    'Ring3': {
        'left': 'l_ring2',
        'right': 'r_ring2'
    },
    'Little1': {
        'left': 'l_pinky0',
        'right': 'r_pinky0'
    },
    'Little2': {
        'left': 'l_pinky1',
        'right': 'r_pinky1'
    },
    'Little3': {
        'left': 'l_pinky2',
        'right': 'r_pinky2'
    }
}

BONE_POSITIONS = [
    'Pelvis', 'Spine1', 'Spine2', 'Spine3', 'Spine4', 'Neck', 'Head',
    'Clavicle', 'UpperArm', 'LowerArm', 'Hand',
    'Thumb1', 'Thumb2', 'Thumb3',
    'Index1', 'Index2', 'Index3',
    'Middle1', 'Middle2', 'Middle3',
    'Ring1', 'Ring2', 'Ring3',
    'Little1', 'Little2', 'Little3',
    'Thigh', 'Calf', 'Foot', 'Toe'
]

BONE_STANDARD_MAPS = {
    'VALVEBIPED': VALVEBIPED_MAP,
    'VRM': VRM_MAP,
    'RIGIFY': RIGIFY_MAP,
    'SFM': SFM_MAP,
    'MMD_ENGLISH': MMD_ENGLISH_MAP,
    'XNA_LARA': XNA_LARA_MAP,
    'DAZ_POSER': DAZ_POSER_MAP,
    'SIMS_2': SIMS_2_MAP,
    'MOTION_BUILDER': MOTION_BUILDER_MAP,
    '3DS_MAX': MAX_3DS_MAP,
    'TYPE_X': TYPE_X_MAP,
    'BEPU': BEPU_MAP
}