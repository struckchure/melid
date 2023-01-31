import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))


from PyQt5.QtWidgets import QPushButton

from melid.base.app import App
from melid.base.processors import Processor
from melid.router.view import Router, RouterView


class ProfilePage(Router):

    TITLE = "Profile Page"

    def __init__(self, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)
        pser = Processor(
            stylesheet_path=BASE_DIR.joinpath("examples/css_processor/style.qss")
        )

        self.button = QPushButton("Page Two")
        self.button.setStyleSheet(
            pser.get_style("bg-red text-white px-5 py-5 mx-5 text-md rounded-md")
        )
        self.addWidget(self.button)


class Window(App):

    STYLESHEET_PATH = BASE_DIR.joinpath("examples/css_processor/style.qss")

    def __init__(self):
        super(Window, self).__init__()

        self.router = RouterView(
            routes=[
                {"name": "profile", "view": ProfilePage},
            ]
        )

        self.addWidget(self.router)


def main():
    window = Window()
    window.mount(showMaximized=False)


if __name__ == "__main__":
    main()
