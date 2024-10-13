import enum

from PyQt5 import QtCore


class AppEvents(enum.Enum):
    WINDOW_RESIZED = QtCore.QSize
