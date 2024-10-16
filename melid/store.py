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


class StatefulWidget:
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
