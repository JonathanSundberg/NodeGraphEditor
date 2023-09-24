from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_socket import GraphicsSocket
from node_graphics_edge import GraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER
MODE_NO_OP = 1
MODE_EDGE_DRAG = 2
DEBUG = True
EDGE_DRAG_START_THRESHOLD = 15


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

        self.mode = MODE_NO_OP

    def initUI(self):
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
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
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonReleased(self, event):
        # Faking left mouse button release when middle mouse button is released
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonReleased(self, event):
        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        super().mouseReleaseEvent(event)

    def leftMouseButtonPressed(self, event):
        item = self.getItemAtClick(event)

        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if type(item) is GraphicsSocket:
            if self.mode == MODE_NO_OP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        super().mouseMoveEvent(event)

    def rightMouseButtonReleased(self, event):
        super().mouseReleaseEvent(event)

    def rightMouseButtonPressed(self, event):
        super().mousePressEvent(event)

        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, GraphicsEdge): print("RMB DEBUG: ", item.edge, ' connecting sockets: ',
                                                     item.edge.start_socket, '<-->', item.edge.end_socket)
            if isinstance(item, GraphicsSocket): print("RMB DEBUG: ", item.socket, 'has edge:', item.socket.edge)
            if item is None:
                print("SCENE: ")
                print("    Nodes:")
                for node in self.grScene.scene.nodes: print('        ', node)
                print("    Edges:")
                for edge in self.grScene.scene.edges: print('        ', edge)

    def wheelEvent(self, event: QWheelEvent) -> None:
        # Calculate our zoom factor
        zoomOutFactor = 1 / self.zoomInFactor

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

    def edgeDragEnd(self, item):
        self.mode = MODE_NO_OP
        if type(item) == GraphicsSocket:
            if DEBUG: print("previous edge: ", self.previous_edge)
            if item.socket.hasEdge():
                item.socket.edge.remove()
            if DEBUG: print(" assign end socket: ", item.socket)
            if self.previous_edge:
                self.previous_edge.remove()

            self.dragEdge.start_socket = self.last_start_socket
            self.dragEdge.end_socket = item.socket
            self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
            if DEBUG: print("assigned start & end sockets to Edge")
            self.dragEdge.updatePositions()
            return True

        if DEBUG: print(" END dragging edge")
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG: print(" about to set socket to previous edge: ", self.previous_edge)
        if self.previous_edge:
            self.previous_edge.start_socket.edge = self.previous_edge
        return False


    def edgeDragStart(self, item):
        if DEBUG: print("edgeDragStart starting drag edge")
        if DEBUG: print("    assign start socket to: ", item.socket)
        self.previous_edge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print('dragEdge: ', self.dragEdge)
    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def distanceBetweenClickAndReleaseIsOff(self, event):
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD * EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y()) > edge_drag_threshold_sq