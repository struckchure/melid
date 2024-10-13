import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QLineEdit, QPushButton, QVBoxLayout

from melid.app import App
from melid.router import Router


class IndexPage(Router):

    STYLESHEET_TYPE = "CSS"
    TITLE = "Index Page"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button = QPushButton("Login")
        self.button.clicked.connect(lambda _: self.navigate("profile"))

        self.group_box_layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.group_box_layout.addWidget(self.username)
        self.group_box_layout.addWidget(self.password)
        self.group_box_layout.addWidget(self.button)

        self.group_box = QGroupBox("Welcome to Melid")
        self.group_box.setMaximumWidth(int(self.width() * 0.5))
        self.group_box.setLayout(self.group_box_layout)

        self.setAlignment(Qt.AlignCenter)
        self.addWidget(self.group_box)


class ProfilePage(Router):

    TITLE = "Profile Page"

    def __init__(self, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)

        self.button = QPushButton("Page Two")
        self.button.clicked.connect(lambda _: self.navigate("index"))
        self.addWidget(self.button)


class Window(App):

    STYLESHEET_PATH = "./examples/basic/style.css"

    def __init__(self):
        super(Window, self).__init__()

        self.router = Router(
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
