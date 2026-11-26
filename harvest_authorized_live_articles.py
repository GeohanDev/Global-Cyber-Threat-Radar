import urllib.request
import xml.etree.ElementTree as ET
import json
import re

feeds = [
    ("The Record", "https://therecord.media/feed"),
    ("Dark Reading", "https://www.darkreading.com/rss.xml"),
    ("SecurityWeek", "https://www.securityweek.com/feed/"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

all_articles = []

for outlet, url in feeds:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            # Find all items
            items = root.findall('.//item')
            print(f"[{outlet}] Found {len(items)} items")
            for item in items:
                title = item.find('title')
                link = item.find('link')
                pubDate = item.find('pubDate')
                desc = item.find('description')
                
                title_text = title.text.strip() if title is not None and title.text else ""
                link_text = link.text.strip() if link is not None and link.text else ""
                date_text = pubDate.text.strip() if pubDate is not None and pubDate.text else ""
                desc_text = desc.text.strip() if desc is not None and desc.text else ""
                
                if link_text and title_text:
                    all_articles.append({
                        "outlet": outlet,
                        "title": title_text,
                        "url": link_text,
                        "date": date_text,
                        "description": desc_text
                    })
    except Exception as e:
        print(f"[{outlet}] Error: {e}")

print(f"\nTotal harvested: {len(all_articles)}")

# Filter for AI/cyber security related
ai_keywords = ['ai', 'artificial intelligence', 'llm', 'chatgpt', 'copilot', 'deepfake', 'gpt', 'genai', 'claude', 'gemini', 'anthropic', 'openai', 'machine learning', 'prompt', 'agent']

ai_articles = []
for a in all_articles:
    text_to_check = (a['title'] + " " + a['description']).lower()
    # check word boundary for short terms like 'ai'
    is_match = False
    for kw in ai_keywords:
        if kw in ['ai', 'llm', 'gpt']:
            if re.search(r'\b' + kw + r'\b', text_to_check):
                is_match = True
                break
        else:
            if kw in text_to_check:
                is_match = True
                break
    if is_match:
        ai_articles.append(a)

print(f"Total AI-related articles found: {len(ai_articles)}")
for a in ai_articles[:15]:
    print(f"- [{a['outlet']}] {a['title']}")
    print(f"  URL: {a['url']}")

with open('harvested_rss.json', 'w', encoding='utf-8') as f:
    json.dump(ai_articles, f, indent=2)
