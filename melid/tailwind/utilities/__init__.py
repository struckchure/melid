from typing import Any, Dict, List

from melid.tailwind.css_ast import Ast, AstNode


def generate_ast(utilities: Dict[str, Any]) -> Dict[str, AstNode]:
    """
    Convert utility mappings into AST nodes.

    Args:
        utilities (Dict[str, Any]): A dictionary of utility classes.

    Returns:
        Dict[str, AstNode]: A dictionary mapping class names to AST nodes.
    """
    utility_ast = {}

    for class_name, utility in utilities.items():
        declarations = [
            Ast.decl(declaration["property"], declaration["value"])
            for declaration in utility["declarations"]
        ]
        rule_node = Ast.rule(f".{class_name}", declarations)
        utility_ast[class_name] = rule_node

    return utility_ast


def generate_utilities_with_variants(
    utilities: Dict[str, str], variants: Dict[str, Dict[str, str]]
) -> List[AstNode]:
    """
    Generate utilities with variants.

    Args:
        utilities (Dict[str, str]): Utilities definitions..
        variants (Dict[str, Dict[str, str]]): Variants definitions.

    Returns:
        List[AstNode]: List of AST nodes for utilities with variants.
    """

    utility_ast = generate_ast(utilities)
    extended_ast: List[AstNode] = list(utility_ast.values())

    for variant_name, variant_detail in variants.items():
        variant_type = variant_detail["type"]
        if variant_type == "pseudo":
            for class_name, rule_node in utility_ast.items():
                # Escape colon in class names
                variant_class = f".{variant_name}\\:{class_name}"

                # Clone declarations
                declarations = [
                    Ast.decl(d.property, d.value, d.important) for d in rule_node.nodes
                ]
                variant_rule_node = Ast.rule(variant_class, declarations)
                extended_ast.append(variant_rule_node)

    return extended_ast


def generate_color_utilities(palette: Dict[str, str]) -> Dict[str, Any]:
    """
    Generate color utilities for background, text, and border colors.

    Args:
        palette (Dict[str, str]): A dictionary mapping color names to hex values.

    Returns:
        Dict[str, Any]: A dictionary of utility classes.
    """
    utilities = {}

    for color_name, color_value in palette.items():
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
                {"property": "border-width-left", "value": value},
                {"property": "border-width-right", "value": value},
            ]
        }
        utilities[f"border-y-{name}"] = {
            "declarations": [
                {"property": "border-width-top", "value": value},
                {"property": "border-width-bottom", "value": value},
            ],
        }
        utilities[f"border-l-{name}"] = {
            "declarations": [{"property": "border-width-left", "value": value}]
        }
        utilities[f"border-r-{name}"] = {
            "declarations": [{"property": "border-width-right", "value": value}]
        }
        utilities[f"border-t-{name}"] = {
            "declarations": [{"property": "border-width-top", "value": value}]
        }
        utilities[f"border-b-{name}"] = {
            "declarations": [{"property": "border-width-bottom", "value": value}]
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
