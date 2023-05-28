from PyQt5.QtWidgets import *
class NodeContentWidget(QWidget):
    """
        Holds the content inside the node.
        such as bools, text edits, number inputs etc.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.wdg_label = QLabel("Some title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QTextEdit("foo"))