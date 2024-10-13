import os
import sys
import typing

from PyQt5 import QtCore, QtWidgets

from melid.types import AppEvents
from melid.utils import Size
from melid.widgets import Widget


class App(QtWidgets.QMainWindow):
    __QT_WINDOW_RESIZED = QtCore.pyqtSignal(AppEvents.WINDOW_RESIZED.value)

    def __init__(
        self,
        child: typing.Optional[
            typing.Union[QtWidgets.QWidget, typing.List[QtWidgets.QWidget]]
        ] = None,
        qt_app: typing.Optional[QtWidgets.QApplication] = None,
        name: typing.Optional[str] = "Melid",
        title: typing.Optional[str] = "Melid || Made with ❤ by Struckchure",
        size: typing.Optional[Size] = Size(minimum_width=500, minimum_height=500),
    ):
        super().__init__()

        self.__QT_APP = qt_app
        self.__QT_APP.setApplicationName(name)

        self.__central_widget = Widget(qt_window_resized=self.__QT_WINDOW_RESIZED)
        if child:
            if isinstance(child, list) and len(child) > 0:
                self.__central_widget.addWidgets(child)

            if isinstance(child, QtWidgets.QWidget):
                self.__central_widget.addWidget(child)

        size.apply(self.__central_widget).apply(self)

        self.setWindowTitle(title)
        self.setCentralWidget(self.__central_widget)
        self.setContentsMargins(0, 0, 0, 0)

    def addWidget(self, *args, **kwargs):
        return self.__central_widget.addWidget(*args, **kwargs)

    def center(self):
        cursor_position = QtWidgets.QApplication.desktop().cursor().pos()

        screen = QtWidgets.QApplication.screenAt(cursor_position)
        if not screen:
            screen = QtWidgets.QApplication.primaryScreen()

        if screen:
            screen_geometry = screen.geometry()
            screen_center = screen_geometry.center()

            # BUG: does not work as intended on all screens
            screen_center.setX(int(screen_center.x() - (screen_center.x() * 0.075)))
            screen_center.setY(int(screen_center.y() - (screen_center.y() * 0.5)))

            self.move(screen_center)

        return self

    def resizeEvent(self, a0):
        self.__QT_WINDOW_RESIZED.emit(a0.size())

        super().resizeEvent(a0)

    def showMaximized(self):
        super().showMaximized()

        return self

    def mount(self):
        self.show()

        sys.exit(self.__QT_APP.exec_())


os.environ["QT_MAC_WANTS_LAYER"] = "1"

qt_app = QtWidgets.QApplication(sys.argv)
qt_app.setQuitOnLastWindowClosed(True)


def CreateApp(*args, **kwargs):
    try:
        return App(qt_app=qt_app, *args, **kwargs)
    except Exception as e:
        print(str(e))

        sys.exit(qt_app.exec_())
