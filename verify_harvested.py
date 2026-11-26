import json
import urllib.request
import sys

with open('harvested_rss.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total items in harvested_rss: {len(items)}")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

valid_items = []
for i, item in enumerate(items):
    url = item['url']
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            code = resp.getcode()
            print(f"[{code}] {item['outlet']}: {item['title'][:50]} -> {url}")
            valid_items.append(item)
    except Exception as e:
        print(f"[FAIL {e}] {item['outlet']}: {item['title'][:50]}")
    sys.stdout.flush()

print(f"\nTotal verified 200 OK from live feeds: {len(valid_items)}")
with open('verified_live_articles.json', 'w', encoding='utf-8') as f:
    json.dump(valid_items, f, indent=2)
