from PyQt5.QtWidgets import QStackedWidget

from melid.base.widget import Widget


class RouterView(Widget):
    def __init__(self, routes, *args, **kwargs):
        super(RouterView, self).__init__(*args, **kwargs)

        # configure router

        self.router = QStackedWidget()
        self.addWidget(self.router)

        # add routes

        self.addRoute(*routes)

        if any(routes):
            self.setCurrentIndex(1)

    def setCurrentIndex(self, index):
        self.router.setCurrentIndex(index)

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
            self.router.addWidget(route["view"])


class Router(Widget):
    def navigate(self, name):
        pass
