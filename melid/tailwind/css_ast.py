import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


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


class WalkAction(Enum):
    CONTINUE = "CONTINUE"
    SKIP = "SKIP"
    STOP = "STOP"


class Ast:
    @classmethod
    def walk(
        cls,
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
                cls.walk(node.nodes, visit, parent, new_context)
                i += 1
                continue

            # Prepare utility functions
            utils = {
                "parent": parent,
                "replace_with": lambda new_node: cls.replace_with(ast, i, new_node),
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
                cls.walk(node.nodes, visit, node, context)

            i += 1

    def replace_with(
        self,
        ast: List[AstNode],
        index: int,
        new_node: Union[AstNode, List[AstNode]],
    ) -> None:
        if isinstance(new_node, list):
            ast[index : index + 1] = new_node
        else:
            ast[index : index + 1] = [new_node]
        # Decrement index to revisit the replaced node(s)
        # This is handled in the walk function by not incrementing 'i' after replacement

    @classmethod
    def rule(cls, selector: str, nodes: List[AstNode]) -> Rule:
        return Rule(selector=selector, nodes=nodes)

    @classmethod
    def decl(
        cls, property: str, value: Optional[str] = None, important: bool = False
    ) -> Declaration:
        return Declaration(property=property, value=value, important=important)

    @classmethod
    def comment(cls, value: str) -> Comment:
        return Comment(value=value)

    @classmethod
    def context_node(cls, context: Dict[str, str], nodes: List[AstNode]) -> Context:
        return Context(context=context, nodes=nodes)

    @classmethod
    def at_root(cls, nodes: List[AstNode]) -> AtRoot:
        return AtRoot(nodes=nodes)

    def parse_stylesheet(self, css: str) -> List[AstNode]:
        """
        Parse a CSS stylesheet string and convert it into an AST.
        """
        tokens = self.tokenize(css)
        ast, _ = self.parse_rules(tokens, 0)
        return ast

    def tokenize(self, css: str) -> List[str]:
        """
        Tokenize a CSS string into individual tokens (selectors, properties, values, etc.).
        """
        # Remove comments and extra whitespace
        css = re.sub(r"/\*[^*]*\*+([^/*][^*]*\*+)*/", "", css)
        css = css.strip()

        # Tokenize using regex (captures braces, semicolons, colons, etc.)
        token_pattern = re.compile(r"([{};:])|\s+")
        tokens = [
            token for token in token_pattern.split(css) if token and not token.isspace()
        ]
        return tokens

    def parse_rules(self, tokens: List[str], pos: int) -> Tuple[List[AstNode], int]:
        """
        Parse CSS tokens and convert them into a list of Rule AST nodes.
        """
        ast_nodes = []
        current_rule = None
        current_declarations = []

        while pos < len(tokens):
            token = tokens[pos]

            if token == "{":
                # Start of declaration block
                current_rule.nodes, pos = self.parse_declarations(tokens, pos + 1)
                ast_nodes.append(current_rule)
                current_rule = None

            elif token == "}":
                # End of block
                break

            elif token == ";":
                # End of a declaration
                if current_declarations:
                    ast_nodes.append(
                        self.decl(current_declarations[0], current_declarations[1])
                    )
                current_declarations = []

            elif ":" in token:
                # It's a property declaration
                property_name = tokens[pos - 1].strip()
                value = tokens[pos + 1].strip()
                current_declarations = [property_name, value]
                pos += 2  # Move past value

            else:
                # Assume it's a selector if not inside a block
                if current_rule is None:
                    current_rule = self.rule(selector=token.strip(), nodes=[])
            pos += 1

        return ast_nodes, pos

    def parse_declarations(
        self, tokens: List[str], pos: int
    ) -> Tuple[List[AstNode], int]:
        """
        Parse a block of declarations and return as Declaration AST nodes.
        """
        declarations = []
        while pos < len(tokens):
            token = tokens[pos]

            if token == "}":
                break  # End of block

            elif ":" in token:
                # Parse a declaration
                property_name = tokens[pos - 1].strip()
                value = tokens[pos + 1].strip()
                declarations.append(self.decl(property_name, value))
                pos += 2  # Move past the value
            elif token == ";":
                pos += 1  # Move past semicolon
            else:
                pos += 1  # Skip over unknown tokens

        return declarations, pos


# # Example usage
# css_string = """
#     .container {
#         width: 100%;
#         padding: 1rem;
#     }

#     .button {
#         background-color: blue;
#         border-radius: 0.5rem;
#     }
# """

# ast = parse_stylesheet(css_string)
# print(ast)


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
