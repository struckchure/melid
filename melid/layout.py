import enum
import typing

from PyQt5 import QtCore, QtWidgets

from melid.utils import Size
from melid.widgets import Widget


class Direction(enum.Enum):
    COLUMN = QtWidgets.QBoxLayout.TopToBottom
    COLUMN_REVERSE = QtWidgets.QBoxLayout.BottomToTop
    ROW = QtWidgets.QBoxLayout.LeftToRight
    ROW_REVERSE = QtWidgets.QBoxLayout.RightToLeft


class Box(Widget):
    def __init__(
        self,
        child: typing.Optional[
            typing.Union[QtWidgets.QWidget, typing.List[QtWidgets.QWidget]]
        ] = None,
        direction: typing.Optional[Direction] = Direction.ROW,
        gap: typing.Optional[int] = 0,
        alignment: typing.Optional[
            typing.Union[QtCore.Qt.Alignment, QtCore.Qt.AlignmentFlag]
        ] = QtCore.Qt.AlignmentFlag.AlignTop
        | QtCore.Qt.AlignmentFlag.AlignLeft,
        size: typing.Optional[Size] = Size(minimum_width=100, minimum_height=50),
        style: typing.Optional[str] = "",
    ):
        super().__init__()

        self.setGap(gap).setDirection(direction.value).setStyleSheet(
            """
            QGroupBox {background-color: transparent; border: none; %s}
            """
            % style
        )

        size.apply(self)

        if child:
            if isinstance(child, list) and len(child) > 0:
                self.addWidgets(child, alignment=alignment)

            if isinstance(child, QtWidgets.QWidget):
                self.addWidget(child, alignment=alignment)


class Scroll(Widget):
    def __init__(
        self,
        child: typing.Optional[
            typing.Union[QtWidgets.QWidget, typing.List[QtWidgets.QWidget]]
        ] = None,
        *args,
        **kwargs,
    ):
        super().__init__()

        self.__box = Box(child, *args, **kwargs)

        self.__scroll_area = QtWidgets.QScrollArea()
        self.__scroll_area.setStyleSheet(
            "QScrollArea {background-color: transparent; border: none;}"
        )
        self.__scroll_area.setContentsMargins(0, 0, 0, 0)
        self.__scroll_area.setWidget(self.__box)
        self.__scroll_area.setWidgetResizable(True)

        super().addWidget(self.__scroll_area)

    def onWindowResized(self, size: QtCore.QSize):
        print("w: %d, h: %d" % (size.width(), size.height()))

        # Size(
        #     width=size.width(),
        #     height=size.height(),
        # ).apply(self).apply(
        #     self.__box
        # ).apply(self.__scroll_area)

        # self.update()

    def addWidget(self, *args, **kwargs):
        return self.__box.addWidget(*args, **kwargs)
