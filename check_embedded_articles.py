from bs4 import BeautifulSoup
import json

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

script_tag = soup.find('script', {'id': 'embedded-data'})
data = json.loads(script_tag.string)

print(f"Total articles in embedded data: {len(data['articles'])}")
for a in data['articles']:
    print(f"{a['article_id']} | {a['outlet']:<20} | {a['headline'][:40]} | {a['url']}")
