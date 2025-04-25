import bpy
import os

class GenerateQCOperator(bpy.types.Operator):
    bl_idname = "object.generate_qc_file"
    bl_label = "Generate QC File"
    bl_description = "Generate QC File for the selected collection"

    def execute(self, context):
        # Получаем имя модели (имя коллекции)
        model_name = bpy.context.collection.name + ".mdl"
        relative_path = bpy.context.window_manager.vmt_path
        output_dir = bpy.path.abspath(bpy.context.window_manager.output_path)

        # Начало содержимого QC файла
        qc_content = f'''$modelname "{model_name}"
$staticprop
'''
        # Обрабатываем объекты в коллекции
        for obj in bpy.context.collection.objects:
            if obj.type == 'MESH' and "_phys" not in obj.name:
                qc_content += f'$bodygroup "{obj.name}"\n{{\n'
                qc_content += f'  studio "{obj.name}.smd"\n'
                qc_content += '}\n'

        # Добавляем оставшиеся параметры
        qc_content += '$contents "solid"\n'
        qc_content += f'$cdmaterials "{relative_path}"\n'
        qc_content += '$sequence idle "idle.smd"\n'

        # Генерация пути и запись файла
        qc_file_path = os.path.join(output_dir, model_name.replace(".mdl", ".qc"))
        os.makedirs(output_dir, exist_ok=True)

        with open(qc_file_path, "w") as qc_file:
            qc_file.write(qc_content)

        self.report({'INFO'}, f"QC файл сгенерирован: {qc_file_path}")
        return {'FINISHED'}