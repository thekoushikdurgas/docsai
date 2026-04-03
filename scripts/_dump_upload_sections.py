import re

s = open(
    r"d:\code\ayan\contact\docs\backend\postman\10_Upload_Module.postman_collection.json",
    encoding="utf-8",
).read()
for name in ["uploadStatus", "presignedUrl", "initiateUpload", "registerPart", "completeUpload", "abortUpload"]:
    i = s.find(f'"name":"{name}"')
    if i < 0:
        print("missing", name)
        continue
    j = s.find('"raw":"', i)
    k = s.find('"},"url"', j)
    raw = s[j + 7 : k]
    print(name, "tail:", repr(raw[-70:]))
