from PyQt5.QtWidgets import *
class NodeContentWidget(QWidget):
    """
        Holds the content inside the node.
        such as bools, text edits, number inputs etc.
    """
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Some title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(TextEdit("foo"))

    def setEditingFlag(self, value):
        self.node.scene.grScene.views()[0].editing_flag = value

class TextEdit(QTextEdit):

    def focusInEvent(self, event):
        self.parentWidget().setEditingFlag(True)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parentWidget().setEditingFlag(False)
        super().focusOutEvent(event)