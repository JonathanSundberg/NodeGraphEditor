import math

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_socket import *


EDGE_CP_ROUNDNESS = 100

class GraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        self._color = QColor("#001000")
        self._color_selected = QColor("#00ff00")
        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color_selected)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        self._pen.setWidthF(2.0)
        self._pen_selected.setWidthF(2.0)
        self._pen_dragging.setWidthF(2.0)


        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)

        self.posSource = [0,0]
        self.posDestination = [200,100]


    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x ,y):
        self.posDestination = [x, y]

    def paint(self, painter, option, widget) -> None:
        self.updatePath()

        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def updatePath(self):
        """
        Handles drawing QPainterPath from Point A to B
        """
        raise NotImplemented("This method has to be overriden in a child class")


class GraphicsEdgeDirect(GraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)


class GraphicsEdgeBezier(GraphicsEdge):
    def updatePath(self):
        s = self.posSource
        d = self.posDestination
        dist = (d[0] - s[0] * 0.5)

        controlpoint_x_source = +dist
        controlpoint_x_dest = -dist
        controlpoint_y_source = 0
        controlpoint_y_dest = 0

        starting_socket_pos = self.edge.start_socket.position

        if(s[0] > d[0] and starting_socket_pos is (RIGHT_TOP, RIGHT_BOTTOM)) or (s[0] < d[0] and starting_socket_pos in (LEFT_BOTTOM, LEFT_TOP)):
            controlpoint_x_dest *= -1
            controlpoint_x_source *= -1
            controlpoint_y_dest = ((s[1] - d[1]) / math.fabs(
                (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.001)) * EDGE_CP_ROUNDNESS

            controlpoint_y_source = ((d[1] - s[1]) / math.fabs(
                (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.001)) * EDGE_CP_ROUNDNESS


        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.cubicTo(s[0] + controlpoint_x_source, s[1] +controlpoint_y_source, d[0] + controlpoint_x_dest, d[1] +controlpoint_y_dest
        ,self.posDestination[0], self.posDestination[1])
        self.setPath(path)

