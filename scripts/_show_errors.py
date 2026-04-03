import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for path in sorted(ROOT.glob("*Module*.json")):
    if path.name.startswith("_"):
        continue
    s = path.read_text(encoding="utf-8")
    try:
        json.loads(s)
    except json.JSONDecodeError as e:
        i = e.pos
        print(path.name, "pos", i)
        print(repr(s[max(0, i - 80) : i + 80]))
        print()
