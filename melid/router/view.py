from PyQt5.QtWidgets import QStackedWidget

from melid.base.widget import Widget


class RouterView(Widget):
    def __init__(self, routes, *args, **kwargs):
        super(RouterView, self).__init__(*args, **kwargs)

        self.routes = routes

        # configure router

        self.router = QStackedWidget()
        self.addWidget(self.router)

        # add routes

        self.addRoute(*routes)

        self.setCurrentIndex(self.router.currentIndex())

    def setCurrentIndex(self, index):
        self.router.setCurrentIndex(index)

    def addView(self, name, view):
        self.router.addWidget(view())

    def addRoute(self, *routes):
        """
        `view` key must be a `Router` instance
        ```
        addRoute(
            {
                "name": "index",
                "view": IndexPage,
            },
            {
                "name": "profile",
                "view": ProfilePage,
            }
        )
        ```
        """

        for route in routes:
            self.addView(**route)

    def navigate(self, name):
        for index, route in enumerate(self.routes):
            if route["name"] == name:
                self.setCurrentIndex(index)


class Router(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def navigate(self, name):
        self.parent().parent().navigate(name)
