from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class GraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24.0
        self._padding = 4.0
        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        # init title
        self.initTitle()
        self.title = self.node.title

        # init sockets
        self.initSockets()

        # init content
        self.initContent()

        self.initUI()

    def mouseMoveEvent(self, event) -> None:
        super().mouseMoveEvent(event)

        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()

    def initSockets(self):
        pass

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(self.edge_size), int(self.title_height + self.edge_size),
                                 int(self.width - 2 * self.edge_size), int(self.height - 2 * self.edge_size - self.title_height))
        self.grContent.setWidget(self.content)

    def boundingRect(self):
        return QRectF(
            0,
            0,
        self.width,
        self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(self.width - 2 * self._padding)

    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, option, widget) -> None:
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size,
                           self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_size,
                                    self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
