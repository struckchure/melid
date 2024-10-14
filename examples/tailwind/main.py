import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))

from melid.tailwind import Tailwind

print(
    Tailwind().tw(
        "Button",
        "bg-blue-300 text-black hover:bg-blue-500 rounded-md hover:p-sm ml-sm",
    )
)
