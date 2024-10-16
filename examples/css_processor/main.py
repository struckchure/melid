import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))


from PyQt5.QtWidgets import QPushButton

from melid.app import App
from melid.processors import CSSProcessor
from melid.router import Router


class ProfilePage(Router):

    TITLE = "Profile Page"

    def __init__(self, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)
        pser = CSSProcessor(
            stylesheet_path=BASE_DIR.joinpath("examples/css_processor/style.css")
        )

        self.button = QPushButton("Page Two")
        self.button.setStyleSheet(
            pser.get("bg-red text-white px-5 py-5 mx-5 text-md rounded-md")
        )
        self.addWidget(self.button)


class Window(App):

    STYLESHEET_PATH = BASE_DIR.joinpath("examples/css_processor/style.css")

    def __init__(self):
        super(Window, self).__init__()

        self.router = Router(
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
