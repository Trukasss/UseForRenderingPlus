import bpy
from bpy.types import Panel, Context
from bl_ui.space_node import NODE_MT_context_menu

from .op import (
    UFRP_OP_batch, 
    UFRP_OP_OnlyUnmuted,
    UFRP_OP_OnlySelected,
    UFRP_OP_SwitchViewLayer,
)
from . import icons


class UFRP_MT_menu(bpy.types.Menu):
    bl_label = "View Layers"
    bl_idname = "UFRP_MT_menu"

    def draw(self, context: Context):
        layout = self.layout
        op_on = layout.operator(
            UFRP_OP_batch.bl_idname, 
            text="Enable all",
            icon_value = icons.get_addon_id())
        op_on.state = True
        op_off = layout.operator(
            UFRP_OP_batch.bl_idname, 
            text="Disable all",
            icon_value = icons.get_addon_id())
        op_off.state = False
        layout.operator(
            UFRP_OP_OnlyUnmuted.bl_idname,
            icon_value = icons.get_addon_id())
        layout.operator(
            UFRP_OP_SwitchViewLayer.bl_idname,
            icon_value = icons.get_addon_id())
        layout.operator(
            UFRP_OP_OnlySelected.bl_idname,
            icon_value = icons.get_addon_id())


def draw_batch_operators(self: Panel, context: Context):
    layout = self.layout
    op_on = layout.operator(
        UFRP_OP_batch.bl_idname, 
        text="Enable all", 
        icon_value = icons.get_addon_id())
    op_on.state = True
    op_off = layout.operator(
        UFRP_OP_batch.bl_idname, 
        text="Disable all", 
        icon_value = icons.get_addon_id())
    op_off.state = False


def draw_comp_menu(self: Panel, context: Context):
    space = context.space_data
    if space.type == "NODE_EDITOR" and space.tree_type == "CompositorNodeTree":
        layout = self.layout
        layout.menu(UFRP_MT_menu.bl_idname)


def draw_node_menu(self: NODE_MT_context_menu, context: Context):
    if (context.space_data.tree_type == "CompositorNodeTree"
        and context.active_node):
        layout = self.layout
        layout.separator()
        layout.operator(
            UFRP_OP_SwitchViewLayer.bl_idname, 
            icon_value = icons.get_addon_id())
        layout.operator(
            UFRP_OP_OnlySelected.bl_idname, 
            icon_value = icons.get_addon_id())