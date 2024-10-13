import typing

from PyQt5 import QtWidgets

from melid.layout import Box


class Route(Box):
    _PATH: str
    _COMPONENT: str

    def __init__(self, path: str, component: QtWidgets.QWidget, **kwargs):
        super().__init__(child=component, **kwargs)

        self._PATH = path
        self._COMPONENT = component

    def navigate(self, path: str):
        Router.navigate(path)


class Router(Box):
    _INSTANCE = None
    _ROUTE_TREE: typing.Dict[str, int] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._INSTANCE:
            cls._INSTANCE = super(Router, cls).__new__(cls, *args, **kwargs)
        return cls._INSTANCE

    def __init__(self, *routes: Route, **kwargs):
        super().__init__(**kwargs)

        self.router = QtWidgets.QStackedWidget()

        self.addWidget(self.router)
        self.addRoute(*routes)

        self.setCurrentIndex(self.router.currentIndex())

    def setCurrentIndex(self, index: int):
        self.router.setCurrentIndex(index)

    def addRoute(self, *routes: Route):
        for idx, route in enumerate(routes):
            self._ROUTE_TREE[route._PATH] = idx
            self.router.addWidget(route._COMPONENT)

    @classmethod
    def navigate(cls, path: str):
        if not cls._INSTANCE:
            raise ValueError("Router has not been initialized")

        idx = cls._ROUTE_TREE.get(path)
        if idx is None:
            raise ValueError("Page not found")

        cls._INSTANCE.setCurrentIndex(idx)
