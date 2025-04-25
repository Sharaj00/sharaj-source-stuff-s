import bpy
import os

class ProportionTrick(bpy.types.Operator):
    bl_idname = "object.proportion_trick"
    bl_label = "Proportion trick"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        armature_found = False
        armature = None

        for obj in selected_objects:
            if obj.type == 'ARMATURE':
                obj.name = "gg"
                armature_found = True
                armature = obj
                break

        if not armature_found:
            self.report({'ERROR'}, "No armature selected!")
            return {'CANCELLED'}

        addon_path = os.path.dirname(__file__)
        blend_file_path = os.path.join(addon_path, "proportion_trick.blend")

        with bpy.data.libraries.load(blend_file_path, link=False) as (data_from, data_to):
            data_to.collections = data_from.collections

        imported_objects = []
        for collection in data_to.collections:
            if collection is not None:
                bpy.context.scene.collection.children.link(collection)
                imported_objects.extend(collection.objects)

        for obj in imported_objects:
            obj.select_set(False)

        script_path = os.path.join(addon_path, "proportion_trick1.py")

        with open(script_path, 'r') as file:
            script_content = file.read()
            exec(script_content)

        if context.window_manager.is_male:
            reference_name = "reference_female"
        else:
            reference_name = "reference_male"
        
        for obj in imported_objects:
            if obj.type == 'ARMATURE' and obj.name == reference_name:
                bpy.data.objects.remove(obj, do_unlink=True)

        if reference_name == "reference_female":
            for obj in bpy.data.objects:
                if obj.name == 'reference_male':
                    obj.hide_set(True)
        elif reference_name == "reference_male":
            for obj in bpy.data.objects:
                if obj.name == 'reference_female':
                    obj.hide_set(True)

        context.window_manager.script_executed = True
        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Press Continue if all looks good, or Cancel to undo."))
        return {'FINISHED'}

class ContinueOperator(bpy.types.Operator):
    bl_idname = "object.continue"
    bl_label = "Continue"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        armature = None
        for obj in selected_objects:
            if obj.type == 'ARMATURE':
                armature = obj
                break

        if armature is None:
            self.report({'ERROR'}, "No armature selected!")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.armature_apply()
        bpy.ops.object.mode_set(mode='OBJECT')

        for bone in armature.pose.bones:
            for constraint in bone.constraints:
                bone.constraints.remove(constraint)

        script_dir = os.path.dirname(__file__)
        script_path = os.path.join(script_dir, "proportion_trick2.py")

        exec(compile(open(script_path).read(), script_path, 'exec'))

        gg_armature = None
        proportions_obj = None
        for obj in bpy.data.objects:
            if obj.name == "gg" and obj.type == 'ARMATURE':
                gg_armature = obj
            elif obj.name == "proportions":
                proportions_obj = obj

        if gg_armature and proportions_obj:
            for child in gg_armature.children:
                child.parent = proportions_obj

        if gg_armature:
            bpy.data.objects.remove(gg_armature, do_unlink=True)

        if context.window_manager.is_male:
            reference_name = "reference_female"
        else:
            reference_name = "reference_male"

        if reference_name == "reference_female":
            for obj in bpy.data.objects:
                if obj.name == 'reference_male':
                    obj.hide_set(False)
        elif reference_name == "reference_male":
            for obj in bpy.data.objects:
                if obj.name == 'reference_female':
                    obj.hide_set(False)

        context.window_manager.script_executed = False

        bpy.context.window_manager.popup_menu(lambda self, context: self.layout.label(text="Proportion trick executed successfully! You can now export reference armature animation."))
        return {'FINISHED'}

class CancelOperator(bpy.types.Operator):
    bl_idname = "object.cancel"
    bl_label = "Cancel"

    def execute(self, context):
        bpy.ops.ed.undo()
        context.window_manager.script_executed = False
        return {'FINISHED'}