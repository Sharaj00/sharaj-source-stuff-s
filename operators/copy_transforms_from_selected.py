import bpy

class CopyTransformsFromSelectedOperator(bpy.types.Operator):
    bl_idname = "object.copy_transforms_from_selected"
    bl_label = "Copy Transforms Between Armatures"
    bl_description = "Copy transforms from source armature to target armature"

    def execute(self, context):
        wm = context.window_manager
        source = wm.sss_source_armature
        target = wm.sss_target_armature

        if not source or not target:
            self.report({'ERROR'}, "Both source and target armatures must be set")
            return {'CANCELLED'}
        if source == target:
            self.report({'ERROR'}, "Source and target must be different")
            return {'CANCELLED'}
        if source.type != 'ARMATURE' or target.type != 'ARMATURE':
            self.report({'ERROR'}, "Both objects must be armatures")
            return {'CANCELLED'}

        bpy.context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='POSE')

        for bone in target.pose.bones:
            if bone.name in source.pose.bones:
                constraint = bone.constraints.get("Copy Transforms") or bone.constraints.new('COPY_TRANSFORMS')
                constraint.name = "Copy Transforms"
                constraint.target = source
                constraint.subtarget = bone.name

        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, "Copy Transforms constraints added.")
        return {'FINISHED'}
