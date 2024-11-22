from pathlib import Path
import json

# Get the current file's directory and construct the path to grind75.json
current_dir = Path(__file__).parent
grind_75 = json.load(open(current_dir / "grind75.json"))
