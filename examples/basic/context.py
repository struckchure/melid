import pathlib
import sys

BASE_DIR = pathlib.Path(__file__).parent.parent.parent

sys.path.insert(0, str(BASE_DIR.absolute()))

import melid as _
