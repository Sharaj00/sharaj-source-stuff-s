import bpy
import os

class GenerateJigglebonesSet1Operator(bpy.types.Operator):
    bl_idname = "object.generate_jigglebones_set1"
    bl_label = "Generate Jigglebones Set 1"
    bl_description = "Generate pitch-limited jigglebones set"

    def execute(self, context):
        return self.generate_jigglebones(context, "bone limited.qci", self.get_template())

    def get_template(self):
        return """$jigglebone "{bone_name}"
{{
    is_flexible
    {{
        length 20
        tip_mass 0
        
        pitch_constraint -10 1
        pitch_stiffness 50
        pitch_damping 6
        pitch_friction 0
        pitch_bounce 0
        
        yaw_constraint -10 10
        yaw_stiffness 50
        yaw_damping 6
        yaw_friction 0
        yaw_bounce 0
        
        along_stiffness 100
        along_damping 0
        angle_constraint 20
    }}
}}
"""

    def generate_jigglebones(self, context, filename, template):
        return generate_qci(context, filename, template)


class GenerateJigglebonesSet2Operator(bpy.types.Operator):
    bl_idname = "object.generate_jigglebones_set2"
    bl_label = "Generate Jigglebones Set 2"
    bl_description = "Generate unlimited jigglebones set"

    def execute(self, context):
        return self.generate_jigglebones(context, "bone.qci", self.get_template())

    def get_template(self):
        return """$jigglebone "{bone_name}"
{{
    is_flexible
    {{
        length 20
        tip_mass 0
        
        pitch_constraint -20 20
        pitch_stiffness 50
        pitch_damping 6
        pitch_friction 0
        pitch_bounce 0
        
        yaw_constraint -20 20
        yaw_stiffness 50
        yaw_damping 6
        yaw_friction 0
        yaw_bounce 0
        
        along_stiffness 100
        along_damping 0
        angle_constraint 20
    }}
}}
"""

    def generate_jigglebones(self, context, filename, template):
        return generate_qci(context, filename, template)


class GenerateJigglebonesToClipboardOperator(bpy.types.Operator):
    """
    Класс для копирования сгенерированных jigglebones в буфер обмена
    """
    bl_idname = "object.generate_jigglebones_clipboard"
    bl_label = "Copy Jigglebones"
    bl_description = "Generate and copy jigglebones to clipboard"

    mode: bpy.props.StringProperty()

    def execute(self, context):
        template = self.get_template()
        active_object = context.active_object

        if active_object and active_object.type == 'ARMATURE' and active_object.mode in {'POSE', 'EDIT'}:
            if active_object.mode == 'POSE':
                selected_bones = context.selected_pose_bones
            else:
                selected_bones = context.selected_editable_bones

            if not selected_bones:
                self.report({'WARNING'}, "Select some bones in EDIT or POSE mode first.")
                return {'CANCELLED'}

            result = "".join([template.format(bone_name=sel.name) for sel in selected_bones])
            context.window_manager.clipboard = result  # Используем встроенный буфер обмена Blender
            self.report({'INFO'}, "Jigglebones copied to clipboard")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No bones selected or invalid mode.")
            return {'CANCELLED'}

    def get_template(self):
        if self.mode == "limited":
            return """$jigglebone \"{bone_name}\"\n{{\n    is_flexible\n    {{\n        length 20\n        tip_mass 0\n        pitch_constraint -10 1\n        pitch_stiffness 50\n        pitch_damping 6\n        yaw_constraint -10 10\n        yaw_stiffness 50\n        yaw_damping 6\n        along_stiffness 100\n        along_damping 0\n        angle_constraint 20\n    }}\n}}\n"""
        else:
            return """$jigglebone \"{bone_name}\"\n{{\n    is_flexible\n    {{\n        length 20\n        tip_mass 0\n        pitch_constraint -20 20\n        pitch_stiffness 50\n        pitch_damping 6\n        yaw_constraint -20 20\n        yaw_stiffness 50\n        yaw_damping 6\n        along_stiffness 100\n        along_damping 0\n        angle_constraint 20\n    }}\n}}\n"""



def generate_qci(context, filename, template):
    active_object = context.active_object
    if active_object and active_object.type == 'ARMATURE' and active_object.mode in {'POSE', 'EDIT'}:
        if active_object.mode == 'POSE':
            selected_bones = context.selected_pose_bones
        else:
            selected_bones = context.selected_editable_bones

        if not selected_bones:
            bpy.context.window_manager.popup_menu(
                lambda self, context: self.layout.label(text="Select some bones in EDIT or POSE mode first."),
                title="Warning", icon='ERROR'
            )
            return {'CANCELLED'}

        result = ""
        for sel in selected_bones:
            result += template.format(bone_name=sel.name)

        output_path = bpy.path.abspath("//")
        full_path = os.path.join(output_path, filename)
        with open(full_path, "w") as file:
            file.write(result)

        bpy.context.window_manager.popup_menu(
            lambda self, context: self.layout.label(text=f"File '{filename}' created at {output_path}"),
            title="Info", icon='INFO'
        )
        return {'FINISHED'}
    else:
        bpy.context.window_manager.popup_menu(
            lambda self, context: self.layout.label(text="No bones selected or invalid mode."),
            title="Error", icon='ERROR'
        )
        return {'CANCELLED'}
