import enum
import types
import typing

from PyQt5 import QtCore, QtGui, QtWidgets

from melid.store import State
from melid.types import AppEvents


class Widget(QtWidgets.QGroupBox):

    STYLESHEET_PATH = ""
    STYLESHEET_TYPE = "CSS"

    def __init__(
        self,
        qt_window_resized: typing.Optional[QtCore.pyqtBoundSignal] = None,
    ):
        super().__init__()

        if qt_window_resized:
            qt_window_resized.connect(self.onWindowResized)

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

    def state(
        self,
        state: State,
        condition: typing.Union[bool, typing.Callable[[], bool]] = True,
        attribute: str = None,
        params: typing.Union[typing.List, typing.Dict, typing.Callable] = None,
    ):
        def resolve_params(p):
            if callable(p):
                return resolve_params(p())

            p1 = p if isinstance(p, list) else []
            p2 = p if isinstance(p, dict) else {}

            return p1, p2

        def resolve_condition(c):
            if callable(c):
                return resolve_condition(c())

            return c

        def on_state_change():
            p1, p2 = resolve_params(params)

            if resolve_condition(condition) and attribute and hasattr(self, attribute):
                getattr(self, attribute)(*p1, **p2)

        state.subscribe(on_state_change)

        return self


class Label(QtWidgets.QLabel, Widget):
    def __init__(self, text: str, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)

        self.setText(text)
        self.setObjectName(self.__class__.__name__)


class Button(QtWidgets.QPushButton, Widget):
    def __init__(
        self,
        text: typing.Optional[typing.Union[str, QtWidgets.QWidget]] = "",
        on_click: typing.Optional[types.FunctionType] = None,
        style: typing.Optional[str] = "",
        *args,
        **kwargs,
    ):
        super(Button, self).__init__(*args, **kwargs)

        if isinstance(text, str):
            self.setText(text)

        if on_click:
            self.clicked.connect(lambda: on_click())

        self.setObjectName(self.__class__.__name__)
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
        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
            )
        )
