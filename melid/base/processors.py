class Processor:

    STYLESHEET_PATH = None

    STYLESHEET_TYPE = "CSS"
    STYLESHEET_TYPES = ["CSS"]

    def __init__(self, *args, **kwargs):
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

        with open(self.STYLESHEET_PATH, "r") as file:
            for line in file.readlines():
                style += self.trim_text(line)

        return style

    def get_style(self, *class_names):
        __style = ""

        for class_name in class_names:
            section = self.read_style_sheet().find(class_name)
            if section > 0:
                target_section = self.read_style_sheet()[section:]
                target_start = target_section.find("{") + 2
                target_end = target_section.find("}") + 1

                __style += self.read_style_sheet()[target_start:target_end]

        return __style.strip()


def main():
    pser = Processor(stylesheet_path="examples/basic/style.css")
    print(pser.get_style("one"))


if __name__ == "__main__":
    main()
