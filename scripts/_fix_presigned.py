path = r"d:\code\ayan\contact\docs\backend\postman\10_Upload_Module.postman_collection.json"
s = open(path, encoding="utf-8").read()
old = '\\"partNumber\\":1}"}},'
new = '\\"partNumber\\":1}},'
if old not in s:
    # try unescaped pattern as stored in file
    old2 = '"partNumber\\":1}"}},'
    print("old found", old in s, "old2", old2 in s)
    idx = s.find("partNumber")
    print("snippet", repr(s[idx : idx + 120]))
else:
    s = s.replace(old, new)
    open(path, "w", encoding="utf-8").write(s)
    print("replaced")
