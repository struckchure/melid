from typing import Any, Dict


def generate_color_utilities(colors: Dict[str, str]) -> Dict[str, Any]:
    utilities = {}

    for color_name, color_value in colors.items():
        # Background Color Utilities
        utilities[f"bg-{color_name}"] = {
            "declarations": [{"property": "background-color", "value": color_value}]
        }

        # Text Color Utilities
        utilities[f"text-{color_name}"] = {
            "declarations": [{"property": "color", "value": color_value}]
        }

        # Border Color Utilities
        utilities[f"border-{color_name}"] = {
            "declarations": [{"property": "border-color", "value": color_value}]
        }

    return utilities
