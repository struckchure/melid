import sys

from PyQt5.QtWidgets import QApplication

from melid.base.widget import Widget


class App(Widget):

    WINDOW_APP = QApplication(sys.argv)

    MIN_WIDTH = 500
    MIN_HEIGHT = 500
    TITLE = "Welcome to Melid || Made with ❤ by Struckchure"

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    def _mount(self, showMaximized=True):
        if showMaximized:
            self.showMaximized()

        self.show()

        sys.exit(self.WINDOW_APP.exec_())

    def mount(self, showMaximized=True):
        self._mount(showMaximized)


if __name__ == "__main__":
    window = App()
    window.mount()
