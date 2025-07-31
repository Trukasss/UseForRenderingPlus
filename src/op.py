import bpy
from bpy.types import Operator, Context, Scene, ViewLayer, CompositorNodeRLayers
from bpy.props import BoolProperty


def get_render_nodes_scene_layer(node: CompositorNodeRLayers):
    if node.type != "R_LAYERS":
        raise ValueError("Active node must be of Render Layer type")
    if node.scene is None:
        return (None, None)
    layer = node.scene.view_layers.get(node.layer, None)
    if layer is None:
        return (node.scene, None)
    return (node.scene, layer)


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
        nb_view_layers = 0
        for scene in bpy.data.scenes:
            scene: Scene
            for vl in scene.view_layers:
                vl: ViewLayer
                vl.use = self.state
                nb_view_layers += 1
        nodes = [node for node in context.scene.node_tree.nodes if node.type == "R_LAYERS"]
        for node in nodes:
            node: CompositorNodeRLayers
            node.mute = not self.state
        if self.state == True:
            self.report({"INFO"}, f"Enabled all {nb_view_layers} view layers for rendering")
        else:
            self.report({"INFO"}, f"Disabled all {nb_view_layers} view layers from rendering")
        return {"FINISHED"}


class UFRP_OP_onlyActive(Operator):
    """Only 'use for rendering' active render layer nodes"""
    bl_idname = "ufrp.only_active"
    bl_label = "Enable only render layers"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context: Context):
        # get layers to use
        render_nodes = [(node.scene, node.layer) for node in context.scene.node_tree.nodes if node.type == "R_LAYERS" and not node.mute]
        # scenes_layers = [(scene, layer_name) (scene, layer_name)]
        layers_to_use = []
        for node in render_nodes:
            scene, layer = get_render_nodes_scene_layer(node)
            if not layer:
                continue
            layers_to_use.append(layer)
        # only activate layers to use
        for scene in bpy.data.scenes:
            scene: Scene
            for vl in scene.view_layers:
                if vl in layers_to_use:
                    vl.use = True
                else:
                    vl.use = False
        self.report({"INFO"}, f"Enable only {len(layers_to_use)} active view layers for rendering")
        return {"FINISHED"}


class UFRP_OP_SwitchViewLayer(Operator):
    """Switch to active render layer node's view layer"""
    bl_idname = "ufrp.switch_view_layer"
    bl_label = "Switch to View Layer"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: Context):
        cls.poll_message_set("Must select a Render Layer Node")
        return (
            context.active_node
            and context.active_node.type == "R_LAYERS")
    
    def execute(self, context: Context):
        node = context.active_node
        if node.type != "R_LAYERS":
            self.report({"ERROR"}, "Active node must be of Render Layer type")
            return {"CANCELLED"}
        scene, layer = get_render_nodes_scene_layer(node)
        if not scene or not layer:
            self.report({"ERROR"}, f"Could not find scene '{scene}' and view layer '{layer}'")
            return {"CANCELLED"}
        context.window.scene = scene
        context.window.view_layer = layer
        self.report({"INFO"}, f"Switched to '{layer.name}' view layer")
        return {"FINISHED"}