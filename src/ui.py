import bpy
from bpy.types import Operator, Context

from .op import UFRP_OP_batch, UFRP_OP_onlyActive


class UFRP_MT_menu(bpy.types.Menu):
    bl_label = "View Layers"
    bl_idname = "UFRP_MT_menu"

    def draw(self, context):
        layout = self.layout
        op_on = layout.operator(UFRP_OP_batch.bl_idname, text="Enable all")
        op_on.state = True
        op_off = layout.operator(UFRP_OP_batch.bl_idname, text="Disable all")
        op_off.state = False
        op_off.state = False
        layout.operator(UFRP_OP_onlyActive.bl_idname)


def draw_operators(self: Operator, context: Context):
    layout = self.layout
    op_on = layout.operator(UFRP_OP_batch.bl_idname, text="Enable all")
    op_on.state = True
    op_off = layout.operator(UFRP_OP_batch.bl_idname, text="Disable all")
    op_off.state = False


def draw_menu(self: Operator, context: Context):
    space = context.space_data
    if space.type == "NODE_EDITOR" and space.tree_type == "CompositorNodeTree":
        layout = self.layout
        layout.menu(UFRP_MT_menu.bl_idname)