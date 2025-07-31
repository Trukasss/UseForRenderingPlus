bl_info = {
    "name": "Use For Rendering Plus",
    "description": "Quickly check or uncheck view layer's 'Use For Rendering' prop",
    "author": "Lukas Sabaliauskas <lukas_sabaliauskas@hotmail.com>",
    "version": (0, 0, 1),
    "blender": (4, 0, 0),
    # "location": "Object Properties > Relations > Matrix Parent Inverse",
    # "warning": "",
    # "doc_url": "https://extensions.blender.org/add-ons/link-parents/",
    # "tracker_url": "https://github.com/Trukasss/LinkParents",
    # "category": "3D View",
}

import bpy
import importlib
from . import icons
importlib.reload(icons)
from . import op
importlib.reload(op)
from . import ui
importlib.reload(ui)


def register():
    icons.register()
    bpy.utils.register_class(op.UFRP_OP_batch)
    bpy.utils.register_class(op.UFRP_OP_onlyActive)
    bpy.utils.register_class(op.UFRP_OP_SwitchViewLayer)
    bpy.utils.register_class(ui.UFRP_MT_menu)
    bpy.types.VIEWLAYER_PT_layer.append(ui.draw_batch_operators)
    bpy.types.NODE_MT_editor_menus.append(ui.draw_comp_menu)
    bpy.types.NODE_MT_context_menu.append(ui.draw_node_menu)


def unregister():
    bpy.utils.unregister_class(ui.UFRP_MT_menu)
    bpy.utils.unregister_class(op.UFRP_OP_SwitchViewLayer)
    bpy.utils.unregister_class(op.UFRP_OP_onlyActive)
    bpy.utils.unregister_class(op.UFRP_OP_batch)
    bpy.types.VIEWLAYER_PT_layer.remove(ui.draw_batch_operators)
    bpy.types.NODE_MT_editor_menus.remove(ui.draw_comp_menu)
    bpy.types.NODE_MT_context_menu.remove(ui.draw_node_menu)
    icons.unregister()