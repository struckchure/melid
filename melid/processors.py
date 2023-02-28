class Processor:

    STYLESHEET_PATH = None

    STYLESHEET_TYPE = "CSS"
    STYLESHEET_TYPES = ["CSS"]

    def __init__(self, **kwargs):
        super(Processor, self).__init__()

        stylesheet_path = kwargs.get("stylesheet_path")
        stylesheet_type = kwargs.get("stylesheet_type", self.STYLESHEET_TYPE)

        # validate style sheet type (if in STYLESHEET_TYPES)

        if stylesheet_type not in self.STYLESHEET_TYPES:
            raise ValueError(
                "%s is not supported, available options are %s"
                % (stylesheet_type, self.STYLESHEET_TYPES)
            )

        self.STYLESHEET_PATH = (
            stylesheet_path if stylesheet_path else self.STYLESHEET_PATH
        )
        self.STYLESHEET_TYPE = (
            stylesheet_type if stylesheet_type else self.STYLESHEET_TYPE
        )

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

    def get_style(self, class_names: str) -> str:
        __class_names: list = class_names.split(" ")

        def parse_class_name(class_name: str) -> str:
            class_block = self.read_style_sheet()[
                self.read_style_sheet().find(".%s" % class_name) + len(class_name) + 1 :
            ]

            starts_at = class_block.find("{") + 1
            ends_at = class_block.find("}")

            return self.trim_text(class_block[starts_at:ends_at])

        return "".join(map(parse_class_name, __class_names))
