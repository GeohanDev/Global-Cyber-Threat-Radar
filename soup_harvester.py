# soup_harvester.py
from bs4 import BeautifulSoup
import urllib.request
import json
import re

feeds = [
    ("The Record", "https://therecord.media/feed"),
    ("Dark Reading", "https://www.darkreading.com/rss.xml"),
    ("SecurityWeek", "https://www.securityweek.com/feed/"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

harvested = []

print("Running BeautifulSoup threat intel extractor...")

for outlet, feed_url in feeds:
    try:
        req = urllib.request.Request(feed_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw_xml = resp.read()
            # Parse with BeautifulSoup XML parser (powered by lxml)
            soup = BeautifulSoup(raw_xml, "xml")
            items = soup.find_all("item")
            print(f"[{outlet}] BeautifulSoup extracted {len(items)} items")
            
            for item in items:
                title_tag = item.find("title")
                link_tag = item.find("link")
                date_tag = item.find("pubdate") or item.find("dc:date")
                desc_tag = item.find("description")
                
                title = title_tag.get_text(strip=True) if title_tag else ""
                # BeautifulSoup gets link text or next sibling text for XML links
                link = ""
                if link_tag:
                    link = link_tag.get_text(strip=True)
                    if not link and link_tag.next_sibling:
                        link = str(link_tag.next_sibling).strip()
                
                # Clean HTML tags inside description using BeautifulSoup
                clean_desc = ""
                if desc_tag:
                    desc_soup = BeautifulSoup(desc_tag.get_text(), "html.parser")
                    clean_desc = desc_soup.get_text(strip=True)
                
                date = date_tag.get_text(strip=True) if date_tag else ""
                
                if link and title:
                    harvested.append({
                        "outlet": outlet,
                        "title": title,
                        "url": link,
                        "date": date,
                        "description": clean_desc
                    })
    except Exception as e:
        print(f"[{outlet}] Error during extraction: {e}")

print(f"\nTotal articles extracted by BeautifulSoup: {len(harvested)}")

# Filter for AI/LLM/cyberattack related content
ai_keywords = ['ai', 'artificial intelligence', 'llm', 'chatgpt', 'copilot', 'deepfake', 'gpt', 'genai', 'claude', 'gemini', 'anthropic', 'openai', 'machine learning', 'prompt injection', 'agentic', 'agent']

ai_extracted = []
for art in harvested:
    combined_text = (art['title'] + " " + art['description']).lower()
    is_match = False
    for kw in ai_keywords:
        if kw in ['ai', 'llm', 'gpt']:
            if re.search(r'\b' + kw + r'\b', combined_text):
                is_match = True
                break
        else:
            if kw in combined_text:
                is_match = True
                break
    if is_match:
        ai_extracted.append(art)

print(f"BeautifulSoup filtered {len(ai_extracted)} AI-focused threat reports.")
for a in ai_extracted[:5]:
    print(f"- [{a['outlet']}] {a['title']}")
    print(f"  URL: {a['url']}")

with open("bs4_extracted_feed.json", "w", encoding="utf-8") as f:
    json.dump(ai_extracted, f, indent=2)

print("\nSaved bs4_extracted_feed.json successfully.")
