from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Union

# Define AST Node Types


@dataclass
class Rule:
    kind: str = field(init=False, default="rule")
    selector: str
    nodes: List["AstNode"]


@dataclass
class Declaration:
    kind: str = field(init=False, default="declaration")
    property: str
    value: Optional[str] = None
    important: bool = False


@dataclass
class Comment:
    kind: str = field(init=False, default="comment")
    value: str


@dataclass
class Context:
    kind: str = field(init=False, default="context")
    context: Dict[str, str]
    nodes: List["AstNode"]


@dataclass
class AtRoot:
    kind: str = field(init=False, default="at-root")
    nodes: List["AstNode"]


AstNode = Union[Rule, Declaration, Comment, Context, AtRoot]

# Helper Functions to Create AST Nodes


def rule(selector: str, nodes: List[AstNode]) -> Rule:
    return Rule(selector=selector, nodes=nodes)


def decl(
    property: str, value: Optional[str] = None, important: bool = False
) -> Declaration:
    return Declaration(property=property, value=value, important=important)


def comment(value: str) -> Comment:
    return Comment(value=value)


def context_node(context: Dict[str, str], nodes: List[AstNode]) -> Context:
    return Context(context=context, nodes=nodes)


def at_root(nodes: List[AstNode]) -> AtRoot:
    return AtRoot(nodes=nodes)


# Enum for Walk Actions


class WalkAction(Enum):
    CONTINUE = auto()
    SKIP = auto()
    STOP = auto()


# Walk Function


def walk(
    ast: List[AstNode],
    visit: Callable[[AstNode, Dict[str, Any]], Optional[WalkAction]],
    parent: Optional[AstNode] = None,
    context: Optional[Dict[str, str]] = None,
) -> None:
    if context is None:
        context = {}

    i = 0
    while i < len(ast):
        node = ast[i]

        # Handle Context Nodes
        if isinstance(node, Context):
            new_context = {**context, **node.context}
            walk(node.nodes, visit, parent, new_context)
            i += 1
            continue

        # Prepare utility functions
        utils = {
            "parent": parent,
            "replace_with": lambda new_node: replace_with(ast, i, new_node),
            "context": context,
        }

        # Visit the node
        result = visit(node, utils)
        status = result if result is not None else WalkAction.CONTINUE

        # Handle WalkAction
        if status == WalkAction.STOP:
            return
        elif status == WalkAction.SKIP:
            i += 1
            continue

        # Recursively walk child nodes if it's a Rule
        if isinstance(node, Rule):
            walk(node.nodes, visit, node, context)

        i += 1


def replace_with(
    ast: List[AstNode], index: int, new_node: Union[AstNode, List[AstNode]]
) -> None:
    if isinstance(new_node, list):
        ast[index : index + 1] = new_node
    else:
        ast[index : index + 1] = [new_node]
    # Decrement index to revisit the replaced node(s)
    # This is handled in the walk function by not incrementing 'i' after replacement


# Function to Serialize AST to CSS


def to_css(ast: List[AstNode]) -> str:
    at_roots = ""
    seen_at_properties = set()
    property_fallbacks_root: List[Declaration] = []
    property_fallbacks_universal: List[Declaration] = []

    def stringify(node: AstNode, depth: int = 0) -> str:
        nonlocal at_roots
        css = ""
        indent = "  " * depth

        if isinstance(node, Rule):
            if node.selector == "@tailwind utilities":
                for child in node.nodes:
                    css += stringify(child, depth)
                return css

            # At-rules without nodes
            if node.selector.startswith("@") and not node.nodes:
                return f"{indent}{node.selector};\n"

            if node.selector.startswith("@property ") and depth == 0:
                if node.selector in seen_at_properties:
                    return ""

                property_name = node.selector.replace("@property ", "").strip()
                initial_value = None
                inherits = False

                for prop in node.nodes:
                    if isinstance(prop, Declaration):
                        if prop.property == "initial-value":
                            initial_value = prop.value
                        elif prop.property == "inherits":
                            inherits = prop.value.lower() == "true"

                fallback_decl = decl(
                    property=property_name,
                    value=initial_value if initial_value else "initial",
                )

                if inherits:
                    property_fallbacks_root.append(fallback_decl)
                else:
                    property_fallbacks_universal.append(fallback_decl)

                seen_at_properties.add(node.selector)
                return ""

            css += f"{indent}{node.selector} {{\n"
            for child in node.nodes:
                css += stringify(child, depth + 1)
            css += f"{indent}}}\n"

        elif isinstance(node, Comment):
            css += f"{indent}/*{node.value}*/\n"

        elif isinstance(node, Context):
            for child in node.nodes:
                css += stringify(child, depth)

        elif isinstance(node, AtRoot):
            for child in node.nodes:
                at_roots += stringify(child, 0)
            return css

        elif isinstance(node, Declaration):
            if node.property == "--tw-sort" or node.value is None:
                return css
            important = " !important" if node.important else ""
            css += f"{indent}{node.property}: {node.value}{important};\n"

        return css

    css = ""
    for node in ast:
        result = stringify(node)
        if result:
            css += result

    fallback_ast = []

    if property_fallbacks_root:
        fallback_ast.append(rule(":root", property_fallbacks_root))

    if property_fallbacks_universal:
        fallback_ast.append(
            rule("*, ::before, ::after, ::backdrop", property_fallbacks_universal)
        )

    fallback = ""

    if fallback_ast:
        fallback = stringify(
            rule("@supports (-moz-orient: inline)", [rule("@layer base", fallback_ast)])
        )

    return f"{css}{fallback}{at_roots}"


def generate_utilities(
    utilities: Dict[str, Any], variants: Dict[str, Dict[str, str]] = {}
) -> List[AstNode]:
    utility_rules = []

    # Basic utilities
    for class_name, utility in utilities.items():
        declarations = [
            decl(declaration["property"], declaration["value"])
            for declaration in utility["declarations"]
        ]
        rule_node = rule(f".{class_name}", declarations)
        utility_rules.append(rule_node)

    # Handle variants
    for variant_name, variant_detail in variants.items():
        variant_type = variant_detail.get("type")
        if variant_type == "pseudo":
            pseudo_class = variant_detail.get("pseudo")
            for class_name, utility in utilities.items():
                declarations = [
                    decl(declaration["property"], declaration["value"])
                    for declaration in utility["declarations"]
                ]
                # Escape colon in class names
                variant_class_name = f".{variant_name}\\:{class_name}"
                variant_rule_node = rule(
                    f"{variant_class_name}{pseudo_class}", declarations
                )
                utility_rules.append(variant_rule_node)

        elif variant_type == "media":
            media_query = variant_detail.get("query")
            variant_rules = []
            for class_name, utility in utilities.items():
                declarations = [
                    decl(declaration["property"], declaration["value"])
                    for declaration in utility["declarations"]
                ]
                variant_class_name = f".{variant_name}\\:{class_name}"
                variant_rule_node = rule(f"{variant_class_name}", declarations)
                variant_rules.append(variant_rule_node)
            media_rule = rule(media_query, variant_rules)
            utility_rules.append(media_rule)

    return utility_rules


# __initial_ast: List[AstNode] = [
#     rule(
#         "body",
#         [
#             decl("background-color", "white"),
#             decl("color", "black"),
#             comment("This is a comment"),
#         ],
#     ),
#     rule(
#         ".container",
#         [
#             decl("max-width", "1200px"),
#             decl("margin", "0 auto"),
#         ],
#     ),
#     context_node(
#         {"media": "screen"},
#         [
#             rule(
#                 "@media screen and (max-width: 600px)",
#                 [
#                     decl("background-color", "lightgray"),
#                 ],
#             ),
#         ],
#     ),
#     at_root(
#         [
#             rule(
#                 ":root",
#                 [
#                     decl("--main-color", "#333"),
#                 ],
#             )
#         ]
#     ),
#     rule(
#         "@property --custom-color",
#         [
#             decl("initial-value", "#fff"),
#             decl("inherits", "true"),
#         ],
#     ),
# ]
