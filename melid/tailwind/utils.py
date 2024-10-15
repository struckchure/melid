from typing import Any, Dict, List

from melid.tailwind.css_ast import Ast, AstNode


def generate_ast(utilities: Dict[str, Any]) -> Dict[str, AstNode]:
    utility_ast = {}

    for class_name, utility in utilities.items():
        declarations = list(
            map(
                lambda declaration: Ast.decl(
                    declaration["property"], declaration["value"]
                ),
                utility["declarations"],
            )
        )
        rule_node = Ast.rule(f".{class_name}", declarations)
        utility_ast[class_name] = rule_node

    return utility_ast


def generate_utilities_with_variants(
    utilities: Dict[str, str], variants: Dict[str, Dict[str, str]]
) -> List[AstNode]:

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
