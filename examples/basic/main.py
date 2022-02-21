from PyQt5.QtWidgets import QApplication, QLabel
import sys

from context import melid
from melid.base.widget import Widget
from melid.router.view import Router, RouterView


class IndexPage(Router):
    def __init__(self, *args, **kwargs):
        super(IndexPage).__init__(*args, **kwargs)

        self.addWidget(QLabel("Index Page"))


class ProfilePage(Router):
    def __init__(self, *args, **kwargs):
        super(ProfilePage).__init__(*args, **kwargs)

        self.addWidget(QLabel("Profile Page"))


class App(Widget):
    def __init__(self):
        super(App, self).__init__()

        self.router = RouterView(
            routes=[
                {"name": "index", "view": IndexPage()},
                {"name": "profile", "view": ProfilePage()},
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
