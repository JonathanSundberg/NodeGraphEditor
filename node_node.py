from node_graphics_node import GraphicsNode

class Node():
    """
        This is the base class for a node inside the scene.
        It has inputs and outputs, title and more.
    """
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title=title

        self.grNode = GraphicsNode(self, self.title)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.grNode.title = "yahooo"
        self.inputs = []
        self.outputs = []

