from typing import Any, Dict


def generate_size_utilities(sizes: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate color utilities for padding, margin, border width, border radius, width and height
    """
    utilities = {}

    for name, value in sizes.items():
        # Padding Utilities
        utilities[f"p-{name}"] = {
            "declarations": [{"property": "padding", "value": value}]
        }
        utilities[f"px-{name}"] = {
            "declarations": [
                {"property": "padding-left", "value": value},
                {"property": "padding-right", "value": value},
            ]
        }
        utilities[f"py-{name}"] = {
            "declarations": [
                {"property": "padding-top", "value": value},
                {"property": "padding-bottom", "value": value},
            ],
        }
        utilities[f"pl-{name}"] = {
            "declarations": [{"property": "padding-left", "value": value}]
        }
        utilities[f"pr-{name}"] = {
            "declarations": [{"property": "padding-right", "value": value}]
        }
        utilities[f"pt-{name}"] = {
            "declarations": [{"property": "padding-top", "value": value}]
        }
        utilities[f"pb-{name}"] = {
            "declarations": [{"property": "padding-bottom", "value": value}]
        }

        # Margin Utilities
        utilities[f"m-{name}"] = {
            "declarations": [{"property": "margin", "value": value}]
        }
        utilities[f"mx-{name}"] = {
            "declarations": [
                {"property": "margin-left", "value": value},
                {"property": "margin-right", "value": value},
            ]
        }
        utilities[f"my-{name}"] = {
            "declarations": [
                {"property": "margin-top", "value": value},
                {"property": "margin-bottom", "value": value},
            ],
        }
        utilities[f"ml-{name}"] = {
            "declarations": [{"property": "margin-left", "value": value}]
        }
        utilities[f"mr-{name}"] = {
            "declarations": [{"property": "margin-right", "value": value}]
        }
        utilities[f"mt-{name}"] = {
            "declarations": [{"property": "margin-top", "value": value}]
        }
        utilities[f"mb-{name}"] = {
            "declarations": [{"property": "margin-bottom", "value": value}]
        }

        # Border Utilities
        utilities[f"border-{name}"] = {
            "declarations": [{"property": "border-width", "value": value}]
        }
        utilities[f"border-x-{name}"] = {
            "declarations": [
                {"property": "border-left-width", "value": value},
                {"property": "border-right-width", "value": value},
            ]
        }
        utilities[f"border-y-{name}"] = {
            "declarations": [
                {"property": "border-top-width", "value": value},
                {"property": "border-bottom-width", "value": value},
            ],
        }
        utilities[f"border-l-{name}"] = {
            "declarations": [{"property": "border-left-width", "value": value}]
        }
        utilities[f"border-r-{name}"] = {
            "declarations": [{"property": "border-right-width", "value": value}]
        }
        utilities[f"border-t-{name}"] = {
            "declarations": [{"property": "border-top-width", "value": value}]
        }
        utilities[f"border-b-{name}"] = {
            "declarations": [{"property": "border-bottom-width", "value": value}]
        }

        # Border Radius Utilities
        # TODO: direction combos (top-right, bottom-left, etc)
        utilities[f"rounded-{name}"] = {
            "declarations": [{"property": "border-radius", "value": value}]
        }
        utilities[f"rounded-l-{name}"] = {
            "declarations": [
                {"property": "border-top-left-radius", "value": value},
                {"property": "border-bottom-left-radius", "value": value},
            ]
        }
        utilities[f"rounded-r-{name}"] = {
            "declarations": [
                {"property": "border-top-right-radius", "value": value},
                {"property": "border-bottom-right-radius", "value": value},
            ]
        }
        utilities[f"rounded-t-{name}"] = {
            "declarations": [
                {"property": "border-top-left-radius", "value": value},
                {"property": "border-top-right-radius", "value": value},
            ]
        }
        utilities[f"rounded-b-{name}"] = {
            "declarations": [
                {"property": "border-bottom-left-radius", "value": value},
                {"property": "border-bottom-right-radius", "value": value},
            ]
        }

        # Width and Height Utilities
        utilities[f"w-{name}"] = {
            "declarations": [{"property": "width", "value": value}]
        }
        utilities[f"h-{name}"] = {
            "declarations": [{"property": "height", "value": value}]
        }
        utilities[f"min-w-{name}"] = {
            "declarations": [{"property": "min-width", "value": value}]
        }
        utilities[f"min-h-{name}"] = {
            "declarations": [{"property": "min-height", "value": value}]
        }
        utilities[f"max-w-{name}"] = {
            "declarations": [{"property": "max-width", "value": value}]
        }
        utilities[f"max-h-{name}"] = {
            "declarations": [{"property": "max-height", "value": value}]
        }

    return utilities
