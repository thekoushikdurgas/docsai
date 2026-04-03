"""Validate Postman JSON files in this directory."""
import json
import sys
from pathlib import Path

def main() -> None:
    root = Path(__file__).resolve().parent
    errors = []
    for path in sorted(root.glob("*.json")):
        if path.name.startswith("_"):
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}: {e}")
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("OK:", len(list(root.glob("*.json"))) - 1, "files")

if __name__ == "__main__":
    main()
