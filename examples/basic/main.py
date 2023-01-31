from PyQt5 import QtCore
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QPushButton, QVBoxLayout

from melid.base.app import App
from melid.router.view import Router, RouterView


class IndexPage(Router):

    STYLESHEET_TYPE = "CSS"
    TITLE = "Index Page"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = QPushButton("Login")
        self.button.clicked.connect(lambda _: self.navigate("profile"))

        self.group_box_layout = QVBoxLayout()
        self.group_box_layout.setAlignment(QtCore.Qt.AlignCenter)

        # credentials
        self.__username = ""
        self.__password = ""

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.textChanged.connect(
            lambda text: self.onTextChanged(text, self.__username)
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.textChanged.connect(
            lambda text: self.onTextChanged(text, self.__password)
        )
        self.password.setEchoMode(QLineEdit.Password)

        self.group_box_layout.addWidget(self.username)
        self.group_box_layout.addWidget(self.password)
        self.group_box_layout.addWidget(self.button)

        self.group_box = QGroupBox("Welcome to Melid")
        self.group_box.setMaximumWidth(int(self.width() * 0.5))
        self.group_box.setLayout(self.group_box_layout)

        # self.setAlignment(QtCore.Qt.AlignCenter)
        self.addWidget(self.group_box)

    def onTextChanged(self, text, name):
        name = text
        print(self.__username, self.__password)


class ProfilePage(Router):

    TITLE = "Profile Page"

    def __init__(self, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)

        self.button = QPushButton("Page Two")
        self.button.clicked.connect(lambda _: self.navigate("index"))
        self.addWidget(self.button)


class Window(App):

    STYLESHEET_PATH = BASE_DIR.joinpath("examples/basic/style.qss")

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
    window.mount(showMaximized=False)


if __name__ == "__main__":
    main()
