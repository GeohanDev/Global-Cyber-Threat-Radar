import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = [
    "https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/data/case-studies.json",
    "https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.json"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[SUCCESS] {u}")
            if isinstance(data, list):
                print(f"List with {len(data)} items")
                print("Sample keys:", list(data[0].keys()) if len(data) > 0 else "empty")
            elif isinstance(data, dict):
                print("Dict keys:", list(data.keys())[:10])
                if 'case-studies' in data:
                    print(f"case-studies count: {len(data['case-studies'])}")
                    print("Sample case study:", data['case-studies'][0].get('name'))
    except Exception as e:
        print(f"[FAIL] {u}: {e}")
