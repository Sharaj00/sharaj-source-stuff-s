bl_info = {
    "name": "sharaj source stuff's",
    "author": "sharaj00",
    "version": (1, 3, 1),
    "blender": (4, 00, 0),
    "category": "Object",
    "description": "some tools for work with source models",
}

from . import menu
from . import menu_eyes

def register():
    menu.register()
    menu_eyes.register()

def unregister():
    menu.unregister()
    menu_eyes.unregister()
