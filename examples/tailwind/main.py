import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(BASE_DIR))

from melid.tailwind import Tailwind, TailwindConfig

tw_cfg = TailwindConfig()
tw_cfg.extend(
    colors={"primary": "orange"},
    variants={"checked": {"type": "pseudo", "pseudo": ":checked"}},
)

print(
    Tailwind(tw_cfg).tw(
        "Button",
        "bg-primary border-primary text-black checked:bg-pink-500 hover:bg-blue-500 rounded-md hover:p-sm ml-sm after:w-40",
    )
)
