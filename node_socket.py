from node_graphics_socket import GraphicsSocket

LEFT_TOP=1
LEFT_BOTTOM=2
RIGHT_TOP=3
RIGHT_BOTTOM=4
class Socket():

    def __init__(self, node, index=0, position=LEFT_TOP):
        self.node = node
        self.index=index
        self.position = position
        print(" Socket -- creating with: ", self.index, self.position, "for node: ", self.node)
        self.grSocket = GraphicsSocket(self.node.grNode)

        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None

    def getSocketPosition(self):
        return self.node.getSocketPosition(self.index, self.position)

    def setConnectedEdge(self, edge=None):
        self.edge = edge
