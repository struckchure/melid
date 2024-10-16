import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))


from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from melid.app import CreateApp
from melid.layout import Box, Direction
from melid.router import Route, Router
from melid.store import State
from melid.tailwind import Tailwind, TailwindConfig
from melid.widgets import Button, Input, InputType, Label, Option, Select

tw_cfg = TailwindConfig().extend(colors={"primary": "gold"})
tw = Tailwind(tw_cfg).tw


def HomePage():
    def open_folder():
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Folder")

        # If a folder is selected, display the path
        if folder_path:
            print(f"Selected Folder: {folder_path}")
        else:
            print("No folder selected")

    return Box(
        [
            Box(
                Button(
                    "Open Folder",
                    on_click=open_folder,
                    style=tw(
                        "Button",
                        "rounded-none px-6 py-2 hover:bg-blue-700 bg-blue-800",
                    ),
                ),
                style=tw(
                    "Box",
                    "rounded-0 bg-gray-800 h-full w-80 p-4 m-0",
                ),
                alignment=Qt.AlignmentFlag.AlignCenter,
                direction=Direction.ROW,
                gap=5,
            ),
            Box(
                Label("Welcome to Melid"),
                style=tw("Box", "rounded-0 bg-gray-900 h-full w-full p-4"),
                alignment=Qt.AlignmentFlag.AlignCenter,
                direction=Direction.ROW,
                gap=5,
            ),
        ],
        direction=Direction.ROW,
        alignment=Qt.AlignmentFlag.AlignLeft,
        style=tw("Box", "rounded-0 h-full w-full p-0"),
        gap=0,
    )


def LoginPage():
    username = State("")
    password = State("")
    show_password = State(False)

    update_title = lambda: ["%s / %s" % (username.get(), password.get())]

    return Box(
        Box(
            [
                Select(
                    [Option("Python", 1), Option("Go", 2), Option("TypeScript", 3)],
                    on_change=print,
                    style=tw("Select", "rounded-0 p-2 bg-gray-900")
                    + tw("Select QAbstractItemView", "px-2 w-full"),
                ),
                Label(
                    update_title()[0],
                    style=tw(
                        "Label",
                        "p-2 rounded-none text-black bg-primary",
                    ),
                )
                .state(username, lambda: True, "setText", update_title)
                .state(password, lambda: True, "setText", update_title),
                Input(
                    placeholder="Username",
                    on_change=lambda val: username.set(val),
                    style=tw(
                        "Input",
                        "p-2 rounded-none bg-gray-900",
                    ),
                ).state(
                    username,
                    lambda: username.get() == "user",
                    "updateStyleSheet",
                    [tw("Input", "text-red-500")],
                ),
                Box(
                    [
                        Input(
                            placeholder="Password",
                            on_change=lambda val: password.set(val),
                            input_type=InputType.PASSWORD,
                            style=tw(
                                "Input",
                                "p-2 rounded-none bg-gray-900 w-full h-full",
                            ),
                        )
                        .state(
                            password, lambda: password.get() == "pass", "deleteLater"
                        )
                        .state(
                            show_password,
                            lambda: show_password.get() == True,
                            "setEchoMode",
                            [QtWidgets.QLineEdit.Normal],
                        )
                        .state(
                            show_password,
                            lambda: show_password.get() == False,
                            "setEchoMode",
                            [QtWidgets.QLineEdit.Password],
                        ),
                        Button(
                            "show",
                            style=tw(
                                "Button",
                                "p-2 rounded-none bg-gray-900 h-full",
                            ),
                            on_click=lambda: show_password.set(not show_password.get()),
                        )
                        .state(
                            show_password,
                            lambda: show_password.get() == True,
                            "setText",
                            ["hide"],
                        )
                        .state(
                            show_password,
                            lambda: show_password.get() == False,
                            "setText",
                            ["show"],
                        ),
                    ],
                    alignment=Qt.AlignmentFlag.AlignVCenter,
                    style=tw("Box", "max-h-10"),
                ),
                Button(
                    "Login",
                    on_click=lambda: Router.navigate("/home"),
                    style=tw(
                        "Button",
                        "p-2 rounded-none bg-gray-900",
                    ),
                ),
            ],
            direction=Direction.COLUMN,
            alignment=Qt.AlignmentFlag.AlignVCenter,
            gap=20,
            style=tw(
                "Box",
                "rounded-none max-w-60",
            ),
        ),
        alignment=Qt.AlignmentFlag.AlignCenter,
        style=tw(
            "Box",
            "rounded-none bg-gray-800",
        ),
    )


try:
    CreateApp(
        Router(
            Route("/", LoginPage()),
            Route("/home", HomePage()),
        ),
    ).mount()
except Exception as e:
    print(str(e))
