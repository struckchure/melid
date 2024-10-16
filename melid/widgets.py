import enum
import types
import typing
from dataclasses import dataclass

from PyQt5 import QtCore, QtGui, QtWidgets

from melid.store import StatefulWidget
from melid.types import AppEvents


class Widget(QtWidgets.QGroupBox, StatefulWidget):

    STYLESHEET_PATH = ""
    STYLESHEET_TYPE = "CSS"

    def __init__(
        self,
        qt_window_resized: typing.Optional[QtCore.pyqtBoundSignal] = None,
    ):
        super().__init__()

        # if qt_window_resized:
        #     qt_window_resized.connect(self.onWindowResized)

        self.setObjectName(self.__class__.__name__)
        self.setContentsMargins(0, 0, 0, 0)

        # Apply stylesheets if a valid stylesheet path is provided
        if self.STYLESHEET_PATH:
            with open(self.STYLESHEET_PATH, "r") as stylesheet:
                self.setStyleSheet(
                    "QGroupBox {background-color: transparent; border: none; %s}"
                    % stylesheet.read()
                )

        # Initialize a QBoxLayout (Top to Bottom) for the widget
        self.__layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self)
        self.__layout.setContentsMargins(0, 0, 0, 0)

    def setGap(self, gap: int):
        self.__layout.setSpacing(gap)

        return self

    def setDirection(self, direction: QtWidgets.QBoxLayout.Direction):
        """
        Set the layout direction (e.g., TopToBottom, LeftToRight).
        """
        self.__layout.setDirection(direction)

        return self

    def addWidget(self, widget: QtWidgets.QWidget, *args, **kwargs):
        """
        Add a single widget to the layout.
        """

        kwargs.setdefault("stretch", widget.width())

        self.__layout.addWidget(widget, *args, **kwargs)

        return self

    def addWidgets(self, widgets: typing.List[QtWidgets.QWidget], *args, **kwargs):
        """
        Add multiple widgets progressively using QTimer to avoid freezing the UI.
        """

        def _addNextWidget():
            if len(widgets) > 0:
                # Add the next widget
                self.addWidget(widgets.pop(0), *args, **kwargs)

                QtWidgets.QApplication.processEvents()
            else:
                # Stop the timer once all widgets are added
                timer.stop()

        # Use a QTimer to add widgets progressively
        timer = QtCore.QTimer(self)
        timer.timeout.connect(_addNextWidget)
        timer.start()

        return self

    @QtCore.pyqtSlot(AppEvents.WINDOW_RESIZED.value)
    def onWindowResized(self, size: QtCore.QSize):
        pass

    def updateStyleSheet(self, style: str):
        self.setStyleSheet(self.styleSheet() + "\n%s" % style)


class Label(QtWidgets.QLabel, Widget):
    def __init__(self, text: str, style: str = "", *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)

        self.setObjectName(self.__class__.__name__)

        self.setText(text)
        self.setStyleSheet(style)


class Button(QtWidgets.QPushButton, Widget):
    def __init__(
        self,
        child: typing.Optional[typing.Union[str, QtWidgets.QWidget, QtGui.QIcon]] = "",
        on_click: typing.Optional[types.FunctionType] = None,
        style: typing.Optional[str] = "",
        *args,
        **kwargs,
    ):
        super(Button, self).__init__(*args, **kwargs)

        self.setObjectName(self.__class__.__name__)

        if child:
            if isinstance(child, str):
                self.setText(child)
            if isinstance(child, QtGui.QIcon):
                self.setIcon(child)

        if on_click:
            self.clicked.connect(lambda: on_click())

        self.setStyleSheet(style)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


class InputType(enum.Enum):
    TEXT = "TEXT"
    PASSWORD = "PASSWORD"
    EMAIL = "EMAIL"


class Input(QtWidgets.QLineEdit, Widget):
    def __init__(
        self,
        input_type: typing.Optional[InputType] = InputType.TEXT,
        placeholder: typing.Optional[str] = None,
        on_change: typing.Optional[typing.Callable] = None,
        style: typing.Optional[str] = "",
    ):
        super().__init__()

        if input_type == InputType.PASSWORD:
            self.setEchoMode(QtWidgets.QLineEdit.Password)

        if placeholder:
            self.setPlaceholderText(placeholder)

        if on_change:
            self.textChanged.connect(on_change)

        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(style)


class TextArea(QtWidgets.QTextEdit, Widget):
    def __init__(
        self,
        on_change: typing.Optional[typing.Callable] = None,
        style: typing.Optional[str] = "",
    ):
        super().__init__()

        if on_change:
            self.textChanged.connect(on_change)

        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(style)


@dataclass
class Option:
    label: str
    value: typing.Any


class Select(QtWidgets.QComboBox, Widget):
    def __init__(
        self,
        options: typing.Optional[typing.List[Option]] = None,
        on_change: typing.Optional[typing.Callable] = None,
        style: typing.Optional[str] = "",
    ):
        super().__init__()

        if options:
            self.addItems(list(map(lambda x: x.label, options)))

        if on_change:
            self.activated.connect(lambda idx: on_change(options[idx].value))

        # Set placeholder text for the combo box
        self.setEditable(True)
        self.lineEdit().setPlaceholderText("Select an option...")
        self.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.setEditable(False)  # Disable edit after setting placeholder

        # Set custom background color and styling using CSS
        # self.setStyleSheet(
        #     """
        #         QComboBox {
        #             background-color: #EFEFEF;
        #             border: 1px solid #AFAFAF;
        #             padding: 5px;
        #             border-radius: 5px;
        #         }
        #         QComboBox::drop-down {
        #             subcontrol-origin: padding;
        #             subcontrol-position: top right;
        #             width: 20px;
        #             border-left-width: 1px;
        #             border-left-color: darkgray;
        #             border-left-style: solid; /* Just a single line */
        #             border-top-right-radius: 3px; /* same radius as the QComboBox */
        #             border-bottom-right-radius: 3px;
        #         }
        #         QComboBox::down-arrow {
        #             image: url(icons/down_arrow.png);  /* Custom down-arrow icon */
        #         }
        #         QComboBox QAbstractItemView {
        #             background-color: white;
        #             selection-background-color: lightgray;
        #             selection-color: black;
        #         }
        #     """
        # )
        self.setStyleSheet(
            style
            + """
            Select::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 5px;
                padding: 5px;
            }
            """
        )
