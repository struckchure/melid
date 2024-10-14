import typing

from PyQt5 import QtCore


class Store:

    _instance = None
    _INITIAL_STATE: dict

    def __init__(self, initialState: dict[str, typing.Any] | None) -> None:
        if initialState:
            self._INITIAL_STATE = initialState

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.args = args
            cls.kwargs = kwargs

        return cls._instance

    def setState(self, state: dict):
        self._INITIAL_STATE = {**self.state, **state}

    @property
    def state(self) -> dict:
        return self._INITIAL_STATE


class State(QtCore.QObject):
    __value: typing.Any

    updated = QtCore.pyqtSignal(object)

    def __init__(self, value: typing.Any):
        super().__init__()

        self.__value = value

    def get(self):
        return self.__value

    def set(self, value):
        if self.__value != value:
            self.__value = value
            self.updated.emit(self.__value)

    def subscribe(self, callback: typing.Callable[[typing.Any], None]):
        self.updated.connect(callback)
