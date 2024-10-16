import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout

from melid.app import App
from melid.router import Router
from melid.store import Store
from melid.widgets import Button, Label

globalStore = Store(initialState={"count": 1})


class IndexPage(Router):

    STYLESHEET_TYPE = "CSS"
    TITLE = "Index Page"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = Label(lambda: globalStore.state["count"])

        self.increase_button = Button(child="+")
        self.increase_button.clicked.connect(
            lambda: globalStore.setState({"count": globalStore.state["count"] + 1})
        )

        self.reduce_button = Button(child="-")
        self.reduce_button.clicked.connect(
            lambda: globalStore.setState({"count": globalStore.state["count"] - 1})
        )

        self.group_box_layout = QVBoxLayout()

        self.group_box_layout.addWidget(self.label)
        self.group_box_layout.addWidget(self.increase_button)
        self.group_box_layout.addWidget(self.reduce_button)

        self.group_box = QGroupBox("Welcome to Melid")
        self.group_box.setMaximumWidth(int(self.width() * 0.5))
        self.group_box.setLayout(self.group_box_layout)

        self.setAlignment(Qt.AlignCenter)
        self.addWidget(self.group_box)


class Window(App):

    STYLESHEET_PATH = "./examples/store/style.css"

    def __init__(self):
        super(Window, self).__init__()

        self.addWidget(IndexPage())


def main():
    window = Window()
    window.mount(showMaximized=False)


if __name__ == "__main__":
    main()
