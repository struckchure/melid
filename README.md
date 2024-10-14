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
