from PyQt5.QtWidgets import QApplication
import sys

from melid.base.widget import Widget


class App(Widget):

    WINDOW_APP = QApplication(sys.argv)

    MIN_WIDTH = 500
    MIN_HEIGHT = 500
    DEFAULT_WINDOW_TITLE = "Welcome to Melid || Made with <3 by Dev 47"

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.setDefaults()

    def setDefaults(self):
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.setWindowTitle(self.DEFAULT_WINDOW_TITLE)

    def mount(self, showMaximized=True):
        if showMaximized:
            self.showMaximized()

        self.show()

        sys.exit(self.WINDOW_APP.exec_())


if __name__ == "__main__":
    window = App()
    window.mount()
