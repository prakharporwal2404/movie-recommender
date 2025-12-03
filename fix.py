# fix_movies_json.py
import json, re, sys
from pathlib import Path

PATH = Path("data/sample_movies.json")  # update if your file path differs
if not PATH.exists():
    print("File not found:", PATH)
    sys.exit(1)

text = PATH.read_text(encoding="utf-8")

# 1) Try normal load (if already valid, exit)
try:
    json.loads(text)
    print("movies.json already valid JSON. No changes made.")
    sys.exit(0)
except json.JSONDecodeError:
    pass

# 2) Try NDJSON parse
objs = []
nd = True
for line in text.splitlines():
    if not line.strip():
        continue
    try:
        objs.append(json.loads(line))
    except json.JSONDecodeError:
        nd = False
        break
if nd and objs:
    PATH.write_text(json.dumps(objs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Rewrote as JSON array from NDJSON. ({len(objs)} objects)")
    sys.exit(0)

# 3) Repair concatenated JSON objects by replacing '}{' boundaries
repaired = re.sub(r'\}\s*\{', '},{', text, flags=re.M)
repaired = f'[{repaired}]'
try:
    data = json.loads(repaired)
    PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Repaired concatenated JSON objects into an array. ({len(data)} objects)")
    sys.exit(0)
except json.JSONDecodeError as e:
    print("Could not auto-repair movies.json:", e)
    sys.exit(2)
