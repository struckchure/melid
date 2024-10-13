import typing

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRunnable, pyqtSlot


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.fn(*self.args, **self.kwargs)


class Size:
    def __init__(
        self,
        width: typing.Optional[int] = None,
        height: typing.Optional[int] = None,
        minimum_width: typing.Optional[int] = 0,
        minimum_height: typing.Optional[int] = 0,
        maximum_width: typing.Optional[int] = QtWidgets.QWIDGETSIZE_MAX,
        maximum_height: typing.Optional[int] = QtWidgets.QWIDGETSIZE_MAX,
    ):
        # Set the fixed size if width and height are provided
        self.fixed_size = QtCore.QSize(width or 0, height or 0)

        # Set minimum and maximum sizes
        self.minimum_size = QtCore.QSize(minimum_width, minimum_height)
        self.maximum_size = QtCore.QSize(maximum_width, maximum_height)

    def size(self) -> QtCore.QSize:
        """
        Returns the right size based on the PyQt5 preference for fixed, min, and max sizes.
        """
        # If a fixed size is set (both width and height)
        if self.fixed_size.width() > 0 and self.fixed_size.height() > 0:
            return self.fixed_size

        # Get the current size hint
        current_size = self.sizeHint()

        # Ensure the current size respects the min and max constraints
        width = max(
            self.minimum_size.width(),
            min(current_size.width(), self.maximum_size.width()),
        )
        height = max(
            self.minimum_size.height(),
            min(current_size.height(), self.maximum_size.height()),
        )

        return QtCore.QSize(width, height)

    def sizePolicy(self) -> QtWidgets.QSizePolicy:
        """
        Returns the appropriate size policies based on the fixed, minimum, and maximum sizes.
        """
        horizontal_policy = QtWidgets.QSizePolicy.Expanding
        vertical_policy = QtWidgets.QSizePolicy.Expanding

        # # Determine horizontal policy
        # if self.fixed_size.width() > 0:
        #     horizontal_policy = QtWidgets.QSizePolicy.Fixed
        # elif self.minimum_size.width() == self.maximum_size.width():
        #     horizontal_policy = QtWidgets.QSizePolicy.Fixed
        # elif self.maximum_size.width() == QtWidgets.QWIDGETSIZE_MAX:
        #     horizontal_policy = QtWidgets.QSizePolicy.Expanding

        # # Determine vertical policy
        # if self.fixed_size.height() > 0:
        #     vertical_policy = QtWidgets.QSizePolicy.Fixed
        # elif self.minimum_size.height() == self.maximum_size.height():
        #     vertical_policy = QtWidgets.QSizePolicy.Fixed
        # elif self.maximum_size.height() == QtWidgets.QWIDGETSIZE_MAX:
        #     vertical_policy = QtWidgets.QSizePolicy.Expanding

        return QtWidgets.QSizePolicy(horizontal_policy, vertical_policy)

    def apply(self, widget: QtWidgets.QWidget):
        widget.setSizePolicy(self.sizePolicy())

        if self.fixed_size.width() > 0:
            widget.setFixedWidth(self.fixed_size.width())

        if self.fixed_size.height() > 0:
            widget.setFixedHeight(self.fixed_size.height())

        if self.minimum_size.width() > 0:
            widget.setMinimumWidth(self.minimum_size.width())

        if self.minimum_size.height() > 0:
            widget.setMinimumHeight(self.minimum_size.height())

        if self.maximum_size.width() > 0:
            widget.setMaximumWidth(self.maximum_size.width())

        if self.maximum_size.height() > 0:
            widget.setMaximumHeight(self.maximum_size.height())

        return self
