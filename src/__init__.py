bl_info = {
    "name": "View Layer Plus",
    "description": "Quickly check or uncheck view layer's 'Use For Rendering' prop",
    "author": "Lukas Sabaliauskas <lukas_sabaliauskas@hotmail.com>",
    "version": (0, 1, 3),
    "blender": (4, 0, 0),
    "doc_url": "https://extensions.blender.org/add-ons/use-for-rendering-plus/",
    "tracker_url": "https://github.com/Trukasss/ViewLayerPlus",
}


is_reloading = "bpy" in locals()

import bpy
from . import icons
from . import op
from . import ui

if is_reloading:
    import importlib
    importlib.reload(icons)
    importlib.reload(op)
    importlib.reload(ui)


def register():
    icons.register()
    bpy.utils.register_class(op.UFRP_OP_batch)
    bpy.utils.register_class(op.UFRP_OP_OnlyUnmuted)
    bpy.utils.register_class(op.UFRP_OP_OnlySelected)
    bpy.utils.register_class(op.UFRP_OP_SwitchViewLayer)
    bpy.utils.register_class(ui.UFRP_MT_menu)
    bpy.types.VIEWLAYER_PT_layer.append(ui.draw_batch_operators)
    bpy.types.NODE_MT_editor_menus.append(ui.draw_comp_menu)
    bpy.types.NODE_MT_context_menu.append(ui.draw_node_menu)


def unregister():
    bpy.utils.unregister_class(ui.UFRP_MT_menu)
    bpy.utils.unregister_class(op.UFRP_OP_SwitchViewLayer)
    bpy.utils.unregister_class(op.UFRP_OP_OnlySelected)
    bpy.utils.unregister_class(op.UFRP_OP_OnlyUnmuted)
    bpy.utils.unregister_class(op.UFRP_OP_batch)
    bpy.types.VIEWLAYER_PT_layer.remove(ui.draw_batch_operators)
    bpy.types.NODE_MT_editor_menus.remove(ui.draw_comp_menu)
    bpy.types.NODE_MT_context_menu.remove(ui.draw_node_menu)
    icons.unregister()