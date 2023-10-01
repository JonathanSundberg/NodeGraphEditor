from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from node_graphics_scene import GraphicsScene
from node_graphics_view import GraphicsView
from node_scene import Scene
from node_node import Node
from node_edge import Edge, EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER


class NodeEditorWnd(QWidget):
    """
        This is the main window.
        It controls window titles, geometry, layouts and is the main parent for all child scene and nodes.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stylesheet_filename = "qss/nodestyle.qss"
        self.loadStylesheet(self.stylesheet_filename)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.scene = Scene()
        self.addNodes()

        # Create graphics scene
        # self.grScene = self.scene.grScene

        # create graphics view
        self.view = GraphicsView(self.scene.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")

        self.show()

        # self.addDebugContent()

    def addNodes(self):
        node1 = Node(self.scene, "test node 1", inputs=[0, 1, 2, 3, 4, 5], outputs=[1])
        node2 = Node(self.scene, "test node 2", inputs=[0, 1, 2, 3, 4, 5], outputs=[1])
        node3 = Node(self.scene, "test node 3", inputs=[0, 1, 2, 3, 4, 5], outputs=[1])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200, -150)

        edge1 = Edge(self.scene, node1.outputs[0], node2.inputs[0], edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0], node3.inputs[2], edge_type=EDGE_TYPE_BEZIER)

    def addDebugContent(self):
        """
        Debug content in the QGraphicScene, proof that widgets work in the scene
        :return:
        """
        self.grScene = self.scene.grScene
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)
        rect = self.grScene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("This is my text")
        text.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 0.7, 0.1))

        widget1 = QPushButton("Hello world")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setFlags(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0, 30)

        widget2 = QTextEdit()
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setPos(0, -200)

        line = self.grScene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def loadStylesheet(self, filename):
        print("STYLE loading: ", filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))
