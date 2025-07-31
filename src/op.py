import bpy
from bpy.types import Operator, Context, Scene, ViewLayer, CompositorNodeRLayers
from bpy.props import BoolProperty


# def get_render_nodes_layers(active_only=False):



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
            scene: Scene
            for vl in scene.view_layers:
                vl: ViewLayer
                vl.use = self.state
        nodes = [node for node in context.scene.node_tree.nodes if node.type == "R_LAYERS"]
        for node in nodes:
            node: CompositorNodeRLayers
            node.mute = not self.state
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
            scene: Scene
            for vl in scene.view_layers:
                if vl in layers_to_use:
                    vl.use = True
                else:
                    vl.use = False
        return {"FINISHED"}