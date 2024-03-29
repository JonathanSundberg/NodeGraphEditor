from node_graphics_node import GraphicsNode
from node_content_widget import NodeContentWidget
from node_socket import *
class Node():
    """
        This is the base class for a node inside the scene.
        It has inputs and outputs, title and more.
    """
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        self.scene = scene

        self.title=title
        self.content = NodeContentWidget(self)
        self.grNode = GraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.grNode.title = "yahooo"
        self.socket_spacing = 22

        # Create sockets for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0
        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP, socket_type=item)
            counter  += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
            counter+=1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])


    def getSocketPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.grNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            # start from top
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing


        return [x, y]

    @property
    def pos(self):
        return self.grNode.pos() # QPointF ... pos.x
    def setPos(self, x, y):
        self.grNode.setPos(x,y)

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        for socket in (self.inputs+self.outputs):
            if socket.hasEdge():
                socket.edge.remove()
        self.scene.grScene.removeItem(self.grNode)
        self.grNode = None
        self.scene.removeNode(self)