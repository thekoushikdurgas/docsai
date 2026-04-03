"""Fix duplicated }} before closing raw string in Postman collections (invalid JSON)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BAD = '}}"}},"url"'
GOOD = '}}"},"url"'
BAD2 = '}}"}}}'  # rare trailing
# activityStats ends with variables: {} differently
BAD3 = '}}}"},"url"'  # activities filters - wrong, see 11

fixed = []
for path in sorted(ROOT.glob("*Module*.json")):
    if path.name.startswith("_"):
        continue
    text = path.read_text(encoding="utf-8")
    if BAD in text:
        text2 = text.replace(BAD, GOOD)
        if text2 != text:
            path.write_text(text2, encoding="utf-8")
            fixed.append((path.name, text.count(BAD)))

# 11_Activities might have }}\"}"} pattern
p11 = ROOT / "11_Activities_Module.postman_collection.json"
if p11.exists():
    t = p11.read_text(encoding="utf-8")
    # fix }}\"}"}  -> \"}}"}  for activities line
    bad_a = '\"offset\":0}}\"}"}'
    good_a = '\"offset\":0}}"}'
    if bad_a in t:
        t = t.replace(bad_a, good_a)
        p11.write_text(t, encoding="utf-8")
        fixed.append(("11 activities fix", 1))

print("fixed:", fixed)
