from PyQt5.QtWidgets import QApplication, QPushButton
import sys

from context import melid
from melid.base.widget import Widget
from melid.router.view import Router, RouterView


class IndexPage(Router):
    def __init__(self, *args, **kwargs):
        super(IndexPage, self).__init__(*args, **kwargs)

        self.label = QPushButton("Index Page")
        self.label.clicked.connect(lambda _: self.navigate("profile"))
        self.addWidget(self.label)


class ProfilePage(Router):
    def __init__(self, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)

        self.label = QPushButton("Profile Page")
        self.label.clicked.connect(lambda _: self.navigate("index"))
        self.addWidget(self.label)


class App(Widget):
    def __init__(self):
        super(App, self).__init__()

        self.router = RouterView(
            routes=[
                {"name": "index", "view": IndexPage},
                {"name": "profile", "view": ProfilePage},
            ]
        )

        self.addWidget(self.router)


def main():
    app = QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
