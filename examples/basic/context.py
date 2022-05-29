import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

sys.path.append(str(BASE_DIR.absolute()))

import melid as _
