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
from bpy.types import Operator, Context
from bpy.props import BoolProperty


class UFRP_OP_batch(Operator):
    """Set all view layers 'Use for rendering' property"""
    bl_idname = "ufrp.batch"
    bl_label = "Use for rendering batch"
    bl_options = {"REGISTER", "UNDO"}
    state: BoolProperty(
        name="UseForRenderingState", 
        description="Check or uncheck all view layers 'Use for rendering' property"
        ) # type: ignore

    def execute(self, context: Context):
        if self.state == True:
            context.scene.render.use_single_layer = False
        for scene in bpy.data.scenes:
            scene: bpy.types.Scene
            for vl in scene.view_layers:
                vl: bpy.types.ViewLayer
                vl.use = self.state
        return {"FINISHED"}


class UFRP_OP_onlyActive(Operator):
    """Only 'use for rendering' active render layer nodes"""
    bl_idname = "ufrp.only_active"
    bl_label = "Enable only render layers"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context: Context):
        # get layers to use
        scenes_layers = [(node.scene, node.layer) for node in context.scene.node_tree.nodes if node.type == "R_LAYERS" and not node.mute]
        # scenes_layers = [(scene, layer_name) (scene, layer_name)]
        layers_to_use = []
        for scene_layer in scenes_layers:
            scene = scene_layer[0]
            layer_name = scene_layer[1]
            if scene is None:
                continue
            layer = scene.view_layers.get(layer_name, None)
            if layer is None:
                continue
            layers_to_use.append(layer)
        # only activate layers to use
        for scene in bpy.data.scenes:
            scene: bpy.types.Scene
            for vl in scene.view_layers:
                if vl in layers_to_use:
                    vl.use = True
                else:
                    vl.use = False
        return {"FINISHED"}



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
    layout = self.layout
    layout.menu(UFRP_MT_menu.bl_idname)


def register():
    bpy.utils.register_class(UFRP_MT_menu)
    bpy.utils.register_class(UFRP_OP_batch)
    bpy.utils.register_class(UFRP_OP_onlyActive)
    bpy.types.VIEWLAYER_PT_layer.append(draw_operators)
    bpy.types.NODE_MT_editor_menus.append(draw_menu)


def unregister():
    bpy.utils.unregister_class(UFRP_MT_menu)
    bpy.utils.unregister_class(UFRP_OP_batch)
    bpy.utils.unregister_class(UFRP_OP_onlyActive)
    bpy.types.VIEWLAYER_PT_layer.remove(draw_operators)
    bpy.types.NODE_MT_editor_menus.remove(draw_menu)