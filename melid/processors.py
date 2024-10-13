class CSSProcessor:

    STYLESHEET_PATH: str
    STYLESHEET_TYPE: str

    STYLESHEET_TYPES = ["CSS"]

    def __init__(self, stylesheet_path: str, stylesheet_type="CSS"):
        super(CSSProcessor, self).__init__()

        # validate style sheet type (if in STYLESHEET_TYPES)

        if stylesheet_type not in self.STYLESHEET_TYPES:
            raise ValueError(
                "%s is not supported, available options are %s"
                % (stylesheet_type, self.STYLESHEET_TYPES)
            )

        self.STYLESHEET_PATH = stylesheet_path
        self.STYLESHEET_TYPE = stylesheet_type

    def trim_text(self, text):
        escapes = "".join([chr(char) for char in range(1, 15)])
        translator = str.maketrans("", "", escapes)

        return text.translate(translator)

    def read_style_sheet(self):
        style = ""

        if self.STYLESHEET_PATH:
            with open(self.STYLESHEET_PATH, "r") as file:
                for line in file.readlines():
                    # ignore comments
                    if not line.startswith("/*") and not line.endswith("*/"):
                        style += line

        return style

    def get(self, class_names: str = None, style: str = "") -> str:
        if class_names:
            __class_names: list = class_names.split(" ")

            def parse_class_name(class_name: str) -> str:
                class_block = self.read_style_sheet()[
                    self.read_style_sheet().find(".%s" % class_name)
                    + len(class_name)
                    + 1 :
                ]

                starts_at = class_block.find("{") + 1
                ends_at = class_block.find("}")

                return self.trim_text(class_block[starts_at:ends_at])

            return "".join(map(parse_class_name, __class_names)) + " " + style

        return style
