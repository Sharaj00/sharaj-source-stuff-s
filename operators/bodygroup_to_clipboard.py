import bpy

def show_popup_message(message):
    def draw_func(self, context):
        layout = self.layout
        for line in message.splitlines():
            layout.label(text=line)

    bpy.context.window_manager.popup_menu(draw_func, title="Script Message")

class BodygroupToClipboardOperator(bpy.types.Operator):
    bl_idname = "object.bodygroup_to_clipboard"  
    bl_label = "Bodygroups to clipboard"

    def execute(self, context):
        result = ""

        selected_mesh_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        
        if not selected_mesh_objects:
            show_popup_message("No Mesh objects selected.")
            return {'CANCELLED'}

        for sel in selected_mesh_objects:
            result += f"""    studio "{sel.name}.dmx"\n"""

        if result:
            bpy.context.window_manager.clipboard = result
            show_popup_message(f"Copied to clipboard:\n{result}")
        else:
            show_popup_message("No Mesh objects selected.")

        return {'FINISHED'}
