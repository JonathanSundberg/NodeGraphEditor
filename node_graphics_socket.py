from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class GraphicsSocket(QGraphicsItem):
    def __init__(self, socket, socket_type=1):
        super().__init__(socket.node.grNode)

        self.socket = socket
        self.radius = 6.0
        self.outline_width = 1.0
        self._colors = [QColor("#FFFF7700"),
                        QColor("#FF52ee220"),
                        QColor("#FF0056a6"),
                        QColor("#FFa86db1"),
                        QColor("#FFb54747"),
                        QColor("#FFdbe220")]
        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItemm, widget=None) -> None:

        # painter circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(int(-self.radius), int(-self.radius), int(2*self.radius), int(2*self.radius))

    def boundingRect(self):
        return QRectF(
            -self.radius - self.outline_width,
            -self.radius - self.outline_width,
            2*(self.radius+self.outline_width),
            2 * (self.radius + self.outline_width)
        )

