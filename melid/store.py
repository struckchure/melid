import json
import typing

from PyQt5.QtCore import QThreadPool

from melid.utils import Worker


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


class MemoryStore:

    _instance = None
    _STORE_FILE_NAME = "store.json"

    def __init__(self, initialState: dict[str, typing.Any] | None) -> None:
        if initialState:
            self.setState(initialState)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls.args = args
            cls.kwargs = kwargs

        return cls._instance

    @classmethod
    def _getFile(cls, mode="r"):
        try:
            return open(cls._STORE_FILE_NAME, mode)
        except FileNotFoundError:
            open(cls._STORE_FILE_NAME, "a")

            return cls._getFile(mode)

    @classmethod
    def _readFile(cls):
        try:
            return json.load(cls._getFile())
        except json.JSONDecodeError:
            return {}

    @classmethod
    def _writeFile(cls, data: dict):
        try:
            with cls._getFile("w") as file:
                json.dump(data, file, indent=2)
        except json.JSONDecodeError:
            raise ValueError("Problem parsing JSON store data")

    @classmethod
    def _updateFile(cls, data):
        cls._writeFile({**cls._readFile(), **data})

    @classmethod
    def setState(cls, state: dict):
        cls._updateFile(state)

    @property
    def state(self) -> dict:
        return self._readFile()


class StatefulWidget:
    def text(self):
        raise NotImplementedError

    def setText(self, text: str):
        raise NotImplementedError

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
