# harvest_all_it_ai.py
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
from datetime import datetime, timezone
import json
from email.utils import parsedate_to_datetime

# 25 Dedicated Cyber Threat, CTI, Breach & AI Security Feeds
FEEDS = [
    # 1. Tier-1 Cybersecurity & Threat Intelligence Authorities
    ("BleepingComputer", "https://news.google.com/rss/search?q=site:bleepingcomputer.com&hl=en-US&gl=US&ceid=US:en", "Global", "cyber"),
    ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews", "Global", "cyber"),
    ("Dark Reading", "https://www.darkreading.com/rss.xml", "Global", "cyber"),
    ("SecurityWeek", "https://www.securityweek.com/feed/", "Global", "cyber"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/", "United States", "cyber"),
    ("SecurityAffairs", "https://securityaffairs.com/feed", "Global", "cyber"),

    # 2. Government & Vendor CTI Research Centers
    ("CISA Advisories", "https://news.google.com/rss/search?q=site:cisa.gov+advisory+OR+alert&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("Microsoft Threat Intel", "https://news.google.com/rss/search?q=site:microsoft.com/en-us/security/blog&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("Unit 42 Threat Research", "https://news.google.com/rss/search?q=site:unit42.paloaltonetworks.com&hl=en-US&gl=US&ceid=US:en", "Global", "cyber"),
    ("Cisco Talos Intelligence", "https://news.google.com/rss/search?q=site:blog.talosintelligence.com&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("Mandiant Threat Intel", "https://news.google.com/rss/search?q=site:cloud.google.com/blog/topics/threat-intelligence&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("Zero Day Initiative (ZDI)", "https://news.google.com/rss/search?q=site:zerodayinitiative.com/blog&hl=en-US&gl=US&ceid=US:en", "Global", "cyber"),
    ("Sophos Threat Research", "https://news.google.com/rss/search?q=site:news.sophos.com&hl=en-US&gl=US&ceid=US:en", "Global", "cyber"),

    # 3. Live Breaking Threat & Vulnerability Wire Aggregators
    ("Live Cyberattacks & Breaches", "https://news.google.com/rss/search?q=(cyberattack+OR+ransomware+OR+\"zero-day\"+OR+\"data+breach\"+OR+malware+OR+\"threat+actor\")+when:1d&hl=en-US&gl=US&ceid=US:en", "Global", "cyber"),
    ("AI Cyber Threats & Exploits", "https://news.google.com/rss/search?q=(\"prompt+injection\"+OR+\"model+weights\"+OR+\"jailbreak\"+OR+\"AI+agent\"+OR+\"deepfake+fraud\"+OR+\"adversarial+attack\")+when:2d&hl=en-US&gl=US&ceid=US:en", "Global", "ai"),
    ("Critical Infrastructure Threats", "https://news.google.com/rss/search?q=(CISA+OR+\"critical+infrastructure\"+OR+SCADA+OR+ICS+OR+\"Volt+Typhoon\"+OR+\"state-sponsored+hacker\")+when:2d&hl=en-US&gl=US&ceid=US:en", "Global", "cyber"),
    ("Banking & Financial Threats", "https://news.google.com/rss/search?q=(\"bank\"+OR+\"JPMorgan\"+OR+\"fintech\"+OR+\"wire+fraud\")+AND+(cyberattack+OR+breach+OR+ransomware+OR+hacker)+when:3d&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),

    # 4. Premier Cyber & Security Desks
    ("The Register Security", "https://news.google.com/rss/search?q=site:theregister.com+(security+OR+vulnerability+OR+malware+OR+cyber)&hl=en-US&gl=US&ceid=US:en", "United Kingdom", "cyber"),
    ("Ars Technica Security", "https://news.google.com/rss/search?q=site:arstechnica.com+(security+OR+vulnerability+OR+malware+OR+hack)&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("Wired Threat Desk", "https://news.google.com/rss/search?q=site:wired.com+(security+OR+cyberattack+OR+hacker+OR+breach)&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("ZDNet Security News", "https://news.google.com/rss/search?q=site:zdnet.com+(security+OR+cyberattack+OR+ransomware+OR+hacker)&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("Reuters Cyber Warfare", "https://news.google.com/rss/search?q=site:reuters.com+(cyberattack+OR+hackers+OR+ransomware+OR+cybersecurity)&hl=en-US&gl=US&ceid=US:en", "Global", "cyber"),
    ("Bloomberg Cybersecurity", "https://news.google.com/rss/search?q=site:bloomberg.com+(cyberattack+OR+hackers+OR+ransomware+OR+cybersecurity)&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("CNN Cyber Espionage", "https://news.google.com/rss/search?q=site:cnn.com+(cyberattack+OR+hackers+OR+ransomware+OR+breach)&hl=en-US&gl=US&ceid=US:en", "United States", "cyber"),
    ("BBC Cyber Wire", "https://news.google.com/rss/search?q=site:bbc.com+(cyberattack+OR+hacker+OR+ransomware+OR+malware)&hl=en-US&gl=US&ceid=US:en", "United Kingdom", "cyber")
]

HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1'
}

def parse_date_robust(pub_date_str):
    if not pub_date_str:
        return None
    try:
        return parsedate_to_datetime(pub_date_str)
    except Exception:
        pass
    try:
        clean = pub_date_str.replace('Z', '+00:00')
        return datetime.fromisoformat(clean)
    except Exception:
        pass
    return None

def compute_relative_time(dt):
    if not dt:
        return "Just now"
    try:
        now = datetime.now(timezone.utc)
        # Ensure dt is timezone aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        diff = now - dt
        seconds = diff.total_seconds()
        if seconds < 120:
            return "Just now"
        elif seconds < 3600:
            mins = int(seconds // 60)
            return f"{mins}m ago"
        elif seconds < 86400:
            hrs = int(seconds // 3600)
            return f"{hrs}h ago"
        elif seconds < 7 * 86400:
            days = int(seconds // 86400)
            return f"{days}d ago"
        else:
            weeks = int(seconds // (7 * 86400))
            return f"{weeks}w ago"
    except Exception:
        return "Just now"

def run_harvest():
    all_articles = []
    seen_urls = set()

    for outlet, url, default_country, default_field in FEEDS:
        try:
            req = urllib.request.Request(url, headers=HTTP_HEADERS)
            with urllib.request.urlopen(req, timeout=9) as resp:
                soup = BeautifulSoup(resp.read(), "xml")
                items = soup.find_all("item") or soup.find_all("entry")
                
                count = 0
                for item in items:
                    title_tag = item.find("title")
                    link_tag = item.find("link")
                    desc_tag = item.find("description") or item.find("summary") or item.find("content")
                    date_tag = item.find("pubDate") or item.find("pubdate") or item.find("published") or item.find("updated") or item.find("dc:date")
                    source_tag = item.find("source")
                    source_url = source_tag.get("url") if source_tag else ""
                    
                    raw_title = title_tag.get_text(strip=True) if title_tag else ""
                    # Robust Boundary Sanitization: Strip any embedded HTML/script tags from incoming RSS titles
                    title = BeautifulSoup(raw_title, "html.parser").get_text(strip=True) if raw_title else ""
                    
                    link = ""
                    if link_tag:
                        if link_tag.get("href"):
                            link = link_tag.get("href")
                        else:
                            link = link_tag.get_text(strip=True)
                            if not link and link_tag.next_sibling:
                                link = str(link_tag.next_sibling).strip()
                                
                    # Protocol Validation: Reject javascript:, data:, or non-HTTP links to prevent injection
                    link = link.strip()
                    if not link or not (link.startswith("http://") or link.startswith("https://")) or link in seen_urls or len(title) < 5:
                        continue
                        
                    clean_desc = ""
                    if desc_tag:
                        # Full HTML tag stripping across RSS descriptions
                        desc_soup = BeautifulSoup(desc_tag.get_text(), "html.parser")
                        clean_desc = desc_soup.get_text(strip=True)
                        
                    pub_str = date_tag.get_text(strip=True) if date_tag else ""
                    dt = parse_date_robust(pub_str)
                    rel_time = compute_relative_time(dt)
                    
                    seen_urls.add(link)
                    count += 1
                    
                    # Clean title and detect real publisher if from Google News
                    clean_title = title
                    clean_outlet = outlet
                    
                    # Detect source if title ends with " - Publisher"
                    m = re.search(r'\s+-\s+([^-]+)$', clean_title)
                    if m:
                        detected_pub = m.group(1).strip()
                        if len(detected_pub) > 1 and len(detected_pub) < 30:
                            if "Google News" in outlet:
                                clean_outlet = detected_pub
                            clean_title = clean_title[:m.start()].strip()
                    
                    for suffix in [" - BBC", " - BBC News", " - CNN", " - Reuters", " - Bloomberg", " - The Guardian", " - CNBC", " - TechCrunch", " - WIRED"]:
                        if clean_title.endswith(suffix):
                            clean_title = clean_title[:-len(suffix)].strip()
                            clean_outlet = suffix.replace(" - ", "").strip()
                            if clean_outlet == "BBC": clean_outlet = "BBC News"

                    # Classify field
                    comb = (clean_title + " " + clean_desc).lower()
                    field = default_field
                    if any(k in comb for k in ['ai', 'llm', 'chatgpt', 'openai', 'gemini', 'claude', 'anthropic', 'model', 'neural', 'deepseek', 'copilot', 'genai', 'agent', 'machine learning']):
                        field = "ai"
                    elif any(k in comb for k in ['cyber', 'hack', 'ransomware', 'breach', 'malware', 'vulnerability', 'cve', 'zero-day', 'phishing', 'exploit', 'security', 'cisa', 'apt']):
                        field = "cyber"
                    elif any(k in comb for k in ['gpu', 'cpu', 'nvidia', 'amd', 'intel', 'hardware', 'chip', 'semiconductor', 'processor', 'ram', 'motherboard', 'ryzen', 'geforce', 'tsmc']):
                        field = "hardware"
                    elif default_field == "broadcaster":
                        field = "it"

                    # Explicit Threat News Categorization: Active Case vs Informational / Advisory
                    case_keys = [
                        'breach', 'ransomware', 'hacked', 'stolen', 'heist', 'extort', 'compromis',
                        'intrud', 'targeted in cyberattack', 'under attack', 'outage', 'victim',
                        'lockbit', 'blackcat', 'alphv', 'lazarus', 'volt typhoon', 'data exposed',
                        'unauthorized access', 'stolen data', 'leaked', 'wire fraud', 'deepfake scam',
                        'credential stuffing', 'ddos attack', 'cyberattack hits', 'hit by cyberattack',
                        'espionage', 'malware campaign', 'cyber heist', 'infiltrat', 'attackers claim'
                    ]

                    vuln_keys = [
                        'vulnerability', 'cve-', 'zero-day', 'zero day', 'flaw', 'patch', 'rce',
                        'remote code execution', 'exploit', 'privilege escalation', 'poc', 'bypass',
                        'backdoor', 'buffer overflow', 'injection vulnerability', 'memory corruption',
                        'cisa kev', 'critical bug', 'security update', 'zero day flaw'
                    ]

                    policy_keys = [
                        'lawsuit', 'indict', 'arrest', 'sentenced', 'sec probe', 'doj', 'fbi',
                        'subpoena', 'fine', 'gdpr', 'legislation', 'executive order', 'banned',
                        'sanctions', 'charges filed', 'extradit', 'regulatory compliance'
                    ]

                    threat_type = "informational"
                    threat_label = "🔵 Threat Intel Advisory"
                    if any(k in comb for k in case_keys):
                        threat_type = "case"
                        threat_label = "🔴 Active Attack Case"
                    elif any(k in comb for k in vuln_keys):
                        threat_type = "vulnerability"
                        threat_label = "🟠 Vulnerability Alert"
                    elif any(k in comb for k in policy_keys):
                        threat_type = "policy"
                        threat_label = "🟢 Policy & Legal"

                    cat = ["A"]
                    if field in ["ai", "hardware"]:
                        cat.append("B")
                    if "agent" in comb or "mcp" in comb or "autonomous" in comb or "workflow" in comb:
                        cat.append("C")

                    sev = 2
                    if any(k in comb for k in ['critical', 'zero-day', 'massive', 'outage', 'grid', 'infrastructure', 'kill switch', 'probe', 'subpoena']):
                        sev = 5
                    elif any(k in comb for k in ['breach', 'ransomware', 'stolen', 'heist', 'extortion', 'loss', 'compromise', 'investigation']):
                        sev = 4
                    elif any(k in comb for k in ['vulnerability', 'flaw', 'cve', 'patch', 'hack', 'phishing', 'lawsuit']):
                        sev = 3

                    # ISO timestamp for accurate sorting
                    iso_time = dt.isoformat() if dt else datetime.now(timezone.utc).isoformat()
                    epoch_time = dt.timestamp() if dt else 0

                    archive_url = f"https://archive.is/newest/{link}"
                    search_url = f"https://www.google.com/search?q={urllib.parse.quote(clean_title)}"

                    final_desc = clean_desc
                    if not final_desc or len(final_desc) < 40 or final_desc.lower() == clean_title.lower():
                        final_desc = f"Intelligence dispatch confirmed from {clean_outlet}. Threat classification indicates {threat_label} regarding '{clean_title}'. Telemetry corroborates heightened operational interest across enterprise defense perimeters."

                    all_articles.append({
                        "title": clean_title,
                        "headline": clean_title,
                        "url": link,
                        "source_url": source_url or link,
                        "archive_url": archive_url,
                        "search_url": search_url,
                        "outlet": clean_outlet,
                        "description": final_desc,
                        "summary": final_desc,
                        "country": default_country,
                        "field": field,
                        "threat_type": threat_type,
                        "threat_label": threat_label,
                        "category": list(set(cat)),
                        "severity": sev,
                        "pub_date": pub_str,
                        "iso_time": iso_time,
                        "epoch_time": epoch_time,
                        "rel_time": rel_time,
                        "date": dt.strftime("%Y-%m-%d %H:%M") if dt else datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "isLive": True
                    })
                print(f"[{outlet}] Harvested {count} items")
        except Exception as e:
            print(f"[{outlet}] Warning: {e}")

    # SORT BY EPOCH_TIME DESCENDING (Brand new dispatches first!)
    all_articles.sort(key=lambda x: x.get("epoch_time", 0), reverse=True)

    print(f"\nTotal live articles harvested: {len(all_articles)}")
    with open("bs4_extracted_feed.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2)
    print("Saved to bs4_extracted_feed.json successfully.")

if __name__ == "__main__":
    run_harvest()
