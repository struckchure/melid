import typing

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from melid.utils import Worker


class Widget(QWidget):

    STYLESHEET_PATH = ""
    STYLESHEET_TYPE = "CSS"

    TITLE = "Melid View"
    MIN_WIDTH = 500
    MIN_HEIGHT = 500

    OBJECT_NAME = "widget"

    def __init__(self, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)

        # call initializations
        self.initWindow()
        self.initStylesheet()

        # router layout

        self.view_layout = QVBoxLayout()
        self.view_layout.setSpacing(0)
        self.view_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.view_layout)

    def initWindow(self):
        self.setWindowTitle(self.TITLE)
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setObjectName(self.OBJECT_NAME)

    def initStylesheet(self):
        if self.STYLESHEET_PATH:
            with open(self.STYLESHEET_PATH, "r") as stylesheet:
                self.setStyleSheet(stylesheet.read())

    def setAlignment(self, *args, **kwargs):
        self.view_layout.setAlignment(*args, **kwargs)

    def addWidget(self, *args, **kwargs):
        self.view_layout.addWidget(*args, **kwargs)

    def addLayout(self, *args, **kwargs):
        self.view_layout.addLayout(*args, **kwargs)


class Text(QLabel):
    def __init__(self, text: str | typing.Callable, *args, **kwargs):
        super(Text, self).__init__(*args, **kwargs)

        self.setText(text)
        self.remountWidget(text)

    def updateWidgetData(self, text: str | typing.Callable):
        try:
            while True:
                new_text = self.resolveTextValue(text)
                if self.text() != new_text:
                    self.setText(new_text)
        except RuntimeError as e:
            """
            TODO: fix object been deleted while thread is still running
            """

    def remountWidget(self, text: typing.Any | None = None):
        self.threadpool = QThreadPool()

        if text:
            worker = Worker(self.updateWidgetData, text)
            self.threadpool.start(worker)

    def resolveTextValue(self, text: str | typing.Callable):
        if isinstance(text, typing.Callable):
            return str(text())
        elif isinstance(text, (str, int)):
            return str(text)

    def setText(self, text: str | typing.Callable) -> None:
        super().setText(self.resolveTextValue(text))


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
