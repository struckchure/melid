from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from melid.tailwind.color import generate_color_utilities
from melid.tailwind.configs.color import COLORS
from melid.tailwind.configs.size import SIZES
from melid.tailwind.configs.variants import VARIANTS
from melid.tailwind.css_ast import (
    Ast,
    AstNode,
    AtRoot,
    Context,
    Declaration,
    Rule,
    WalkAction,
)
from melid.tailwind.size import generate_size_utilities
from melid.tailwind.utils import generate_utilities_with_variants


@dataclass
class TailwindConfig:
    colors: Dict[str, str] = field(default_factory=lambda: COLORS)
    sizes: Dict[str, str] = field(default_factory=lambda: SIZES)
    variants: Dict[str, Dict[str, str]] = field(default_factory=lambda: VARIANTS)

    def __build_utilities_ast(self) -> List[AstNode]:
        """Generate AST nodes for the additional utilities."""
        utilities = {}

        utility_ast = []
        utility_ast.extend(
            generate_utilities_with_variants(
                {
                    **generate_color_utilities(self.colors),
                    **generate_size_utilities(self.sizes),
                },
                self.variants,
            )
        )

        for class_name, utility in utilities.items():
            utility_ast.append(Ast.rule(class_name, utility["declarations"]))

        return utility_ast

    @property
    def utilities(self):
        return self.__build_utilities_ast()

    def extend(
        self,
        colors: Dict[str, str] = None,
        sizes: Dict[str, str] = None,
        variants: Dict[str, Dict[str, str]] = None,
    ):
        if colors:
            self.colors.update(colors)

        if sizes:
            self.sizes.update(sizes)

        if variants:
            self.variants.update(variants)

        return self


class Tailwind:
    _INSTANCE = None

    # Build the main AST
    __initial_ast: List[AstNode] = []

    _initialized = False  # Flag to track if __init__ has already been executed

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super().__new__(cls)
        return cls._INSTANCE

    def __init__(self, config: Optional[TailwindConfig] = None):
        if not self._initialized:
            self._initialized = True  # Ensure this is only done once

            # Handle the config to avoid mutable default argument issues
            if config is None:
                config = TailwindConfig()

            self.__initial_ast.extend(config.utilities)

            # Walk the AST and modify it
            Ast.walk(self.__initial_ast, self.visit_function)

            self.__utility_map = self.build_utility_map(self.__initial_ast)

    def visit_function(
        self, node: AstNode, utils: Dict[str, Any]
    ) -> Optional[WalkAction]:
        """
        Traverse AST nodes and update utilities, variants, and colors.
        """
        if isinstance(node, Declaration):
            # Update color values or any other transformation here
            pass  # Customize as needed

        # Process variants (like hover, focus, etc.)
        elif isinstance(node, Context):
            for child in node.nodes:
                self.visit_function(child, utils)

        return WalkAction.CONTINUE

    def build_utility_map(self, ast: List[AstNode]) -> Dict[str, List[Declaration]]:
        """
        Build a utility map from the AST, mapping class names to their declarations.
        """
        utility_map: Dict[str, List[Declaration]] = {}

        def traverse(node: AstNode):
            if isinstance(node, Rule):
                if node.selector.startswith("."):
                    class_selector = node.selector[1:]
                    class_name = class_selector.replace("\\:", ":")
                    declarations = [
                        child for child in node.nodes if isinstance(child, Declaration)
                    ]
                    if declarations:
                        utility_map[class_name] = declarations
            elif isinstance(node, Context) or isinstance(node, AtRoot):
                for child in node.nodes:
                    traverse(child)

        for node in ast:
            traverse(node)

        return utility_map

    def process_class_names(
        self, class_names: str, utility_map: Dict[str, List[Declaration]]
    ) -> Dict[str, List[Declaration]]:
        """
        Process a string of Tailwind-like class names and return a dictionary of
        base and variant CSS declarations.
        """
        base_declarations: List[Declaration] = []
        variant_declarations: Dict[str, List[Declaration]] = {}

        classes = class_names.split()

        for cls in classes:
            if cls in utility_map:
                # Check if the class contains a variant (like hover:)
                if ":" in cls:
                    variant, base_class = cls.split(":")
                    if base_class in utility_map:
                        if variant not in variant_declarations:
                            variant_declarations[variant] = []
                        variant_declarations[variant].extend(utility_map[base_class])
                else:
                    base_declarations.extend(utility_map[cls])
            else:
                print(f"Warning: Class '{cls}' is not defined in the utility map.")

        return {
            "base": base_declarations,
            "variants": variant_declarations,
        }

    @classmethod
    def tw(cls, element: str, class_names: str) -> str:
        """
        Process class names and return corresponding CSS rules for an element,
        including variants like `hover`.
        """

        if not cls._INSTANCE:
            raise ValueError("Router has not been initialized")

        declarations = cls._INSTANCE.process_class_names(
            class_names, cls._INSTANCE.__utility_map
        )

        # Build the base CSS rule
        css_output = f"{element} {{\n"
        for decl in declarations["base"]:
            css_output += f"  {decl.property}: {decl.value};\n"
        css_output += "}\n"

        # Build the CSS rules for variants (e.g., hover, focus, etc.)
        for variant, decls in declarations["variants"].items():
            css_output += f"{element}:{variant} {{\n"
            for decl in decls:
                css_output += f"  {decl.property}: {decl.value};\n"
            css_output += "}\n"

        return css_output
