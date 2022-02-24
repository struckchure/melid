from PyQt5.QtWidgets import QVBoxLayout, QWidget


class Widget(QWidget):

    STYLESHEET_PATH = ""
    STYLESHEET_TYPE = "CSS"

    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)

        # router layout

        self.view_layout = QVBoxLayout()
        self.view_layout.setSpacing(0)
        self.view_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.view_layout)

    def addWidget(self, *args, **kwargs):
        self.view_layout.addWidget(*args, **kwargs)

    def addLayout(self, *args, **kwargs):
        self.view_layout.addLayout(*args, **kwargs)
