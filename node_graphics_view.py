from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
class GraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)
        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing| QPainter.HighQualityAntialiasing|QPainter.TextAntialiasing|QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPressed(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPressed(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPressed(event)

        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonReleased(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonReleased(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonReleased(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPressed(self, event):
        # fake release event
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # fake left mouse click, even though we are holding middle mouse
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons()| Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonReleased(self, event):
        # Faking left mouse button release when middle mouse button is released
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons()| Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonReleased(self, event):
        return super().mouseReleaseEvent(event)
    def leftMouseButtonPressed(self, event):
        return super().mousePressEvent(event)
    def rightMouseButtonReleased(self, event):
        return super().mouseReleaseEvent(event)
    def rightMouseButtonPressed(self, event):
        return super().mousePressEvent(event)


    def wheelEvent(self, event: QWheelEvent) -> None:
        # Calculate our zoom factor
        zoomOutFactor = 1/self.zoomInFactor

        # Calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True
        # Set the scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

