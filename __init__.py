bl_info = {
    "name": "sharaj source stuff's",
    "author": "sharaj00",
    "version": (1, 6, 2),
    "blender": (4, 50, 0),
    "category": "Object",
    "description": "some tools for working with source models",
}

from . import menu_bones
from . import menu_materials
from . import menu_qc
from . import menu_pt
from . import menu_eyes
from . import menu_bonerenamer

def register():
    menu_pt.register()
    menu_eyes.register()
    menu_bones.register()
    menu_materials.register()
    menu_qc.register()
    menu_bonerenamer.register()

def unregister():
    menu_pt.unregister()
    menu_eyes.unregister()
    menu_bones.unregister()
    menu_materials.unregister()
    menu_qc.unregister()
    menu_bonerenamer.unregister()

