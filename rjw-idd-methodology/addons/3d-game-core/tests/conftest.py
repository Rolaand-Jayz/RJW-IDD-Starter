import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
TOOLS = ROOT / "addons" / "3d-game-core" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
