from PyQt5.QtWidgets import QApplication
import sys

from melid.base.widget import Widget
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


class App(Widget):

    WINDOW_APP = QApplication(sys.argv)

    MIN_WIDTH = 500
    MIN_HEIGHT = 500
    TITLE = "Welcome to Melid || Made with ❤ by Struckchure"

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

    def start_watch_reload(self, func):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        path = sys.argv[1] if len(sys.argv) > 1 else "."
        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(func, path, recursive=True)
        observer.start()

        # observer.stop()
        # observer.join()

    def _mount(self, showMaximized=True):
        if showMaximized:
            self.showMaximized()

        self.show()

        sys.exit(self.WINDOW_APP.exec_())

    def mount(self, showMaximized=True):
        self.start_watch_reload(lambda args: self._mount(*args))


if __name__ == "__main__":
    window = App()
    window.mount()
