from PyQt5.QtWidgets import QPushButton

import context as _

from melid.router.view import Router, RouterView
from melid.base.app import App


class IndexPage(Router):
    def __init__(self, *args, **kwargs):
        super(IndexPage, self).__init__(*args, **kwargs)

        self.button = QPushButton("Index Page")
        self.button.clicked.connect(lambda _: self.navigate("profile"))
        self.addWidget(self.button)


class ProfilePage(Router):
    def __init__(self, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)

        self.button = QPushButton("Profile Page")
        self.button.clicked.connect(lambda _: self.navigate("index"))
        self.addWidget(self.button)


class Window(App):
    def __init__(self):
        super(Window, self).__init__()

        self.router = RouterView(
            routes=[
                {"name": "index", "view": IndexPage},
                {"name": "profile", "view": ProfilePage},
            ]
        )

        self.addWidget(self.router)


def main():
    window = Window()
    window.mount()


if __name__ == "__main__":
    main()
