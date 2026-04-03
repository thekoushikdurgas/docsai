import json
import re

path = r"d:\code\ayan\contact\docs\backend\postman\10_Upload_Module.postman_collection.json"
s = open(path, encoding="utf-8").read()
# Find uploadStatus raw
i = s.find("uploadStatus")
j = s.find('"raw":', i)
k = s.find('","url"', j)
chunk = s[j + 7 : k]  # after "raw":
print("raw uploadStatus chunk tail:", repr(chunk[-120:]))
# presignedUrl
i2 = s.find("presignedUrl")
j2 = s.find('"raw":', i2)
k2 = s.find('","url"', j2)
chunk2 = s[j2 + 7 : k2]
print("raw presignedUrl chunk tail:", repr(chunk2[-120:]))
