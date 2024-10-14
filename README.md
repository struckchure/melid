# Melid

Melid is a PyQt5 Library for Desktop Applications containing commonly used utils and advanced widget implementations in very simple forms.

# Features

- [x] Router
- [x] State management
- [x] Data binded widgets (Provider Widget)
- [ ] Hot-reload
- [x] CSS Processor (TailwindCSS Syntax)

# Install

```sh
$ pip install melid
```

# Usage

With Builder Pattern (compose widgets with a Flutter-like pattern)

```python
from PyQt5.QtCore import Qt

from melid.app import CreateApp
from melid.layout import Box, Direction
from melid.processors import CSSProcessor
from melid.router import Route, Router
from melid.utils import Size
from melid.widgets import Button, Input, InputType, Label

css = CSSProcessor(BASE_DIR.joinpath("examples/builder/style.css")).get


def IndexPage():
  return Box(
    Box(
      [
        Label("Click here to "),
        Button(
          "Login",
          on_click=lambda: Router.navigate("/login"),
          style=css("button", "border-radius: none;"),
        ),
      ],
      style=css("py-5"),
      alignment=Qt.AlignmentFlag.AlignCenter,
      direction=Direction.ROW,
      gap=5,
    ),
    alignment=Qt.AlignmentFlag.AlignCenter,
    style=css("py-5 my-5 border-gray"),
  )


def LoginPage():
  return Box(
    Box(
      [
        Input(
          placeholder="Username",
          on_change=print,
          style=css("input", "border-radius: none;"),
        ),
        Input(
          placeholder="Password",
          on_change=print,
          input_type=InputType.PASSWORD,
          style=css("input", "border-radius: none;"),
        ),
        Box(
          [
            Button(
              "Login",
              on_click=lambda: print("hello"),
              style=css(
                  "button", "border-radius: none; border-right: none;"
              ),
            ),
            Button(
              "Go Back",
              on_click=lambda: Router.navigate("/"),
              style=css("button", "border-radius: none;"),
            ),
          ],
          alignment=Qt.AlignmentFlag.AlignVCenter,
          size=Size(minimum_width=400),
        ),
      ],
      direction=Direction.COLUMN,
      alignment=Qt.AlignmentFlag.AlignVCenter,
      size=Size(minimum_width=400),
      gap=20,
    ),
    alignment=Qt.AlignmentFlag.AlignCenter,
  )


if __name__ == "__main__":
  CreateApp(
      Router(
          Route("/", IndexPage()),
          Route("/login", LoginPage()),
      ),
  ).showMaximized().mount()
```

# Styling

Melid comes with it's own implementation of tailwind and it is dependency free.
Due to the default limitations of PyQt5 stylesheet (QSS - CSS2), not all tailwind classes are supported. Also, for layout related styles (flex, grid, etc) and responsive variants, you would have to use melid widgets (`Box`) from that.

```python
from melid.tailwind import Tailwind

print(
  Tailwind().tw(
    "Button",
    "bg-blue-300 text-black hover:bg-blue-500 rounded-md hover:p-sm ml-sm",
  )
)
```

# State Management

Melid provided a way to make data reactive to widgets, with the help of PyQt5 signals and slots.

```python
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from melid.layout import Box
from melid.store import State
from melid.tailwind import Tailwind
from melid.widgets import Button, Input, InputType

username = State("")
password = State("")
show_password = State(False)

update_title = lambda: ["%s / %s" % (username.get(), password.get())]

tw = Tailwind().tw

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
    .state(password, lambda: password.get() == "pass", "deleteLater")
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
)
```
