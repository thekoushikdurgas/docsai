import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = [
    "17_AI_Chats_Module.postman_collection.json",
    "19_Pages_Module.postman_collection.json",
    "21_LinkedIn_Module.postman_collection.json",
    "26_Saved_Searches_Module.postman_collection.json",
    "28_Profile_Module.postman_collection.json",
]
for name in FILES:
    path = ROOT / name
    s = path.read_text(encoding="utf-8")
    try:
        json.loads(s)
    except json.JSONDecodeError as e:
        i = e.pos
        print(path.name, "pos", i)
        print(repr(s[max(0, i - 80) : i + 80]))
        print()
