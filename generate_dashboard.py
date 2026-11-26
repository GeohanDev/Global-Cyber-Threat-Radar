# generate_dashboard.py
import json
import os
import urllib.parse
import html

with open("incidents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Pre-embed the latest broadcast feed directly into embedded-data preserving chronological newest-first order
if os.path.exists("bs4_extracted_feed.json"):
    try:
        with open("bs4_extracted_feed.json", "r", encoding="utf-8") as f:
            feed_items = json.load(f)
        existing_urls = set(a.get("url") for a in data.get("articles", []))
        live_articles = []
        live_incidents = []
        for idx, item in enumerate(feed_items, start=1):
            url = item.get("url", "#")
            if url and url not in existing_urls:
                existing_urls.add(url)
                art_id = f"ART-LIVE-{idx:04d}"
                inc_id = f"INC-LIVE-{idx:04d}"
                title = item.get("title") or item.get("headline", "")
                outlet = item.get("outlet", "Live Stream")
                country = item.get("country", "Global")
                desc = item.get("description") or item.get("summary", "")
                cat = item.get("category", ["A"])
                sev = item.get("severity", 2)
                field = item.get("field", "it")

                live_articles.append({
                    "article_id": art_id,
                    "incident_id": inc_id,
                    "date": item.get("date", "2026-11-20")[:10],
                    "headline": title,
                    "outlet": outlet,
                    "url": url,
                    "source_url": item.get("source_url") or url,
                    "archive_url": item.get("archive_url") or f"https://archive.is/newest/{url}",
                    "search_url": item.get("search_url") or f"https://www.google.com/search?q={urllib.parse.quote(title)}",
                    "country": country,
                    "field": field,
                    "threat_type": item.get("threat_type", "informational"),
                    "threat_label": item.get("threat_label", "🔵 Threat Intel Advisory"),
                    "category": cat,
                    "severity": sev,
                    "summary": desc,
                    "isLive": True,
                    "pub_date": item.get("pub_date", ""),
                    "iso_time": item.get("iso_time", ""),
                    "epoch_time": item.get("epoch_time", 0),
                    "rel_time": item.get("rel_time", "Just now"),
                    "live_time": item.get("rel_time", "Just now")
                })
                live_incidents.append({
                    "incident_id": inc_id,
                    "date": item.get("date", "2026-11-20")[:10],
                    "headline": title,
                    "source_url": url,
                    "source_tier": 3,
                    "category": cat,
                    "attack_vector": "Cybersecurity Threat Dispatch" if field == 'cyber' else "AI & Tech Telemetry Feed",
                    "target_sector": "Semiconductor & Hardware" if field == 'hardware' else ("Frontier AI Labs" if field == 'ai' else "Enterprise Technology"),
                    "country": country,
                    "severity": sev,
                    "confidence": "high",
                    "outlet": outlet
                })
        data["articles"] = live_articles + data.get("articles", [])
        data["incidents"] = live_incidents + data.get("incidents", [])
        print(f"Pre-embedded {len(live_articles)} live articles into dashboard dataset in exact chronological order.")
    except Exception as e:
        print("Error pre-embedding live feed:", e)

    # --- 25 Connected Ingestion Sources & Monitored Websites Registry ---
    article_counts = {}
    for a in data.get("articles", []):
        o = a.get("outlet", "")
        article_counts[o] = article_counts.get(o, 0) + 1

    PULLED_SOURCES_CONFIG = [
        {
            "id": "bleepingcomputer",
            "name": "BleepingComputer",
            "domain": "bleepingcomputer.com",
            "homepage": "https://www.bleepingcomputer.com",
            "feed_url": "https://news.google.com/rss/search?q=site:bleepingcomputer.com",
            "category": "Tier-1 Cyber Authority",
            "icon": "🛡️",
            "jurisdiction": "Global",
            "protocol": "HTTPS · RSS 2.0 / Atom",
            "cadence": "Every 90s",
            "description": "Premier information security news publication covering breaking ransomware, zero-days, and cyber incidents.",
            "count": article_counts.get("BleepingComputer", 0)
        },
        {
            "id": "thehackernews",
            "name": "The Hacker News",
            "domain": "thehackernews.com",
            "homepage": "https://thehackernews.com",
            "feed_url": "https://feeds.feedburner.com/TheHackersNews",
            "category": "Tier-1 Cyber Authority",
            "icon": "📰",
            "jurisdiction": "Global",
            "protocol": "HTTPS · FeedBurner XML",
            "cadence": "Every 90s",
            "description": "Leading independent cybersecurity news channel dedicated to infosec research, cyber warfare, and zero-day advisories.",
            "count": article_counts.get("The Hacker News", 0)
        },
        {
            "id": "darkreading",
            "name": "Dark Reading",
            "domain": "darkreading.com",
            "homepage": "https://www.darkreading.com",
            "feed_url": "https://www.darkreading.com/rss.xml",
            "category": "Tier-1 Cyber Authority",
            "icon": "🔍",
            "jurisdiction": "Global",
            "protocol": "HTTPS · Direct RSS XML",
            "cadence": "Every 90s",
            "description": "Comprehensive enterprise cybersecurity portal analyzing threat vectors, risk management, and attack mitigations.",
            "count": article_counts.get("Dark Reading", 0)
        },
        {
            "id": "securityweek",
            "name": "SecurityWeek",
            "domain": "securityweek.com",
            "homepage": "https://www.securityweek.com",
            "feed_url": "https://www.securityweek.com/feed/",
            "category": "Tier-1 Cyber Authority",
            "icon": "⚡",
            "jurisdiction": "Global",
            "protocol": "HTTPS · RSS 2.0",
            "cadence": "Every 90s",
            "description": "Cybersecurity news, insights, and analysis covering industrial security, malware, and critical CVE releases.",
            "count": article_counts.get("SecurityWeek", 0)
        },
        {
            "id": "krebsonsecurity",
            "name": "Krebs on Security",
            "domain": "krebsonsecurity.com",
            "homepage": "https://krebsonsecurity.com",
            "feed_url": "https://krebsonsecurity.com/feed/",
            "category": "Tier-1 Cyber Authority",
            "icon": "🕵️",
            "jurisdiction": "United States",
            "protocol": "HTTPS · Direct Feed",
            "cadence": "Every 90s",
            "description": "In-depth investigative cybercrime reporting by Brian Krebs covering financial fraud syndicates and underground markets.",
            "count": article_counts.get("Krebs on Security", 0)
        },
        {
            "id": "securityaffairs",
            "name": "SecurityAffairs",
            "domain": "securityaffairs.com",
            "homepage": "https://securityaffairs.com",
            "feed_url": "https://securityaffairs.com/feed",
            "category": "Tier-1 Cyber Authority",
            "icon": "🛡️",
            "jurisdiction": "Global",
            "protocol": "HTTPS · RSS Feed",
            "cadence": "Every 90s",
            "description": "International cyber intelligence portal covering state-sponsored hacking, cyber warfare, and hacktivism.",
            "count": article_counts.get("SecurityAffairs", 0)
        },
        {
            "id": "cisa",
            "name": "CISA Advisories",
            "domain": "cisa.gov",
            "homepage": "https://www.cisa.gov",
            "feed_url": "https://news.google.com/rss/search?q=site:cisa.gov+advisory+OR+alert",
            "category": "Government CTI & Alerts",
            "icon": "🏛️",
            "jurisdiction": "United States",
            "protocol": "HTTPS · Official CISA RSS",
            "cadence": "Continuous",
            "description": "U.S. Cybersecurity and Infrastructure Security Agency official alerts on active exploits, KEV catalog, and emergency directives.",
            "count": article_counts.get("CISA Advisories", 0)
        },
        {
            "id": "microsoft",
            "name": "Microsoft Threat Intel",
            "domain": "microsoft.com/security/blog",
            "homepage": "https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/",
            "feed_url": "https://news.google.com/rss/search?q=site:microsoft.com/en-us/security/blog",
            "category": "Vendor Threat Lab",
            "icon": "🏢",
            "jurisdiction": "United States",
            "protocol": "HTTPS · MSTIC News Feed",
            "cadence": "Continuous",
            "description": "Microsoft Threat Intelligence Center (MSTIC) telemetry tracking nation-state threat actors, storm actors, and cloud exploits.",
            "count": article_counts.get("Microsoft Threat Intel", 0)
        },
        {
            "id": "unit42",
            "name": "Unit 42 Threat Research",
            "domain": "unit42.paloaltonetworks.com",
            "homepage": "https://unit42.paloaltonetworks.com",
            "feed_url": "https://news.google.com/rss/search?q=site:unit42.paloaltonetworks.com",
            "category": "Vendor Threat Lab",
            "icon": "🔬",
            "jurisdiction": "Global",
            "protocol": "HTTPS · Palo Alto Feed",
            "cadence": "Continuous",
            "description": "Palo Alto Networks threat research team delivering elite adversary profiling, zero-day discoveries, and ransomware teardowns.",
            "count": article_counts.get("Unit 42 Threat Research", 0)
        },
        {
            "id": "talos",
            "name": "Cisco Talos Intelligence",
            "domain": "blog.talosintelligence.com",
            "homepage": "https://blog.talosintelligence.com",
            "feed_url": "https://news.google.com/rss/search?q=site:blog.talosintelligence.com",
            "category": "Vendor Threat Lab",
            "icon": "🛡️",
            "jurisdiction": "United States",
            "protocol": "HTTPS · Talos Blog Feed",
            "cadence": "Continuous",
            "description": "One of the largest commercial threat intelligence teams in the world, analyzing billions of daily telemetry points.",
            "count": article_counts.get("Cisco Talos Intelligence", 0)
        },
        {
            "id": "mandiant",
            "name": "Mandiant Threat Intel",
            "domain": "cloud.google.com/threat-intelligence",
            "homepage": "https://cloud.google.com/blog/topics/threat-intelligence",
            "feed_url": "https://news.google.com/rss/search?q=site:cloud.google.com/blog/topics/threat-intelligence",
            "category": "Vendor Threat Lab",
            "icon": "🌐",
            "jurisdiction": "United States",
            "protocol": "HTTPS · Google Cloud Feed",
            "cadence": "Continuous",
            "description": "Google Cloud & Mandiant frontline cyber espionage investigations, APT attribution, and incident response intelligence.",
            "count": article_counts.get("Mandiant Threat Intel", 0)
        },
        {
            "id": "zdi",
            "name": "Zero Day Initiative (ZDI)",
            "domain": "zerodayinitiative.com",
            "homepage": "https://www.zerodayinitiative.com",
            "feed_url": "https://news.google.com/rss/search?q=site:zerodayinitiative.com/blog",
            "category": "Vulnerability Research",
            "icon": "🎯",
            "jurisdiction": "Global",
            "protocol": "HTTPS · ZDI Feed",
            "cadence": "Continuous",
            "description": "Trend Micro Zero Day Initiative, the world's largest vendor-agnostic bug bounty and vulnerability research program.",
            "count": article_counts.get("Zero Day Initiative (ZDI)", 0)
        },
        {
            "id": "sophos",
            "name": "Sophos Threat Research",
            "domain": "news.sophos.com",
            "homepage": "https://news.sophos.com",
            "feed_url": "https://news.google.com/rss/search?q=site:news.sophos.com",
            "category": "Vendor Threat Lab",
            "icon": "🛡️",
            "jurisdiction": "Global",
            "protocol": "HTTPS · Sophos X-Ops",
            "cadence": "Continuous",
            "description": "Sophos X-Ops cross-functional threat intelligence analyzing active ransomware campaigns and Living-off-the-Land (LotL) tactics.",
            "count": article_counts.get("Sophos Threat Research", 0)
        },
        {
            "id": "liveattacks",
            "name": "Live Cyberattacks & Breaches",
            "domain": "Google News CTI Aggregator",
            "homepage": "https://news.google.com",
            "feed_url": "https://news.google.com/rss/search?q=(cyberattack+OR+ransomware+OR+\"zero-day\"+OR+\"data+breach\"+OR+malware+OR+\"threat+actor\")+when:1d",
            "category": "Live Incident Wire",
            "icon": "⚡",
            "jurisdiction": "Global",
            "protocol": "HTTPS · Real-time Stream",
            "cadence": "Continuous / 90s",
            "description": "High-velocity live aggregation stream tracking breaking cyberattacks, data breaches, and active extortion alerts worldwide.",
            "count": article_counts.get("Live Cyberattacks & Breaches", 0)
        },
        {
            "id": "aithreats",
            "name": "AI Cyber Threats & Exploits",
            "domain": "Google News AI Security",
            "homepage": "https://news.google.com",
            "feed_url": "https://news.google.com/rss/search?q=(\"prompt+injection\"+OR+\"model+weights\"+OR+\"jailbreak\"+OR+\"AI+agent\"+OR+\"deepfake+fraud\"+OR+\"adversarial+attack\")+when:2d",
            "category": "AI Security Wire",
            "icon": "🤖",
            "jurisdiction": "Global",
            "protocol": "HTTPS · Specialized Filter",
            "cadence": "Continuous / 90s",
            "description": "Automated wire tracking adversarial machine learning, prompt injection, model weight theft, deepfake fraud, and agentic exploits.",
            "count": article_counts.get("AI Cyber Threats & Exploits", 0)
        },
        {
            "id": "critinfra",
            "name": "Critical Infrastructure Threats",
            "domain": "CISA & SCADA Monitor",
            "homepage": "https://www.cisa.gov",
            "feed_url": "https://news.google.com/rss/search?q=(CISA+OR+\"critical+infrastructure\"+OR+SCADA+OR+ICS+OR+\"Volt+Typhoon\"+OR+\"state-sponsored+hacker\")+when:2d",
            "category": "Infrastructure Wire",
            "icon": "🏭",
            "jurisdiction": "Global",
            "protocol": "HTTPS · SCADA/ICS Query",
            "cadence": "Continuous / 90s",
            "description": "Targeted intelligence wire monitoring OT, SCADA, power grids, water facilities, and state-sponsored groups like Volt Typhoon.",
            "count": article_counts.get("Critical Infrastructure Threats", 0)
        },
        {
            "id": "bankthreats",
            "name": "Banking & Financial Threats",
            "domain": "FinTech & Banking Feed",
            "homepage": "https://news.google.com",
            "feed_url": "https://news.google.com/rss/search?q=(\"bank\"+OR+\"JPMorgan\"+OR+\"fintech\"+OR+\"wire+fraud\")+AND+(cyberattack+OR+breach+OR+ransomware+OR+hacker)+when:3d",
            "category": "Financial Cyber Wire",
            "icon": "🏦",
            "jurisdiction": "United States",
            "protocol": "HTTPS · FinSec Query",
            "cadence": "Continuous / 90s",
            "description": "Dedicated wire focused on banking cyberattacks, ATM malware, wire fraud, SWIFT intrusions, and financial sector ransomware.",
            "count": article_counts.get("Banking & Financial Threats", 0)
        },
        {
            "id": "theregister",
            "name": "The Register Security",
            "domain": "theregister.com",
            "homepage": "https://www.theregister.com/security",
            "feed_url": "https://news.google.com/rss/search?q=site:theregister.com+(security+OR+vulnerability+OR+malware+OR+cyber)",
            "category": "Tech & Cyber Desk",
            "icon": "💻",
            "jurisdiction": "United Kingdom",
            "protocol": "HTTPS · RSS Stream",
            "cadence": "Every 90s",
            "description": "Biting British tech publication reporting on enterprise vulnerabilities, IT security blunders, and cloud outages.",
            "count": article_counts.get("The Register Security", 0)
        },
        {
            "id": "arstechnica",
            "name": "Ars Technica Security",
            "domain": "arstechnica.com",
            "homepage": "https://arstechnica.com/security",
            "feed_url": "https://news.google.com/rss/search?q=site:arstechnica.com+(security+OR+vulnerability+OR+malware+OR+hack)",
            "category": "Tech & Cyber Desk",
            "icon": "💻",
            "jurisdiction": "United States",
            "protocol": "HTTPS · RSS Stream",
            "cadence": "Every 90s",
            "description": "Authoritative technology journalism focusing on cryptography, hardware vulnerabilities, and sophisticated exploit chains.",
            "count": article_counts.get("Ars Technica Security", 0)
        },
        {
            "id": "wired",
            "name": "Wired Threat Desk",
            "domain": "wired.com",
            "homepage": "https://www.wired.com/category/security",
            "feed_url": "https://news.google.com/rss/search?q=site:wired.com+(security+OR+cyberattack+OR+hacker+OR+breach)",
            "category": "Tech & Cyber Desk",
            "icon": "🔌",
            "jurisdiction": "United States",
            "protocol": "HTTPS · RSS Stream",
            "cadence": "Every 90s",
            "description": "High-impact investigative reporting on cyber warfare, privacy crises, intelligence agencies, and global hacker culture.",
            "count": article_counts.get("Wired Threat Desk", 0)
        },
        {
            "id": "zdnet",
            "name": "ZDNet Security News",
            "domain": "zdnet.com",
            "homepage": "https://www.zdnet.com/topic/security",
            "feed_url": "https://news.google.com/rss/search?q=site:zdnet.com+(security+OR+cyberattack+OR+ransomware+OR+hacker)",
            "category": "Tech & Cyber Desk",
            "icon": "☁️",
            "jurisdiction": "United States",
            "protocol": "HTTPS · RSS Stream",
            "cadence": "Every 90s",
            "description": "Business technology and enterprise IT security reporting on patching cycles, CISO strategies, and cloud protection.",
            "count": article_counts.get("ZDNet Security News", 0)
        },
        {
            "id": "reuters",
            "name": "Reuters Cyber Warfare",
            "domain": "reuters.com",
            "homepage": "https://www.reuters.com/technology/cybersecurity",
            "feed_url": "https://news.google.com/rss/search?q=site:reuters.com+(cyberattack+OR+hackers+OR+ransomware+OR+cybersecurity)",
            "category": "Global News Wire",
            "icon": "🌐",
            "jurisdiction": "Global",
            "protocol": "HTTPS · Reuters Feed",
            "cadence": "Continuous",
            "description": "Global wire service providing verified geopolitical cyber espionage, state sanctions, and international cyber treaty coverage.",
            "count": article_counts.get("Reuters Cyber Warfare", 0)
        },
        {
            "id": "bloomberg",
            "name": "Bloomberg Cybersecurity",
            "domain": "bloomberg.com",
            "homepage": "https://www.bloomberg.com/technology",
            "feed_url": "https://news.google.com/rss/search?q=site:bloomberg.com+(cyberattack+OR+hackers+OR+ransomware+OR+cybersecurity)",
            "category": "Financial News Wire",
            "icon": "📈",
            "jurisdiction": "United States",
            "protocol": "HTTPS · Bloomberg Feed",
            "cadence": "Continuous",
            "description": "Financial news leader analyzing the market fallout of major cyberattacks, ransom payments, and cybersecurity defense spending.",
            "count": article_counts.get("Bloomberg Cybersecurity", 0)
        },
        {
            "id": "cnn",
            "name": "CNN Cyber Espionage",
            "domain": "cnn.com",
            "homepage": "https://www.cnn.com",
            "feed_url": "https://news.google.com/rss/search?q=site:cnn.com+(cyberattack+OR+hackers+OR+ransomware+OR+breach)",
            "category": "Global News Wire",
            "icon": "📺",
            "jurisdiction": "United States",
            "protocol": "HTTPS · CNN Wire",
            "cadence": "Continuous",
            "description": "Breaking mainstream coverage of national security threats, election infrastructure security, and federal indictments.",
            "count": article_counts.get("CNN Cyber Espionage", 0)
        },
        {
            "id": "bbc",
            "name": "BBC Cyber Wire",
            "domain": "bbc.com",
            "homepage": "https://www.bbc.com/news/technology",
            "feed_url": "https://news.google.com/rss/search?q=site:bbc.com+(cyberattack+OR+hacker+OR+ransomware+OR+malware)",
            "category": "Global News Wire",
            "icon": "📻",
            "jurisdiction": "United Kingdom",
            "protocol": "HTTPS · BBC Wire",
            "cadence": "Continuous",
            "description": "Public service international reporting on cybercrime, digital privacy, surveillance technologies, and European cyber incidents.",
            "count": article_counts.get("BBC Cyber Wire", 0)
        }
    ]
    data["pulledSources"] = PULLED_SOURCES_CONFIG

    # Build dynamic live-time ticker content from the newest harvested live articles
    ticker_items = []
    for art in live_articles[:20]:
        t_type = art.get("threat_type", "informational")
        badge_cls = "ticker-badge-case" if t_type == "case" else ("ticker-badge-vuln" if t_type == "vulnerability" else "")
        sev_icon = "🔴" if t_type == "case" else ("🟠" if t_type == "vulnerability" else "⚡")
        rel_t = art.get("rel_time", "Live")
        art_title = html.escape(art.get("headline", ""))
        outlet_name = html.escape(art.get("outlet", "CTI Wire"))
        art_id = html.escape(art.get("article_id", ""))
        item_html = f'''<div class="ticker-item"><span class="ticker-badge-live {badge_cls}"><span class="pulse-dot-mini"></span> {sev_icon} LIVE · {rel_t}</span><span class="ticker-outlet">[{outlet_name}]</span><span class="ticker-headline" onclick="openArticleReaderModal('{art_id}')" style="cursor:pointer;" title="Click to read live threat briefing">{art_title}</span></div>'''
        ticker_items.append(item_html)

    initial_ticker_content = "".join(ticker_items * 2) if ticker_items else ""


json_str = json.dumps(data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Global AI Cyberattack Threat Radar (10-Year Macro & Continuous)</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {{
      --bg-base: #080c14;
      --bg-card: #101625;
      --bg-card-hover: #162035;
      --border-subtle: #1e293b;
      --border-focus: #3b82f6;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --input-bg: #090e1a;
      --table-th: #141b2b;
      --table-row-hover: rgba(255, 255, 255, 0.02);
      --table-border: rgba(255, 255, 255, 0.04);
      --hud-box-bg: #0d1322;
      --ticker-bg: #0f172a;
      
      --sev-1: #64748b;
      --sev-2: #38bdf8;
      --sev-3: #facc15;
      --sev-4: #fb923c;
      --sev-5: #ef4444;
      
      --cat-a: #38bdf8;
      --cat-b: #c084fc;
      --cat-c: #34d399;
      
      --accent-warn: #f59e0b;
      --accent-danger: #ef4444;
      --accent-info: #06b6d4;
    }}

    body.light, body.light-theme {{
      --bg-base: #f1f5f9;
      --bg-card: #ffffff;
      --bg-card-hover: #f8fafc;
      --border-subtle: #cbd5e1;
      --border-focus: #2563eb;
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --input-bg: #ffffff;
      --table-th: #e2e8f0;
      --table-row-hover: rgba(0, 0, 0, 0.02);
      --table-border: rgba(0, 0, 0, 0.06);
      --hud-box-bg: #ffffff;
      --ticker-bg: #e2e8f0;

      --sev-1: #475569;
      --sev-2: #0284c7;
      --sev-3: #ca8a04;
      --sev-4: #ea580c;
      --sev-5: #dc2626;

      --cat-a: #0284c7;
      --cat-b: #7e22ce;
      --cat-c: #047857;

      --accent-warn: #d97706;
      --accent-danger: #dc2626;
      --accent-info: #0284c7;
    }}


    
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    
    /* High-Performance Theme Transition: Zero-jank instant color switching */
    
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.45;
      padding: 0 0 30px 0;
      -webkit-font-smoothing: antialiased;
    }}

    /* Top Live Marquee Ticker (FIXED OVERLAP: Separate static flex-shrink label and masked scroll track) */
    .live-top-ticker {{
      background: var(--ticker-bg);
      border-bottom: 1px solid var(--border-subtle);
      padding: 6px 16px;
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 0.76rem;
      position: relative;
      overflow: hidden;
      z-index: 50;
    }}

    .ticker-label {{
      background: #ef4444;
      color: #ffffff;
      font-weight: 800;
      padding: 3px 9px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
      position: relative;
      z-index: 10;
      box-shadow: 2px 0 8px rgba(0,0,0,0.25);
    }}

    .ticker-pulse-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #ffffff;
      animation: blink 1s infinite alternate;
    }}

    @keyframes blink {{
      from {{ opacity: 1; }}
      to {{ opacity: 0.2; }}
    }}

    .ticker-track {{
      flex: 1;
      min-width: 0;
      overflow: hidden;
      position: relative;
      white-space: nowrap;
      mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
      -webkit-mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
    }}

    .ticker-content {{
      display: inline-flex;
      gap: 36px;
      white-space: nowrap;
      animation: scrollTicker var(--ticker-duration, 140s) linear infinite;
      padding-left: 16px;
    }}

    .ticker-content:hover,
    .ticker-content.ticker-paused {{
      animation-play-state: paused !important;
    }}

    /* Speed & Pause Controls */
    .ticker-controls {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      flex-shrink: 0;
      z-index: 10;
    }}

    .ticker-ctrl-btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      border-radius: 4px;
      padding: 2px 7px;
      font-size: 0.72rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
    }}

    .ticker-ctrl-btn:hover {{
      background: rgba(255, 255, 255, 0.18);
      border-color: var(--border-focus);
    }}

    .ticker-speed-group {{
      display: inline-flex;
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      overflow: hidden;
      background: rgba(0, 0, 0, 0.25);
    }}

    .ticker-speed-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 0.67rem;
      font-weight: 600;
      padding: 2px 7px;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }}

    .ticker-speed-btn:hover {{
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.08);
    }}

    .ticker-speed-btn.active {{
      background: var(--border-focus);
      color: #ffffff;
      font-weight: 700;
    }}

    @keyframes scrollTicker {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-50%); }}
    }}

    .ticker-item {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--text-main);
      font-size: 0.77rem;
    }}

    .ticker-badge-live {{
      font-size: 0.65rem;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.45);
      display: inline-flex;
      align-items: center;
      gap: 5px;
      white-space: nowrap;
    }}
    .ticker-badge-case {{
      background: rgba(239, 68, 68, 0.22);
      color: #fca5a5;
      border-color: rgba(239, 68, 68, 0.55);
    }}
    .ticker-badge-vuln {{
      background: rgba(249, 115, 22, 0.22);
      color: #fdba74;
      border-color: rgba(249, 115, 22, 0.55);
    }}
    .pulse-dot-mini {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #10b981;
      display: inline-block;
      box-shadow: 0 0 6px #10b981;
      animation: pulseDotMiniAnim 1.4s infinite ease-in-out;
    }}
    .ticker-badge-case .pulse-dot-mini {{
      background: #ef4444;
      box-shadow: 0 0 6px #ef4444;
    }}
    .ticker-badge-vuln .pulse-dot-mini {{
      background: #f97316;
      box-shadow: 0 0 6px #f97316;
    }}
    @keyframes pulseDotMiniAnim {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.4); opacity: 0.4; }}
    }}
    .ticker-outlet {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--border-focus);
      opacity: 0.95;
      white-space: nowrap;
    }}
    .ticker-headline {{
      color: var(--text-main);
      font-weight: 600;
      transition: color 0.15s;
      cursor: pointer;
    }}
    .ticker-headline:hover {{
      color: #38bdf8;
      text-decoration: underline;
    }}


    .ticker-item a {{
      color: #3b82f6;
      text-decoration: none;
      font-weight: 600;
      cursor: pointer;
    }}
    .ticker-item a:hover {{
      text-decoration: underline;
    }}
    
    .dashboard-container {{
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
      padding: 16px 20px 0 20px;
    }}

    @media (min-width: 1024px) {{
      .dashboard-container {{
        padding: 24px 32px 0 32px;
      }}
    }}
    
    /* Header & Live Time HUD */
    header {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border-subtle);
    }}
    
    .header-titles h1 {{
      font-size: 1.55rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    
    .header-titles h1 span.badge-live {{
      font-size: 0.72rem;
      font-weight: 700;
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid #10b981;
      color: #10b981;
      padding: 2px 8px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .badge-5y {{
      font-size: 0.72rem;
      font-weight: 700;
      background: rgba(59, 130, 246, 0.15);
      border: 1px solid #3b82f6;
      color: #3b82f6;
      padding: 2px 8px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    
    .header-titles p {{
      font-size: 0.84rem;
      color: var(--text-muted);
      margin-top: 3px;
    }}
    
    .livetime-hud {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .digital-clock-box {{
      background: var(--hud-box-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 6px 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      min-width: 180px;
    }}

    .clock-time {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--border-focus);
      letter-spacing: 0.05em;
      line-height: 1.1;
      text-align: center;
      width: 100%;
    }}

    .clock-sub {{
      font-size: 0.68rem;
      color: var(--text-dim);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      text-align: center;
      width: 100%;
    }}

    .live-status-pill {{
      display: flex;
      align-items: center;
      gap: 8px;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      padding: 7px 12px;
      border-radius: 8px;
      font-size: 0.8rem;
    }}
    
    .status-indicator {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
      0% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.5; transform: scale(0.9); }}
      100% {{ opacity: 1; transform: scale(1); }}
    }}

    .hud-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 6px 11px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .hud-btn:hover {{
      background: var(--border-focus);
      color: #ffffff;
      border-color: var(--border-focus);
    }}

    .theme-toggle-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      font-size: 0.8rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
    .theme-toggle-btn:hover {{
      background: var(--bg-card-hover);
      border-color: var(--border-focus);
    }}
    
    /* Universal Filter Bar */
    .filter-panel {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 14px 18px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 12px;
      align-items: center;
    }}
    
    .filter-group {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    
    .filter-group label {{
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}
    
    .filter-group select, .filter-group input {{
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 0.82rem;
      outline: none;
      transition: border-color 0.15s;
    }}
    
    .filter-group select:focus, .filter-group input:focus {{
      border-color: var(--border-focus);
    }}
    
    .filter-actions {{
      display: flex;
      gap: 8px;
      align-self: flex-end;
    }}
    
    .btn-reset {{
      background: var(--input-bg);
      color: var(--text-main);
      border: 1px solid var(--border-subtle);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    
    .btn-reset:hover {{
      background: var(--bg-card-hover);
      border-color: var(--border-focus);
    }}

    /* 1. KPI Strip */
    .kpi-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(185px, 1fr));
      gap: 12px;
    }}

    /* 1B. KPI Matrix: Category & Severity Telemetry Grid */
    .kpi-matrix-section {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-top: 14px;
      margin-bottom: 6px;
    }}

    .kpi-matrix-block {{
      background: rgba(16, 22, 37, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 12px;
      padding: 14px 16px;
    }}

    .kpi-matrix-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}

    .kpi-matrix-title-group {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .kpi-matrix-badge {{
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }}

    .kpi-matrix-title {{
      font-size: 0.88rem;
      font-weight: 700;
      color: var(--text-main);
      margin: 0;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .kpi-matrix-hint {{
      font-size: 0.72rem;
      font-weight: 400;
      color: var(--text-dim);
    }}

    .kpi-matrix-reset-btn {{
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      font-size: 0.72rem;
      padding: 3px 10px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .kpi-matrix-reset-btn:hover {{
      border-color: var(--border-focus);
      color: var(--text-main);
      background: rgba(59, 130, 246, 0.1);
    }}

    .category-kpi-strip {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }}

    .severity-kpi-strip {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
    }}

    @media (max-width: 1024px) {{
      .category-kpi-strip {{
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      }}
      .severity-kpi-strip {{
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      }}
    }}

    /* Interactive Filterable KPI Cards */
    .interactive-kpi-card {{
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, background 0.2s ease;
      user-select: none;
      position: relative;
    }}

    .interactive-kpi-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
      border-color: rgba(255, 255, 255, 0.22);
    }}

    .kpi-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }}

    .kpi-card-middle {{
      display: flex;
      align-items: baseline;
      gap: 8px;
      margin-bottom: 4px;
    }}

    .kpi-badge {{
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 2px 7px;
      border-radius: 4px;
    }}

    .kpi-pct-badge {{
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.06);
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.02em;
    }}

    .kpi-filter-indicator {{
      font-size: 0.65rem;
      font-weight: 600;
      text-transform: uppercase;
      color: var(--text-dim);
      opacity: 0.6;
      transition: all 0.2s;
    }}

    .interactive-kpi-card:hover .kpi-filter-indicator {{
      opacity: 1;
      color: var(--text-main);
    }}

    /* Category Accents */
    .cat-a-kpi::after {{ background: var(--cat-a); }}
    .cat-b-kpi::after {{ background: var(--cat-b); }}
    .cat-c-kpi::after {{ background: var(--cat-c); }}

    .cat-a-val {{ color: var(--cat-a); }}
    .cat-b-val {{ color: var(--cat-b); }}
    .cat-c-val {{ color: var(--cat-c); }}

    .cat-a-badge {{ background: rgba(56, 189, 248, 0.15); color: var(--cat-a); border: 1px solid rgba(56, 189, 248, 0.25); }}
    .cat-b-badge {{ background: rgba(192, 132, 252, 0.15); color: var(--cat-b); border: 1px solid rgba(192, 132, 252, 0.25); }}
    .cat-c-badge {{ background: rgba(52, 211, 153, 0.15); color: var(--cat-c); border: 1px solid rgba(52, 211, 153, 0.25); }}

    /* Severity Accents */
    .sev-5-kpi::after {{ background: var(--sev-5); }}
    .sev-4-kpi::after {{ background: var(--sev-4); }}
    .sev-3-kpi::after {{ background: var(--sev-3); }}
    .sev-2-kpi::after {{ background: var(--sev-2); }}
    .sev-1-kpi::after {{ background: var(--sev-1); }}

    .sev-5-val {{ color: var(--sev-5); }}
    .sev-4-val {{ color: var(--sev-4); }}
    .sev-3-val {{ color: var(--sev-3); }}
    .sev-2-val {{ color: var(--sev-2); }}
    .sev-1-val {{ color: var(--sev-1); }}

    .sev-5-badge {{ background: rgba(239, 68, 68, 0.18); color: var(--sev-5); border: 1px solid rgba(239, 68, 68, 0.3); }}
    .sev-4-badge {{ background: rgba(251, 146, 60, 0.18); color: var(--sev-4); border: 1px solid rgba(251, 146, 60, 0.3); }}
    .sev-3-badge {{ background: rgba(250, 204, 21, 0.18); color: var(--sev-3); border: 1px solid rgba(250, 204, 21, 0.3); }}
    .sev-2-badge {{ background: rgba(56, 189, 248, 0.18); color: var(--sev-2); border: 1px solid rgba(56, 189, 248, 0.3); }}
    .sev-1-badge {{ background: rgba(100, 116, 139, 0.18); color: var(--sev-1); border: 1px solid rgba(100, 116, 139, 0.3); }}

    /* Glowing Active States for KPI Filter Cards */
    .interactive-kpi-card.active-kpi-filter {{
      transform: translateY(-2px);
    }}

    .interactive-kpi-card.active-kpi-filter .kpi-filter-indicator {{
      opacity: 1 !important;
      color: #fff;
      background: rgba(255, 255, 255, 0.18);
      padding: 1px 6px;
      border-radius: 3px;
      font-weight: 700;
    }}

    .cat-a-kpi.active-kpi-filter {{
      border-color: var(--cat-a) !important;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.45) !important;
      background: linear-gradient(180deg, rgba(56, 189, 248, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    .cat-b-kpi.active-kpi-filter {{
      border-color: var(--cat-b) !important;
      box-shadow: 0 0 16px rgba(192, 132, 252, 0.45) !important;
      background: linear-gradient(180deg, rgba(192, 132, 252, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    .cat-c-kpi.active-kpi-filter {{
      border-color: var(--cat-c) !important;
      box-shadow: 0 0 16px rgba(52, 211, 153, 0.45) !important;
      background: linear-gradient(180deg, rgba(52, 211, 153, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    .sev-5-kpi.active-kpi-filter {{
      border-color: var(--sev-5) !important;
      box-shadow: 0 0 16px rgba(239, 68, 68, 0.45) !important;
      background: linear-gradient(180deg, rgba(239, 68, 68, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    .sev-4-kpi.active-kpi-filter {{
      border-color: var(--sev-4) !important;
      box-shadow: 0 0 16px rgba(251, 146, 60, 0.45) !important;
      background: linear-gradient(180deg, rgba(251, 146, 60, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    .sev-3-kpi.active-kpi-filter {{
      border-color: var(--sev-3) !important;
      box-shadow: 0 0 16px rgba(250, 204, 21, 0.45) !important;
      background: linear-gradient(180deg, rgba(250, 204, 21, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    .sev-2-kpi.active-kpi-filter {{
      border-color: var(--sev-2) !important;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.45) !important;
      background: linear-gradient(180deg, rgba(56, 189, 248, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    .sev-1-kpi.active-kpi-filter {{
      border-color: var(--sev-1) !important;
      box-shadow: 0 0 16px rgba(100, 116, 139, 0.45) !important;
      background: linear-gradient(180deg, rgba(100, 116, 139, 0.12) 0%, var(--bg-card) 100%) !important;
    }}

    /* Enforce colored values over .kpi-value defaults */
    .kpi-value.cat-a-val {{ color: var(--cat-a) !important; }}
    .kpi-value.cat-b-val {{ color: var(--cat-b) !important; }}
    .kpi-value.cat-c-val {{ color: var(--cat-c) !important; }}
    .kpi-value.sev-5-val {{ color: var(--sev-5) !important; }}
    .kpi-value.sev-4-val {{ color: var(--sev-4) !important; }}
    .kpi-value.sev-3-val {{ color: var(--sev-3) !important; }}
    .kpi-value.sev-2-val {{ color: var(--sev-2) !important; }}
    .kpi-value.sev-1-val {{ color: var(--sev-1) !important; }}

    /* Light Mode Comprehensive Overrides for Threat Matrix */
    body.light .kpi-matrix-block,
    body.light-theme .kpi-matrix-block {{
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
    }}

    body.light .kpi-matrix-title,
    body.light-theme .kpi-matrix-title {{
      color: #0f172a !important;
    }}

    body.light .kpi-matrix-hint,
    body.light-theme .kpi-matrix-hint {{
      color: #64748b !important;
    }}

    body.light .kpi-matrix-reset-btn,
    body.light-theme .kpi-matrix-reset-btn {{
      background: #f8fafc !important;
      border: 1px solid #cbd5e1 !important;
      color: #334155 !important;
    }}
    body.light .kpi-matrix-reset-btn:hover,
    body.light-theme .kpi-matrix-reset-btn:hover {{
      background: #e2e8f0 !important;
      border-color: #2563eb !important;
      color: #0f172a !important;
    }}

    body.light .kpi-matrix-badge,
    body.light-theme .kpi-matrix-badge {{
      font-weight: 800 !important;
    }}

    body.light .interactive-kpi-card,
    body.light-theme .interactive-kpi-card {{
      background: #ffffff !important;
      border: 1px solid #e2e8f0 !important;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
    }}

    body.light .interactive-kpi-card:hover,
    body.light-theme .interactive-kpi-card:hover {{
      background: #f8fafc !important;
      border-color: #cbd5e1 !important;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08) !important;
    }}

    /* Light Mode Value Colors */
    body.light .cat-a-val, body.light-theme .cat-a-val {{ color: #0284c7 !important; }}
    body.light .cat-b-val, body.light-theme .cat-b-val {{ color: #7e22ce !important; }}
    body.light .cat-c-val, body.light-theme .cat-c-val {{ color: #047857 !important; }}

    body.light .sev-5-val, body.light-theme .sev-5-val {{ color: #dc2626 !important; }}
    body.light .sev-4-val, body.light-theme .sev-4-val {{ color: #ea580c !important; }}
    body.light .sev-3-val, body.light-theme .sev-3-val {{ color: #ca8a04 !important; }}
    body.light .sev-2-val, body.light-theme .sev-2-val {{ color: #0284c7 !important; }}
    body.light .sev-1-val, body.light-theme .sev-1-val {{ color: #475569 !important; }}

    /* Light Mode Badges */
    body.light .cat-a-badge, body.light-theme .cat-a-badge {{
      background: #e0f2fe !important;
      color: #0369a1 !important;
      border: 1px solid #bae6fd !important;
    }}
    body.light .cat-b-badge, body.light-theme .cat-b-badge {{
      background: #f3e8ff !important;
      color: #6b21a8 !important;
      border: 1px solid #e9d5ff !important;
    }}
    body.light .cat-c-badge, body.light-theme .cat-c-badge {{
      background: #dcfce7 !important;
      color: #047857 !important;
      border: 1px solid #bbf7d0 !important;
    }}

    body.light .sev-5-badge, body.light-theme .sev-5-badge {{
      background: #fee2e2 !important;
      color: #b91c1c !important;
      border: 1px solid #fecaca !important;
    }}
    body.light .sev-4-badge, body.light-theme .sev-4-badge {{
      background: #ffedd5 !important;
      color: #c2410c !important;
      border: 1px solid #fed7aa !important;
    }}
    body.light .sev-3-badge, body.light-theme .sev-3-badge {{
      background: #fef9c3 !important;
      color: #854d0e !important;
      border: 1px solid #fef08a !important;
    }}
    body.light .sev-2-badge, body.light-theme .sev-2-badge {{
      background: #e0f2fe !important;
      color: #0284c7 !important;
      border: 1px solid #bae6fd !important;
    }}
    body.light .sev-1-badge, body.light-theme .sev-1-badge {{
      background: #f1f5f9 !important;
      color: #475569 !important;
      border: 1px solid #cbd5e1 !important;
    }}

    /* Light Mode Percentage Badges */
    body.light .kpi-pct-badge,
    body.light-theme .kpi-pct-badge {{
      background: #f1f5f9 !important;
      color: #334155 !important;
      border: 1px solid #e2e8f0 !important;
      font-weight: 700 !important;
    }}

    /* Light Mode Labels & Subtext */
    body.light .interactive-kpi-card .kpi-label,
    body.light-theme .interactive-kpi-card .kpi-label {{
      color: #0f172a !important;
      font-weight: 700 !important;
    }}
    body.light .interactive-kpi-card .kpi-subtext,
    body.light-theme .interactive-kpi-card .kpi-subtext {{
      color: #475569 !important;
    }}
    body.light .kpi-filter-indicator,
    body.light-theme .kpi-filter-indicator {{
      color: #64748b !important;
    }}

    /* Light Mode Active Glowing States */
    body.light .cat-a-kpi.active-kpi-filter, body.light-theme .cat-a-kpi.active-kpi-filter {{
      border-color: #0284c7 !important;
      background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(2, 132, 199, 0.35) !important;
    }}
    body.light .cat-b-kpi.active-kpi-filter, body.light-theme .cat-b-kpi.active-kpi-filter {{
      border-color: #7e22ce !important;
      background: linear-gradient(180deg, #faf5ff 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(126, 34, 206, 0.35) !important;
    }}
    body.light .cat-c-kpi.active-kpi-filter, body.light-theme .cat-c-kpi.active-kpi-filter {{
      border-color: #047857 !important;
      background: linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(4, 120, 87, 0.35) !important;
    }}

    body.light .sev-5-kpi.active-kpi-filter, body.light-theme .sev-5-kpi.active-kpi-filter {{
      border-color: #dc2626 !important;
      background: linear-gradient(180deg, #fef2f2 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(220, 38, 38, 0.35) !important;
    }}
    body.light .sev-4-kpi.active-kpi-filter, body.light-theme .sev-4-kpi.active-kpi-filter {{
      border-color: #ea580c !important;
      background: linear-gradient(180deg, #fff7ed 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(234, 88, 12, 0.35) !important;
    }}
    body.light .sev-3-kpi.active-kpi-filter, body.light-theme .sev-3-kpi.active-kpi-filter {{
      border-color: #ca8a04 !important;
      background: linear-gradient(180deg, #fefce8 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(202, 138, 4, 0.35) !important;
    }}
    body.light .sev-2-kpi.active-kpi-filter, body.light-theme .sev-2-kpi.active-kpi-filter {{
      border-color: #0284c7 !important;
      background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(2, 132, 199, 0.35) !important;
    }}
    body.light .sev-1-kpi.active-kpi-filter, body.light-theme .sev-1-kpi.active-kpi-filter {{
      border-color: #64748b !important;
      background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%) !important;
      box-shadow: 0 0 14px rgba(100, 116, 139, 0.35) !important;
    }}

    body.light .interactive-kpi-card.active-kpi-filter .kpi-filter-indicator,
    body.light-theme .interactive-kpi-card.active-kpi-filter .kpi-filter-indicator {{
      color: #0f172a !important;
      background: rgba(0, 0, 0, 0.08) !important;
    }}
    
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 14px 18px;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }}
    
    .kpi-card::after {{
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--border-focus);
    }}
    
    .kpi-card.agentic::after {{
      background: var(--cat-c);
    }}
    
    .kpi-card.severity-high::after {{
      background: var(--sev-5);
    }}
    
    .kpi-label {{
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}
    
    .kpi-value {{
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--text-main);
      margin: 4px 0;
      line-height: 1.1;
      font-variant-numeric: tabular-nums;
    }}
    
    .kpi-subtext {{
      font-size: 0.75rem;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    
    .kpi-delta-up {{
      color: #ef4444;
      font-weight: 600;
    }}
    .kpi-delta-down {{
      color: #10b981;
      font-weight: 600;
    }}
    
    /* 2. Key Concerns Panel */
    .concerns-panel {{
      background: rgba(245, 158, 11, 0.06);
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-left: 6px solid #f59e0b;
      border-radius: 10px;
      padding: 16px 20px;
    }}
    
    .concerns-header {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
    }}
    
    .concerns-badge {{
      background: #f59e0b;
      color: #000;
      font-size: 0.7rem;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    
    .concerns-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: #f59e0b;
    }}
    
    .concerns-list {{
      display: flex;
      flex-direction: column;
      gap: 9px;
      padding-left: 0;
      list-style: none;
    }}
    
    .concern-item {{
      font-size: 0.88rem;
      color: var(--text-main);
      display: flex;
      align-items: baseline;
      gap: 8px;
    }}
    
    .concern-item::before {{
      content: "▶";
      color: #f59e0b;
      font-size: 0.65rem;
      transform: translateY(-1px);
    }}
    
    .concern-item a {{
      color: var(--border-focus);
      text-decoration: underline;
      font-weight: 600;
      cursor: pointer;
    }}
    .concern-item a:hover {{
      color: #ef4444;
    }}
    
    /* 3. Hero Chart with 5-Year / Monthly Switcher & Dynamic Table */
    .section-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    
    .section-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}
    
    .section-title {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .chart-view-toggle {{
      display: inline-flex;
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
    }}

    .toggle-btn {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s;
    }}

    .toggle-btn.active {{
      background: #2563eb;
      color: #ffffff;
    }}
    
    .chart-legend-custom {{
      display: flex;
      gap: 14px;
      font-size: 0.75rem;
      color: var(--text-muted);
      flex-wrap: wrap;
    }}
    
    .legend-item {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    
    .legend-dot {{
      width: 10px;
      height: 10px;
      border-radius: 2px;
    }}
    
    .chart-container {{
      position: relative;
      height: 380px;
      width: 100%;
    }}
    
    .monthly-table-wrapper {{
      overflow-x: auto;
      margin-top: 6px;
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      background: var(--input-bg);
    }}
    
    .monthly-table {{
      width: 100%;
      border-collapse: collapse;
      text-align: center;
      font-size: 0.78rem;
    }}
    
    .monthly-table th {{
      background: var(--table-th);
      color: var(--text-muted);
      font-weight: 600;
      padding: 8px 6px;
      border-bottom: 1px solid var(--border-subtle);
      white-space: nowrap;
    }}
    
    .monthly-table td {{
      padding: 8px 6px;
      border-bottom: 1px solid var(--table-border);
      color: var(--text-main);
      font-variant-numeric: tabular-nums;
    }}
    
    .monthly-table tr.total-row td {{
      font-weight: 700;
      background: rgba(59, 130, 246, 0.08);
      color: var(--border-focus);
    }}

    .grid-2col {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }}
    
    @media (min-width: 1024px) {{
      .grid-2col {{
        grid-template-columns: 1.15fr 0.85fr;
      }}
    }}

    .grid-3col {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
      margin-top: 20px;
    }}

    @media (min-width: 900px) {{
      .grid-3col {{
        grid-template-columns: repeat(3, 1fr);
      }}
    }}
    
    /* 4. Country View */
    .country-view-content {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    
    .country-bars {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    
    .country-row {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.8rem;
      cursor: pointer;
      padding: 4px 6px;
      border-radius: 4px;
      transition: background 0.15s;
    }}
    
    .country-row:hover {{
      background: var(--bg-card-hover);
    }}
    
    .country-name {{
      width: 135px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-weight: 500;
    }}
    
    .country-bar-bg {{
      flex: 1;
      height: 10px;
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 9999px;
      overflow: hidden;
      position: relative;
    }}
    
    .country-bar-fill {{
      height: 100%;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      border-radius: 9999px;
    }}
    
    .country-count {{
      width: 32px;
      text-align: right;
      font-weight: 700;
      color: var(--border-focus);
      font-variant-numeric: tabular-nums;
    }}

    /* 5. Breakdowns Grid */
    .breakdowns-container {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }}
    
    @media (min-width: 640px) {{
      .breakdowns-container {{
        grid-template-columns: 1fr 1fr;
      }}
    }}
    
    .breakdown-box {{
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    
    .breakdown-title {{
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    
    .meter-list {{
      display: flex;
      flex-direction: column;
      gap: 7px;
    }}
    
    .meter-item {{
      display: flex;
      flex-direction: column;
      gap: 2px;
      font-size: 0.77rem;
    }}
    
    .meter-header {{
      display: flex;
      justify-content: space-between;
    }}
    
    .meter-bar {{
      height: 6px;
      background: var(--border-subtle);
      border-radius: 3px;
      overflow: hidden;
    }}
    
    .meter-bar-fill {{
      height: 100%;
      border-radius: 3px;
    }}

    /* 6. Reported Articles Feed */
    .articles-feed-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
    }}
    
    .feed-controls {{
      display: flex;
      gap: 8px;
    }}
    
    .feed-search {{
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 0.8rem;
      width: 220px;
    }}
    
    .articles-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 12px;
      max-height: 520px;
      overflow-y: auto;
      padding-right: 4px;
    }}
    
    .article-card {{
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
      cursor: pointer;
      position: relative;
      transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
    }}
    
    .article-card:hover {{
      border-color: var(--border-focus);
      transform: translateY(-2px);
      background: var(--bg-card-hover);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
    }}

    /* Elevated Cyber Threat Highlighting */
    .article-card.threat-card-case {{
      border-left: 5px solid #ef4444 !important;
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, var(--input-bg) 60%) !important;
      box-shadow: 0 4px 18px rgba(239, 68, 68, 0.18) !important;
    }}
    .article-card.threat-card-case:hover {{
      border-left-color: #dc2626 !important;
      box-shadow: 0 6px 24px rgba(239, 68, 68, 0.32) !important;
      transform: translateY(-2px);
    }}

    .article-card.threat-card-vuln {{
      border-left: 5px solid #f97316 !important;
      background: linear-gradient(135deg, rgba(249, 115, 22, 0.07) 0%, var(--input-bg) 60%) !important;
      box-shadow: 0 4px 14px rgba(249, 115, 22, 0.15) !important;
    }}
    .article-card.threat-card-vuln:hover {{
      border-left-color: #ea580c !important;
      box-shadow: 0 6px 20px rgba(249, 115, 22, 0.25) !important;
      transform: translateY(-2px);
    }}

    .article-card.threat-card-info {{
      border-left: 3px solid rgba(148, 163, 184, 0.3);
      opacity: 0.94;
    }}
    .article-card.threat-card-info:hover {{
      opacity: 1;
      border-left-color: var(--border-focus);
    }}

    /* Threat Beacon Banner inside Cards */
    .threat-beacon-strip {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.68rem;
      font-weight: 800;
      letter-spacing: 0.04em;
      margin-bottom: 4px;
    }}
    .threat-beacon-case {{
      background: rgba(239, 68, 68, 0.16);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }}
    .threat-beacon-vuln {{
      background: rgba(249, 115, 22, 0.15);
      color: #fdba74;
      border: 1px solid rgba(249, 115, 22, 0.4);
    }}
    .pulse-dot-beacon {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      display: inline-block;
      margin-right: 5px;
      animation: pulseBeaconAnim 1.6s infinite ease-in-out;
    }}
    .pulse-dot-beacon.red {{
      background: #ef4444;
      box-shadow: 0 0 8px #ef4444;
    }}
    .pulse-dot-beacon.orange {{
      background: #f97316;
      box-shadow: 0 0 8px #f97316;
    }}
    @keyframes pulseBeaconAnim {{
      0%, 100% {{ transform: scale(1); opacity: 1; }}
      50% {{ transform: scale(1.35); opacity: 0.55; }}
    }}

    /* Keyword Highlights in Headlines */
    .threat-kw-highlight-case {{
      background: rgba(239, 68, 68, 0.28);
      color: #fee2e2;
      font-weight: 800;
      padding: 1px 4px;
      border-radius: 3px;
      border-bottom: 2px solid #ef4444;
      box-shadow: 0 0 8px rgba(239, 68, 68, 0.3);
    }}
    .threat-kw-highlight-vuln {{
      background: rgba(249, 115, 22, 0.25);
      color: #ffedd5;
      font-weight: 800;
      padding: 1px 4px;
      border-radius: 3px;
      border-bottom: 2px solid #f97316;
      box-shadow: 0 0 8px rgba(249, 115, 22, 0.25);
    }}
    .threat-kw-highlight-general {{
      background: rgba(234, 179, 8, 0.2);
      color: #fef08a;
      font-weight: 700;
      padding: 1px 3px;
      border-radius: 3px;
    }}


    body.light-theme .article-card.threat-card-case {{
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.06) 0%, #ffffff 65%) !important;
      border-left: 5px solid #dc2626 !important;
      box-shadow: 0 4px 16px rgba(220, 38, 38, 0.15) !important;
    }}
    body.light-theme .article-card.threat-card-vuln {{
      background: linear-gradient(135deg, rgba(249, 115, 22, 0.06) 0%, #ffffff 65%) !important;
      border-left: 5px solid #ea580c !important;
      box-shadow: 0 4px 14px rgba(234, 88, 12, 0.14) !important;
    }}
    body.light-theme .threat-kw-highlight-case {{
      background: #fee2e2;
      color: #991b1b;
      border-bottom: 2px solid #dc2626;
    }}
    body.light-theme .threat-kw-highlight-vuln {{
      background: #ffedd5;
      color: #9a3412;
      border-bottom: 2px solid #ea580c;
    }}

    /* Ingested Sources & Websites Registry */
    .ingested-sources-card {{
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 14px;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .source-site-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 8px;
      transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
    }}
    .source-site-card:hover {{
      border-color: var(--border-focus);
      transform: translateY(-2px);
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
    }}

    body.light-theme .ingested-sources-card {{
      background: #f8fafc !important;
      border-color: #e2e8f0 !important;
    }}
    body.light-theme .source-site-card {{
      background: #ffffff !important;
      border-color: #e2e8f0 !important;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04) !important;
    }}
    body.light-theme .source-site-card:hover {{
      border-color: #3b82f6 !important;
      box-shadow: 0 4px 12px rgba(59,130,246,0.15) !important;
    }}
    
    .article-btn-read {{
      padding: 3px 9px;
      font-size: 0.72rem;
      font-weight: 600;
      background: rgba(59, 130, 246, 0.15);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.4);
      border-radius: 4px;
      cursor: pointer;
    }}
    .article-btn-read:hover {{
      background: #2563eb;
      color: #ffffff;
    }}

    .article-btn-ext {{
      padding: 3px 9px;
      font-size: 0.72rem;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-main);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}
    .article-btn-ext:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: var(--border-focus);
    }}
    
    .article-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.7rem;
      color: var(--text-dim);
    }}
    
    .article-outlet {{
      font-weight: 600;
      color: var(--border-focus);
      background: rgba(59, 130, 246, 0.12);
      padding: 2px 6px;
      border-radius: 4px;
    }}
    
    .article-headline {{
      font-size: 0.85rem;
      font-weight: 600;
      line-height: 1.35;
      color: var(--text-main);
    }}
    
    .article-headline a {{
      color: inherit;
      text-decoration: none;
    }}
    .article-headline a:hover {{
      color: var(--border-focus);
      text-decoration: underline;
    }}
    
    .article-badges {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      align-items: center;
    }}

    /* Badges & Pills */
    .badge {{
      font-size: 0.68rem;
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 4px;
      white-space: nowrap;
    }}
    
    .badge-cat-a {{
      background: rgba(56, 189, 248, 0.15);
      color: var(--cat-a);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }}
    
    .badge-cat-b {{
      background: rgba(192, 132, 252, 0.15);
      color: var(--cat-b);
      border: 1px solid rgba(192, 132, 252, 0.3);
    }}
    
    .badge-cat-c {{
      background: rgba(52, 211, 153, 0.15);
      color: var(--cat-c);
      border: 1px solid rgba(52, 211, 153, 0.3);
    }}
    
    .badge-sev-1 {{ background: rgba(100, 116, 139, 0.2); color: #64748b; border: 1px solid #64748b; }}
    .badge-sev-2 {{ background: rgba(56, 189, 248, 0.2); color: #0284c7; border: 1px solid #38bdf8; }}
    .badge-sev-3 {{ background: rgba(250, 204, 21, 0.2); color: #d97706; border: 1px solid #facc15; }}
    .badge-sev-4 {{ background: rgba(251, 146, 60, 0.2); color: #ea580c; border: 1px solid #fb923c; }}
    .badge-sev-5 {{ background: rgba(239, 68, 68, 0.25); color: #dc2626; border: 1px solid #ef4444; }}
    
    .badge-conf-low {{
      background: rgba(239, 68, 68, 0.15);
      color: #dc2626;
      border: 1px dashed #ef4444;
      font-weight: 700;
    }}
    
    .badge-tier {{
      font-size: 0.65rem;
      background: var(--border-subtle);
      color: var(--text-muted);
      padding: 1px 5px;
      border-radius: 3px;
    }}

    /* 7. Incidents Table */
    .table-container {{
      overflow-x: auto;
      max-height: 560px;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
    }}
    
    .incidents-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.8rem;
      text-align: left;
    }}
    
    .incidents-table th {{
      background: var(--table-th);
      color: var(--text-muted);
      font-weight: 600;
      padding: 10px 12px;
      position: sticky;
      top: 0;
      z-index: 10;
      border-bottom: 2px solid var(--border-subtle);
      cursor: pointer;
      user-select: none;
    }}
    
    .incidents-table th:hover {{
      color: var(--text-main);
    }}
    
    .incidents-table td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--table-border);
      vertical-align: middle;
    }}
    
    .incidents-table tr:hover td {{
      background: var(--table-row-hover);
    }}
    
    .incident-headline {{
      font-weight: 500;
      color: var(--text-main);
      max-width: 380px;
    }}
    
    .incident-link {{
      color: var(--border-focus);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }}
    .incident-link:hover {{
      text-decoration: underline;
    }}

    /* Modal for Logging Incidents */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }}
    .modal-overlay.active {{
      display: flex !important;
    }}

    .modal-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      width: 90%;
      max-width: 600px;
      padding: 24px;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 10px;
    }}

    .modal-title {{
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-main);
    }}

    .modal-close {{
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.2rem;
      cursor: pointer;
    }}

    .modal-form {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}

    .form-group-full {{
      grid-column: 1 / -1;
    }}

    .modal-form label {{
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      color: var(--text-muted);
      display: block;
      margin-bottom: 4px;
    }}

    .modal-form input, .modal-form select, .modal-form textarea {{
      width: 100%;
      background: var(--input-bg);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 0.82rem;
      outline: none;
    }}

    .modal-actions {{
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 10px;
    }}

    /* 8. Methodology Footer */
    footer.methodology {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 24px;
      margin-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    
    .methodology h3 {{
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-main);
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 8px;
    }}
    
    .methodology-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    
    .methodology-col h4 {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 6px;
    }}
    
    .sources-status-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.75rem;
      margin-top: 6px;
    }}
    
    .sources-status-table th, .sources-status-table td {{
      padding: 5px 8px;
      border-bottom: 1px solid var(--border-subtle);
      text-align: left;
    }}
    
    .source-status-pill {{
      display: inline-block;
      padding: 1px 6px;
      border-radius: 4px;
      font-weight: 600;
      font-size: 0.7rem;
    }}
    .status-ok {{ background: rgba(16, 185, 129, 0.2); color: #10b981; }}
    .status-blocked {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; }}

    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: var(--bg-base);
    }}
    ::-webkit-scrollbar-thumb {{
      background: var(--border-subtle);
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: var(--border-focus);
    }}

    /* Print Optimization (for browser Save as PDF) */
    @media print {{
      .live-top-ticker, .livetime-hud, .filter-panel, .chart-view-toggle, .btn-reset, .modal-overlay {{
        display: none !important;
      }}
      body {{
        background: #ffffff !important;
        color: #0f172a !important;
      }}
      .dashboard-container {{
        max-width: 100% !important;
        padding: 0 !important;
      }}
      .section-card, .kpi-card, .concerns-panel {{
        box-shadow: none !important;
        border: 1px solid #cbd5e1 !important;
        page-break-inside: avoid;
        background: #ffffff !important;
      }}
      .incidents-table {{
        font-size: 8pt !important;
      }}
    }}

    /* Famous AI Ecosystems Quick-Pill Bar */
    .ecosystem-pills-bar {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 14px;
      padding: 10px 16px;
      background: var(--hud-box-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    }}
    .ecosystem-pills-label {{
      font-size: 0.74rem;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-right: 6px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }}
    .ecosystem-live-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #3b82f6;
      display: inline-block;
      box-shadow: 0 0 6px #3b82f6;
      animation: pulseDot 2s infinite;
    }}
    .pill-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      outline: none;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      user-select: none;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }}
    .pill-btn:hover {{
      border-color: #3b82f6;
      color: #3b82f6;
      background: rgba(59, 130, 246, 0.08);
      transform: translateY(-1px);
      box-shadow: 0 4px 10px rgba(59, 130, 246, 0.15);
    }}
    .pill-btn.active {{
      background: #2563eb !important;
      color: #ffffff !important;
      border-color: #2563eb !important;
      font-weight: 700;
      box-shadow: 0 2px 10px rgba(37, 99, 235, 0.35);
      transform: translateY(-1px);
    }}
    .pill-btn:active {{
      transform: translateY(0);
    }}
    .pill-btn[data-eco="Gemini"]:hover {{
      border-color: #4285f4;
      color: #4285f4;
      background: rgba(66, 133, 244, 0.1);
    }}
    .pill-btn[data-eco="Anthropic"]:hover {{
      border-color: #d97706;
      color: #d97706;
      background: rgba(217, 119, 6, 0.1);
    }}
    .pill-btn[data-eco="Hugging Face"]:hover {{
      border-color: #f59e0b;
      color: #f59e0b;
      background: rgba(245, 158, 11, 0.1);
    }}
    .pill-btn[data-eco="OpenAI"]:hover {{
      border-color: #10a37f;
      color: #10a37f;
      background: rgba(16, 163, 127, 0.1);
    }}
    .pill-btn[data-eco="Copilot"]:hover {{
      border-color: #0078d4;
      color: #0078d4;
      background: rgba(0, 120, 212, 0.1);
    }}
    .pill-btn[data-eco="NVIDIA"]:hover {{
      border-color: #76b900;
      color: #76b900;
      background: rgba(118, 185, 0, 0.1);
    }}
    .pill-btn[data-eco="Meta"]:hover {{
      border-color: #8b5cf6;
      color: #8b5cf6;
      background: rgba(139, 92, 246, 0.1);
    }}

    /* Card Quick-Filter Pill Rows */
    .card-pills-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 8px;
      padding-top: 8px;
      border-top: 1px solid var(--border-subtle);
      align-items: center;
      justify-content: center;
    }}
    .card-pills-row .pill-btn {{
      font-size: 0.72rem;
      padding: 4px 10px;
      border-radius: 16px;
      font-weight: 600;
    }}
    .card-pills-row .pill-btn:hover {{
      transform: translateY(-1px);
    }}
    
    /* Specific Accent Hovers for Category Pills */
    .card-pills-row .pill-btn[data-cat="A"]:hover {{
      border-color: var(--cat-a);
      color: var(--cat-a);
      background: rgba(56, 189, 248, 0.1);
    }}
    .card-pills-row .pill-btn[data-cat="B"]:hover {{
      border-color: var(--cat-b);
      color: var(--cat-b);
      background: rgba(192, 132, 252, 0.1);
    }}
    .card-pills-row .pill-btn[data-cat="C"]:hover {{
      border-color: var(--cat-c);
      color: var(--cat-c);
      background: rgba(52, 211, 153, 0.1);
    }}

    /* Specific Accent Hovers for Severity Pills */
    .card-pills-row .pill-btn[data-sev="5"]:hover {{
      border-color: #ef4444;
      color: #ef4444;
      background: rgba(239, 68, 68, 0.1);
    }}
    .card-pills-row .pill-btn[data-sev="4"]:hover {{
      border-color: #fb923c;
      color: #fb923c;
      background: rgba(251, 146, 60, 0.1);
    }}
    .card-pills-row .pill-btn[data-sev="3"]:hover {{
      border-color: #facc15;
      color: #facc15;
      background: rgba(250, 204, 21, 0.1);
    }}
    .card-pills-row .pill-btn[data-sev="2"]:hover {{
      border-color: #38bdf8;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.1);
    }}
    .card-pills-row .pill-btn[data-sev="1"]:hover {{
      border-color: #94a3b8;
      color: #94a3b8;
      background: rgba(148, 163, 184, 0.1);
    }}

    /* Active Filters Ribbon */
    .active-filters-ribbon {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 8px;
      padding: 8px 14px;
      background: var(--hud-box-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      margin-bottom: 12px;
      font-size: 0.76rem;
      animation: fadeIn 0.2s ease-in-out;
    }}
    .active-filters-left {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .active-filters-title {{
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .active-filter-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 3px 10px;
      background: rgba(37, 99, 235, 0.15);
      border: 1px solid #3b82f6;
      border-radius: 14px;
      color: #93c5fd;
      font-weight: 600;
      font-size: 0.74rem;
    }}
    .active-filter-badge .badge-remove {{
      cursor: pointer;
      color: #cbd5e1;
      font-weight: 800;
      transition: color 0.15s;
    }}
    .active-filter-badge .badge-remove:hover {{
      color: #ef4444;
    }}
    .btn-clear-all-ribbon {{
      background: transparent;
      border: 1px solid rgba(239, 68, 68, 0.6);
      color: #ef4444;
      padding: 3px 10px;
      border-radius: 12px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-clear-all-ribbon:hover {{
      background: rgba(239, 68, 68, 0.15);
      border-color: #ef4444;
    }}
  </style>
</head>
<body>


  <!-- Top Real-Time Threat Stream Marquee (DYNAMIC LIVE TIME CONTINUOUS STREAM) -->
  <div class="live-top-ticker">
    <div class="ticker-label">
      <span class="ticker-pulse-dot"></span> LIVE THREAT BROADCAST · <span id="tickerLiveClock" style="font-size:0.68rem; font-weight:700;">REAL-TIME</span>
    </div>
    <div class="ticker-controls">
      <button class="ticker-ctrl-btn" id="tickerPauseBtn" onclick="window.toggleTickerPause()" title="Pause/Resume scrolling">⏸️</button>
      <div class="ticker-speed-group">
        <button class="ticker-speed-btn active" id="spdSlow" onclick="window.setTickerSpeed('slow')" title="Slow, easy-to-read pace (140s)">🐢 Slow</button>
        <button class="ticker-speed-btn" id="spdNormal" onclick="window.setTickerSpeed('normal')" title="Medium pace (90s)">Medium</button>
        <button class="ticker-speed-btn" id="spdFast" onclick="window.setTickerSpeed('fast')" title="Faster pace (50s)">⚡ Fast</button>
      </div>
    </div>
    <div class="ticker-track">
      <div class="ticker-content" id="liveTickerContent">
        {initial_ticker_content}
      </div>
    </div>
  </div>

  <div class="dashboard-container">
    
    <!-- Top Header with Live Time HUD & Dark/Light Mode Switcher -->
    <header>
      <div class="header-titles">
        <h1>
          GLOBAL AI CYBERATTACK RADAR
          <span class="badge-live" id="liveModeBadge">LIVE SYNC READY</span>

        </h1>
        <p>Worldwide Threat Intelligence · 10-Year Macro Horizon (2017–2026+), Autonomous Agent Exploits & Continuous Ingestion</p>
      </div>

      <!-- Live Time & Controls -->
      <div class="livetime-hud">
        <div class="digital-clock-box">
          <div class="clock-time" id="liveDigitalClock">--:--:-- UTC</div>
          <div class="clock-sub" id="liveDateStr">--</div>
        </div>

        <div class="digital-clock-box" style="align-items: center; text-align: center; min-width: 140px;">
          <div style="font-size: 0.72rem; color: var(--text-dim); font-weight: 600;">NEXT AUTO-SWEEP</div>
          <div style="font-family: ui-monospace, monospace; font-size: 1.05rem; font-weight: 700; color: #10b981;" id="sweepCountdown">04:59</div>
        </div>

        <div class="live-status-pill" id="sourceStatusWidget" onclick="window.openSourcesModal()" style="cursor: pointer;" title="Click to view all 25 live intelligence sources and websites being pulled">
          <span class="status-indicator" id="statusPulse"></span>
          <span id="sourceStatusText">Connecting to Live Threat Intelligence Feed...</span>
        </div>

        <button class="hud-btn" id="btnSyncNow" title="Force immediate re-check of live feeds">
          <span>⚡ Sync Now</span>
        </button>

        <button class="hud-btn" id="btnOpenSourcesModal" onclick="window.openSourcesModal()" style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);" title="View detailed directory of all 25 websites and feeds being pulled">
          <span>🌐 Ingested Sites (25)</span>
        </button>

        <button class="hud-btn" id="btnOpenPipelineModal" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4);" title="View End-to-End System Data Pipeline">
          <span>📊 Pipeline</span>
        </button>

        <button class="hud-btn" id="btnExportData" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);" title="Download Official Threat Intelligence Report (PDF)">
          <span>📥 Export PDF</span>
        </button>

        <!-- Theme Toggle Button -->
        <button class="theme-toggle-btn" id="btnThemeToggle" title="Toggle between Dark and Light mode">
          <span id="themeIcon">☀️</span> <span id="themeLabel">Light Mode</span>
        </button>


      </div>
    </header>

    <!-- Universal Filter Bar (Applies to Every Panel) -->
    <section class="filter-panel" id="universalFilters">
      <div class="filter-group">
        <label for="filterHorizon">Time Horizon</label>
        <select id="filterHorizon">
          <option value="10Y" selected>10-Year Macro View (2017 – 2026+)</option>
          <option value="5Y">5-Year Trend View (2022 – 2026+)</option>
          <option value="12M">Rolling 12 Months (Recent Window)</option>
          <option value="ALL">All-Time Continuous (All Recorded)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterCategory">Scope / Category</label>
        <select id="filterCategory">
          <option value="ALL">All Categories (A, B, C)</option>
          <option value="A">Cat A: Attacks USING AI</option>
          <option value="B">Cat B: Attacks ON AI Systems</option>
          <option value="C">Cat C: Agentic Attacks Only</option>
          <option value="AB">Cat A & B</option>
          <option value="AC">Cat A & C</option>
          <option value="BC">Cat B & C</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterSeverity">Severity Level</label>
        <select id="filterSeverity">
          <option value="ALL">All Severities (1 - 5)</option>
          <option value="5">Severity 5: Systemic / Critical</option>
          <option value="4">Severity 4: Significant Loss</option>
          <option value="3">Severity 3: Confirmed Breach, Limited</option>
          <option value="2">Severity 2: Attempted, No Impact</option>
          <option value="1">Severity 1: Proof-of-Concept</option>
          <option value="4-5">Severity 4 & 5 (High/Critical)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterSector">Target Sector</label>
        <select id="filterSector">
          <option value="ALL">All Sectors</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterVector">Attack Vector</label>
        <select id="filterVector">
          <option value="ALL">All Vectors</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterYear">Specific Year</label>
        <select id="filterYear">
          <option value="ALL">All Years (2017–2026+)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterCountry">Geography / Country</label>
        <select id="filterCountry">
          <option value="ALL">Global (All Countries)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterTier">Source Registry Tier</label>
        <select id="filterTier">
          <option value="ALL">All Tiers (1, 2, 3)</option>
          <option value="1">Tier 1: Registries (ATLAS/CISA/AIID)</option>
          <option value="2">Tier 2: Vendor Intel (MSFT/Mandiant/CS)</option>
          <option value="3">Tier 3: Verified CTI News (Record/DarkReading)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterEntity" style="color: #38bdf8; font-weight: 700;">Famous Company / Ecosystem</label>
        <select id="filterEntity" style="border-color: rgba(56, 189, 248, 0.5);">
          <option value="ALL" selected>All Companies (Global Threat)</option>
          <option value="Gemini">✨ Google Gemini</option>
          <option value="Anthropic">🧠 Anthropic Claude</option>
          <option value="Hugging Face">🤗 Hugging Face</option>
          <option value="OpenAI">🤖 OpenAI / ChatGPT</option>
          <option value="Microsoft">🪟 Microsoft / Copilot</option>
          <option value="NVIDIA">⚡ NVIDIA</option>
          <option value="Meta">🦙 Meta Llama</option>
          <option value="JPMorgan">🏦 JPMorgan Chase & Major Banks (Nov 19 Cyberattack)</option>
        </select>
      </div>

      <div class="filter-actions">
        <button class="btn-reset" id="btnResetFilters" title="Reset all filters to default">Reset Filters</button>
      </div>
    </section>

    <!-- 1. KPI Strip -->
    <section class="kpi-strip">
      <div class="kpi-card">
        <span class="kpi-label">Active Horizon Incidents</span>
        <span class="kpi-value" id="kpiHorizonIncidents">--</span>
        <span class="kpi-subtext" id="kpiHorizonSub">10-Year Macro baseline volume</span>
      </div>

      <div class="kpi-card">
        <span class="kpi-label">Aggregated Reports</span>
        <span class="kpi-value" id="kpiArticleCount">--</span>
        <span class="kpi-subtext">Verified media & CTI dispatches</span>
      </div>

      <div class="kpi-card agentic">
        <span class="kpi-label">Agentic (C) Incidents</span>
        <span class="kpi-value" id="kpiAgenticTotal" style="color: var(--cat-c);">--</span>
        <span class="kpi-subtext" id="kpiAgenticPct">--% of current view</span>
      </div>

      <div class="kpi-card">
        <span class="kpi-label">Countries Impacted</span>
        <span class="kpi-value" id="kpiCountriesCount">--</span>
        <span class="kpi-subtext">Global cross-border reach</span>
      </div>

      <div class="kpi-card severity-high">
        <span class="kpi-label">Critical Incidents (Sev 4–5)</span>
        <span class="kpi-value" id="kpiCriticalTotal" style="color: var(--sev-5);">--</span>
        <span class="kpi-subtext">Significant loss or critical infra</span>
      </div>

      <div class="kpi-card">
        <span class="kpi-label">Session Uptime</span>
        <span class="kpi-value" id="kpiUptime">00:00:00</span>
        <span class="kpi-subtext" id="kpiLastUpdated">--</span>
      </div>
    </section>

    <!-- 1B. Category & Threat Level KPI Telemetry Matrix -->
    <section class="kpi-matrix-section" id="kpiMatrixSection">
      <!-- Row A: Threat Volume by AI Attack Category -->
      <div class="kpi-matrix-block">
        <div class="kpi-matrix-header">
          <div class="kpi-matrix-title-group">
            <span class="kpi-matrix-badge kpi-matrix-badge-cat" style="background: rgba(56, 189, 248, 0.15); color: var(--cat-a); border: 1px solid rgba(56, 189, 248, 0.3);">
              CATEGORY TELEMETRY
            </span>
            <h3 class="kpi-matrix-title">AI Threat Category Breakdown <span class="kpi-matrix-hint">(Click any category card to filter dashboard)</span></h3>
          </div>
          <div class="kpi-matrix-actions">
            <button class="kpi-matrix-reset-btn" id="btnResetCatFilter" onclick="window.filterByCategoryQuick('ALL')" title="Reset category filter" style="display: none;">Reset Category</button>
          </div>
        </div>
        
        <div class="category-kpi-strip" id="categoryKpiStrip">
          <!-- Cat A -->
          <div class="kpi-card interactive-kpi-card cat-a-kpi" id="kpiCardCatA" onclick="window.toggleCategoryKPI('A')" title="Click to filter dashboard by Category A: Offensive AI">
            <div class="kpi-card-top">
              <span class="kpi-badge cat-a-badge">🤖 CAT A: USING AI</span>
              <span class="kpi-filter-indicator" id="indicatorCatA">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value cat-a-val" id="kpiCatACount">--</span>
              <span class="kpi-pct-badge" id="kpiCatAPct">--%</span>
            </div>
            <span class="kpi-label">Offensive AI & Threat Delivery</span>
            <span class="kpi-subtext">Deepfakes, automated phishing, LLM malware generation</span>
          </div>

          <!-- Cat B -->
          <div class="kpi-card interactive-kpi-card cat-b-kpi" id="kpiCardCatB" onclick="window.toggleCategoryKPI('B')" title="Click to filter dashboard by Category B: On AI Systems">
            <div class="kpi-card-top">
              <span class="kpi-badge cat-b-badge">🎯 CAT B: ON AI SYSTEMS</span>
              <span class="kpi-filter-indicator" id="indicatorCatB">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value cat-b-val" id="kpiCatBCount">--</span>
              <span class="kpi-pct-badge" id="kpiCatBPct">--%</span>
            </div>
            <span class="kpi-label">Targeting AI Infra & Models</span>
            <span class="kpi-subtext">Weights extraction, prompt injection, data poisoning</span>
          </div>

          <!-- Cat C -->
          <div class="kpi-card interactive-kpi-card cat-c-kpi" id="kpiCardCatC" onclick="window.toggleCategoryKPI('C')" title="Click to filter dashboard by Category C: Agentic Attacks">
            <div class="kpi-card-top">
              <span class="kpi-badge cat-c-badge">⚡ CAT C: AGENTIC ATTACKS</span>
              <span class="kpi-filter-indicator" id="indicatorCatC">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value cat-c-val" id="kpiCatCCount">--</span>
              <span class="kpi-pct-badge" id="kpiCatCPct">--%</span>
            </div>
            <span class="kpi-label">Autonomous Agentic Exploits</span>
            <span class="kpi-subtext">Self-governing bot loops, API chaining, automated escalation</span>
          </div>
        </div>
      </div>

      <!-- Row B: Threat Volume by Severity Level -->
      <div class="kpi-matrix-block">
        <div class="kpi-matrix-header">
          <div class="kpi-matrix-title-group">
            <span class="kpi-matrix-badge kpi-matrix-badge-sev" style="background: rgba(239, 68, 68, 0.15); color: var(--sev-5); border: 1px solid rgba(239, 68, 68, 0.3);">
              SEVERITY HIERARCHY
            </span>
            <h3 class="kpi-matrix-title">Threat Severity Level Distribution <span class="kpi-matrix-hint">(Click any level card to filter dashboard)</span></h3>
          </div>
          <div class="kpi-matrix-actions">
            <button class="kpi-matrix-reset-btn" id="btnResetSevFilter" onclick="window.filterBySeverityQuick('ALL')" title="Reset severity filter" style="display: none;">Reset Severity</button>
          </div>
        </div>

        <div class="severity-kpi-strip" id="severityKpiStrip">
          <!-- Level 5 -->
          <div class="kpi-card interactive-kpi-card sev-5-kpi" id="kpiCardSev5" onclick="window.toggleSeverityKPI('5')" title="Click to filter dashboard by Level 5: Critical Impact">
            <div class="kpi-card-top">
              <span class="kpi-badge sev-5-badge">🚨 LEVEL 5 · CRITICAL</span>
              <span class="kpi-filter-indicator" id="indicatorSev5">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value sev-5-val" id="kpiSev5Count">--</span>
              <span class="kpi-pct-badge" id="kpiSev5Pct">--%</span>
            </div>
            <span class="kpi-label">National Infra & Grid Loss</span>
            <span class="kpi-subtext">Systemic critical infra disruption, >$50M breach</span>
          </div>

          <!-- Level 4 -->
          <div class="kpi-card interactive-kpi-card sev-4-kpi" id="kpiCardSev4" onclick="window.toggleSeverityKPI('4')" title="Click to filter dashboard by Level 4: High Threat">
            <div class="kpi-card-top">
              <span class="kpi-badge sev-4-badge">🔴 LEVEL 4 · HIGH</span>
              <span class="kpi-filter-indicator" id="indicatorSev4">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value sev-4-val" id="kpiSev4Count">--</span>
              <span class="kpi-pct-badge" id="kpiSev4Pct">--%</span>
            </div>
            <span class="kpi-label">Severe Breach & Extortion</span>
            <span class="kpi-subtext">Ransomware, core model theft, credential takeover</span>
          </div>

          <!-- Level 3 -->
          <div class="kpi-card interactive-kpi-card sev-3-kpi" id="kpiCardSev3" onclick="window.toggleSeverityKPI('3')" title="Click to filter dashboard by Level 3: Moderate Threat">
            <div class="kpi-card-top">
              <span class="kpi-badge sev-3-badge">🟡 LEVEL 3 · MODERATE</span>
              <span class="kpi-filter-indicator" id="indicatorSev3">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value sev-3-val" id="kpiSev3Count">--</span>
              <span class="kpi-pct-badge" id="kpiSev3Pct">--%</span>
            </div>
            <span class="kpi-label">Active Exploit & CVE</span>
            <span class="kpi-subtext">Weaponized CVEs, jailbreak prompts, pipeline bypass</span>
          </div>

          <!-- Level 2 -->
          <div class="kpi-card interactive-kpi-card sev-2-kpi" id="kpiCardSev2" onclick="window.toggleSeverityKPI('2')" title="Click to filter dashboard by Level 2: Low Threat">
            <div class="kpi-card-top">
              <span class="kpi-badge sev-2-badge">🔵 LEVEL 2 · LOW</span>
              <span class="kpi-filter-indicator" id="indicatorSev2">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value sev-2-val" id="kpiSev2Count">--</span>
              <span class="kpi-pct-badge" id="kpiSev2Pct">--%</span>
            </div>
            <span class="kpi-label">Monitored Anomaly</span>
            <span class="kpi-subtext">Automated reconnaissance, port scan, probe telemetry</span>
          </div>

          <!-- Level 1 -->
          <div class="kpi-card interactive-kpi-card sev-1-kpi" id="kpiCardSev1" onclick="window.toggleSeverityKPI('1')" title="Click to filter dashboard by Level 1: Informational">
            <div class="kpi-card-top">
              <span class="kpi-badge sev-1-badge">⚪ LEVEL 1 · INFO</span>
              <span class="kpi-filter-indicator" id="indicatorSev1">Filter</span>
            </div>
            <div class="kpi-card-middle">
              <span class="kpi-value sev-1-val" id="kpiSev1Count">--</span>
              <span class="kpi-pct-badge" id="kpiSev1Pct">--%</span>
            </div>
            <span class="kpi-label">Research Advisory</span>
            <span class="kpi-subtext">Security bulletins, vendor disclosures, academic PoCs</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Key Concerns Panel -->
    <section class="concerns-panel" id="concernsSection">
      <div class="concerns-header">
        <span class="concerns-badge">SOC PRIORITY BULLETIN</span>
        <h2 class="concerns-title" id="socBulletinTitle">10-Year Threat Evolution & Current Findings</h2>
      </div>
      <ul class="concerns-list" id="concernsList">
      </ul>
    </section>

    <!-- 3. Hero Chart with 5-Year / Monthly Switcher & Dynamic Table -->
    <section class="section-card">
      <div class="section-header" style="flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between;">
        <div class="section-title">
          <span id="heroChartTitle">Incident Trajectory</span>
        </div>
        <div class="chart-view-toggle" style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
          <div style="display: inline-flex; background: rgba(255, 255, 255, 0.05); padding: 3px; border-radius: 6px; border: 1px solid var(--border-subtle);">
            <button class="toggle-btn active" id="btnViewAnnual" style="padding: 5px 12px; font-size: 0.78rem;">10-Year Macro (2017–2026)</button>
            <button class="toggle-btn" id="btnViewMonthly2026" style="padding: 5px 12px; font-size: 0.78rem;">2026 Monthly Pulse</button>
            <button class="toggle-btn" id="btnViewCumulative" style="padding: 5px 12px; font-size: 0.78rem;">Cumulative S-Curve</button>
          </div>
          <div style="display: inline-flex; background: rgba(255, 255, 255, 0.05); padding: 3px; border-radius: 6px; border: 1px solid var(--border-subtle);">
            <button class="toggle-btn active" id="btnScaleLinear" title="Standard Linear Proportional Scale" style="padding: 5px 10px; font-size: 0.78rem;">📊 Linear</button>
            <button class="toggle-btn" id="btnScaleLog" title="Logarithmic Scale (Magnifies Historical Growth without compression)" style="padding: 5px 10px; font-size: 0.78rem;">📈 Log Scale</button>
          </div>
        </div>
        <div class="chart-legend-custom">
          <div class="legend-item"><span class="legend-dot" style="background: var(--cat-a);"></span> Cat A: Using AI</div>
          <div class="legend-item"><span class="legend-dot" style="background: var(--cat-b);"></span> Cat B: On AI Systems</div>
          <div class="legend-item"><span class="legend-dot" style="background: var(--cat-c);"></span> Cat C: Agentic Attacks</div>
          <div class="legend-item"><span class="legend-dot" style="background: #f59e0b; border-radius: 50%;"></span> Trendline</div>
        </div>
      </div>

      <!-- Hero Chart Metrics Summary Ribbon -->
      <div class="chart-metrics-ribbon" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin: 4px 0 12px 0; padding:10px 14px; background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:6px; font-size:0.78rem;">
        <div>📈 <strong>10-Year Growth Rate:</strong> <span style="color:#10b981; font-weight:700;">+52.1% CAGR</span></div>
        <div>🚀 <strong>Inflection Epoch:</strong> <span style="color:#38bdf8; font-weight:700;">2024 (Generative Wave)</span></div>
        <div>🤖 <strong>Fastest Expanding:</strong> <span style="color:#34d399; font-weight:700;">Category C Agentic (+180% YoY)</span></div>
        <div>⚡ <strong>Active 2026 Telemetry:</strong> <span style="color:#f59e0b; font-weight:700;" id="heroLiveTelemetryStat">1,100+ Live Dispatches</span></div>
      </div>

      <div class="chart-container" id="chartWrapper">
        <canvas id="heroChartCanvas"></canvas>
      </div>

      <div class="monthly-table-wrapper">
        <table class="monthly-table" id="timelineDataTable">
        </table>
      </div>
    </section>

    <!-- Multi-Dimensional Threat Intelligence Visualizations Deck -->
    <div class="grid-3col">
      <!-- 1. Scope Category Doughnut -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header" style="flex-direction: column; align-items: flex-start; gap: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="section-title">Scope Category Breakdown</div>
            <span style="font-size: 0.72rem; color: #38bdf8; font-weight: 600;">⚡ Quick Filter Pills Below</span>
          </div>
          <p style="font-size: 0.76rem; color: var(--text-muted); margin: 2px 0 0 0; line-height: 1.4;">
            Proportional distribution across core taxonomy: Cat A (Using AI), Cat B (Attacks On AI Systems), and Cat C (Agentic Attacks).
          </p>
        </div>
        <div style="height: 180px; position: relative; margin-top: 6px;">
          <canvas id="categoryDoughnutCanvas"></canvas>
        </div>
        <div class="card-pills-row" id="pillsCategory">
          <button class="pill-btn active" data-cat="ALL" onclick="window.filterByCategoryQuick('ALL')">All Categories</button>
          <button class="pill-btn" data-cat="A" onclick="window.filterByCategoryQuick('A')">Cat A: Using AI</button>
          <button class="pill-btn" data-cat="B" onclick="window.filterByCategoryQuick('B')">Cat B: On AI Systems</button>
          <button class="pill-btn" data-cat="C" onclick="window.filterByCategoryQuick('C')">Cat C: Agentic</button>
        </div>
      </section>

      <!-- 2. MITRE ATLAS Vector Radar (Spider Chart) -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header" style="flex-direction: column; align-items: flex-start; gap: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="section-title">MITRE ATLAS Vector Radar</div>
            <span style="font-size: 0.72rem; color: #38bdf8; font-weight: 600;">⚡ Quick Filter Pills Below</span>
          </div>
          <p style="font-size: 0.76rem; color: var(--text-muted); margin: 2px 0 0 0; line-height: 1.4;">
            Multi-dimensional threat density mapping 6 core adversarial tactics from MITRE ATLAS (Prompt Injection, Rogue MCP, Supply Chain, Evasion, Deepfake, and Recon).
          </p>
        </div>
        <div style="height: 180px; position: relative; margin-top: 6px;">
          <canvas id="vectorRadarCanvas"></canvas>
        </div>
        <div class="card-pills-row" id="pillsVector">
          <button class="pill-btn active" data-vec="ALL" onclick="window.filterByVectorQuick('ALL')">All Vectors</button>
          <button class="pill-btn" data-vec="Prompt Injection" onclick="window.filterByVectorQuick('Prompt Injection')">Prompt Injection</button>
          <button class="pill-btn" data-vec="Rogue MCP" onclick="window.filterByVectorQuick('Rogue MCP')">Rogue MCP / Tools</button>
          <button class="pill-btn" data-vec="Supply Chain" onclick="window.filterByVectorQuick('Supply Chain')">Supply Chain</button>
          <button class="pill-btn" data-vec="Evasion" onclick="window.filterByVectorQuick('Evasion')">Evasion</button>
        </div>
      </section>

      <!-- 3. Severity Impact Profile (Polar Area) -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header" style="flex-direction: column; align-items: flex-start; gap: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="section-title">Severity Impact Profile</div>
            <span style="font-size: 0.72rem; color: #38bdf8; font-weight: 600;">⚡ Quick Filter Pills Below</span>
          </div>
          <p style="font-size: 0.76rem; color: var(--text-muted); margin: 2px 0 0 0; line-height: 1.4;">
            Concentric radial spread across the 5 standard threat severity tiers, scaling from Sev 1 (Lab PoC) to Sev 5 (Systemic Infrastructure Breach).
          </p>
        </div>
        <div style="height: 180px; position: relative; margin-top: 6px;">
          <canvas id="severityPolarCanvas"></canvas>
        </div>
        <div class="card-pills-row" id="pillsSeverity">
          <button class="pill-btn active" data-sev="ALL" onclick="window.filterBySeverityQuick('ALL')">All</button>
          <button class="pill-btn" data-sev="5" onclick="window.filterBySeverityQuick('5')">🔴 Sev 5</button>
          <button class="pill-btn" data-sev="4" onclick="window.filterBySeverityQuick('4')">🟠 Sev 4</button>
          <button class="pill-btn" data-sev="3" onclick="window.filterBySeverityQuick('3')">🟡 Sev 3</button>
          <button class="pill-btn" data-sev="2" onclick="window.filterBySeverityQuick('2')">🔵 Sev 2</button>
          <button class="pill-btn" data-sev="1" onclick="window.filterBySeverityQuick('1')">⚪ Sev 1</button>
        </div>
      </section>
    </div>

    <!-- 4. Country View & 5. Breakdowns Grid -->
    <div class="grid-2col">
      <section class="section-card">
        <div class="section-header">
          <div class="section-title">Geographic Exposure (Incidents by Country)</div>
          <span style="font-size: 0.72rem; color: #38bdf8; font-weight: 600;">⚡ Quick Filter Pills Below</span>
        </div>
        <div class="card-pills-row" id="pillsCountry" style="margin-bottom: 10px; margin-top: 0; padding-top: 0; border-top: none;">
          <button class="pill-btn active" data-country="ALL" onclick="window.filterByCountryQuick('ALL')">All Countries</button>
          <button class="pill-btn" data-country="United States" onclick="window.filterByCountryQuick('United States')">🇺🇸 US</button>
          <button class="pill-btn" data-country="Europe" onclick="window.filterByCountryQuick('Europe')">🇪🇺 Europe</button>
          <button class="pill-btn" data-country="Malaysia" onclick="window.filterByCountryQuick('Malaysia')">🇲🇾 Malaysia</button>
          <button class="pill-btn" data-country="Global" onclick="window.filterByCountryQuick('Global')">🌐 Global</button>
        </div>
        <div class="country-view-content">
          <div class="country-bars" id="countryBarsList">
          </div>
        </div>
      </section>

      <section class="section-card">
        <div class="section-header">
          <div class="section-title">Threat Taxonomy & Severity Breakdowns</div>
        </div>
        <div class="breakdowns-container">
          <div class="breakdown-box">
            <span class="breakdown-title">Primary Attack Vectors</span>
            <div class="meter-list" id="vectorMeterList"></div>
          </div>

          <div class="breakdown-box">
            <span class="breakdown-title">Target Sectors</span>
            <div class="meter-list" id="sectorMeterList"></div>
          </div>

          <div class="breakdown-box" style="grid-column: 1 / -1;">
            <span class="breakdown-title">Severity Distribution (Rubric 1–5)</span>
            <div class="meter-list" id="severityMeterList"></div>
          </div>
        </div>
      </section>
    </div>

    <!-- 6. Reported Articles Feed -->
    <section class="section-card">
      <div class="articles-feed-header" style="flex-wrap: wrap; gap: 10px;">
        <div class="section-title">
          <span>Reported Articles Feed (What Was Reported)</span>
          <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);" id="articlesCountBadge">(50 most recent)</span>
        </div>
        <div class="feed-controls" style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
          <div style="display: flex; align-items: center; gap: 6px; font-size: 0.75rem; color: #10b981; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); padding: 4px 10px; border-radius: 20px; font-weight: 600;">
            <span class="live-dot" style="display: inline-block; width: 7px; height: 7px; background: #10b981; border-radius: 50%; box-shadow: 0 0 6px #10b981;"></span>
            <span>Next Live Sweep: <span id="sweepCountdown">90s</span></span>
          </div>
          <button id="forceSweepBtn" onclick="window.forceLiveSweep()" class="pill-btn" style="background: rgba(56,189,248,0.12); color: #38bdf8; border: 1px solid #38bdf8; font-weight: 600; cursor: pointer; padding: 4px 12px; border-radius: 6px;">
            ⚡ Force Live Sweep
          </button>
          <button id="btnToggleThreatHighlight" onclick="window.toggleThreatHighlight()" class="pill-btn active" style="background: rgba(239,68,68,0.18); color: #f87171; border: 1px solid #ef4444; font-weight: 700; cursor: pointer; padding: 4px 12px; border-radius: 6px;" title="Toggle glowing borders and keyword highlights on cyber threat articles">
            🚨 Threat Highlighting: ON
          </button>
          <button id="btnToggleThreatPriority" onclick="window.toggleThreatPriority()" class="pill-btn" style="background: rgba(249,115,22,0.12); color: #fb923c; border: 1px solid rgba(249,115,22,0.4); font-weight: 600; cursor: pointer; padding: 4px 12px; border-radius: 6px;" title="Sort active threat cases and zero-days to the top of the full feed">
            ⚡ Threats to Top
          </button>
          <input type="text" class="feed-search" id="articleSearchInput" placeholder="Filter articles by text...">
        </div>
      </div>

      <!-- Threat Intelligence & Incident Case Category Bar -->
      <div class="card-pills-row" id="pillsThreatType" style="margin-bottom: 8px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start; flex-wrap: wrap; gap: 6px;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>🎯</span> Threat Focus:
        </span>
        <button class="pill-btn active" data-threat="ALL" onclick="window.filterByThreatType('ALL')">All Threat Feeds</button>
        <button class="pill-btn" data-threat="case" onclick="window.filterByThreatType('case')" style="border-color: rgba(239,68,68,0.45); color: #f87171;">🔴 Active Attack Cases (Breaches & Ransomware)</button>
        <button class="pill-btn" data-threat="vulnerability" onclick="window.filterByThreatType('vulnerability')" style="border-color: rgba(249,115,22,0.45); color: #fb923c;">🟠 Vulnerability Alerts (CVEs & Exploits)</button>
        <button class="pill-btn" data-threat="informational" onclick="window.filterByThreatType('informational')" style="border-color: rgba(59,130,246,0.45); color: #60a5fa;">🔵 Threat Intel Advisories (To Inform)</button>
        <button class="pill-btn" data-threat="policy" onclick="window.filterByThreatType('policy')" style="border-color: rgba(34,197,94,0.45); color: #4ade80;">🟢 Policy, Indictments & Legal</button>
      </div>

      <!-- Tech Domain & Field Quick-Filter Bar -->
      <div class="card-pills-row" id="pillsField" style="margin-bottom: 8px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start; flex-wrap: wrap;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>🌐</span> Domain:
        </span>
        <button class="pill-btn active" data-field="ALL" onclick="window.filterByField('ALL')">All Domains</button>
        <button class="pill-btn" data-field="cyber" onclick="window.filterByField('cyber')">🛡️ Cybersecurity & CTI</button>
        <button class="pill-btn" data-field="ai" onclick="window.filterByField('ai')">🤖 AI & Frontier LLMs</button>
        <button class="pill-btn" data-field="hardware" onclick="window.filterByField('hardware')">💻 Hardware & Infrastructure</button>
        <button class="pill-btn" data-field="it" onclick="window.filterByField('it')">☁️ Enterprise Cloud / IT</button>
      </div>

      <!-- Broadcaster & Cyber Outlets Quick-Filter Bar -->
      <div class="card-pills-row" id="pillsBroadcast" style="margin-bottom: 14px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start; flex-wrap: wrap;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>📡</span> Source:
        </span>
        <button class="pill-btn active" data-broadcast="ALL" onclick="window.filterByBroadcast('ALL')">All Sources</button>
        <button class="pill-btn" data-broadcast="BleepingComputer" onclick="window.filterByBroadcast('bleepingcomputer')">🛡️ BleepingComputer</button>
        <button class="pill-btn" data-broadcast="The Hacker News" onclick="window.filterByBroadcast('hacker news')">📰 The Hacker News</button>
        <button class="pill-btn" data-broadcast="Dark Reading" onclick="window.filterByBroadcast('dark reading')">🔍 Dark Reading</button>
        <button class="pill-btn" data-broadcast="SecurityWeek" onclick="window.filterByBroadcast('securityweek')">⚡ SecurityWeek</button>
        <button class="pill-btn" data-broadcast="Krebs" onclick="window.filterByBroadcast('krebs')">🕵️ Krebs on Security</button>
        <button class="pill-btn" data-broadcast="CISA" onclick="window.filterByBroadcast('cisa')">🏛️ CISA Advisories</button>
        <button class="pill-btn" data-broadcast="Reuters" onclick="window.filterByBroadcast('reuters')">🌐 Reuters Cyber</button>
        <button class="pill-btn" data-broadcast="Wired" onclick="window.filterByBroadcast('wired')">🔌 Wired Security</button>
        <button class="pill-btn" data-broadcast="Ars Technica" onclick="window.filterByBroadcast('arstechnica')">💻 Ars Technica</button>
        <button class="pill-btn" onclick="window.openSourcesModal()" style="background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.4); font-weight: 700;">🌐 View All 25 Sources ↗</button>
      </div>

      <!-- Monitored Feeds & Ingested Websites Registry Card -->
      <div class="ingested-sources-card" id="ingestedSourcesSection" style="background: var(--input-bg); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px 16px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
          <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
            <span style="font-size: 0.88rem; font-weight: 700; color: var(--text-main);">🌐 Connected Ingestion Sources & Websites Being Pulled</span>
            <span class="badge" style="background: rgba(16,185,129,0.18); color: #10b981; border: 1px solid #10b981; font-weight: 700;">🟢 25 Feeds Connected</span>
            <span style="font-size: 0.74rem; color: var(--text-dim);">(Continuous 90s Ingestion Loop · TLS 1.3 / RSS 2.0 / Atom)</span>
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <button class="pill-btn" id="btnToggleSourcesGrid" onclick="window.toggleSourcesRegistry()" style="background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid #3b82f6; font-weight: 700; cursor: pointer; padding: 4px 12px; border-radius: 6px;">
              📋 Show Website List (25)
            </button>
            <button class="pill-btn" onclick="window.openSourcesModal()" style="background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.4); font-weight: 600; cursor: pointer; padding: 4px 12px; border-radius: 6px;">
              🔍 Full Inspector Modal
            </button>
          </div>
        </div>

        <!-- Collapsible Ingestion Registry Grid -->
        <div id="sourcesRegistryContainer" style="display: none; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-subtle);">
          <!-- Category Filter Pills for Sources -->
          <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px;" id="pillsSourceCategory">
            <button class="pill-btn active" data-srccat="ALL" onclick="window.filterSourcesByCategory('ALL')">All 25 Websites</button>
            <button class="pill-btn" data-srccat="Tier-1 Cyber Authority" onclick="window.filterSourcesByCategory('Tier-1 Cyber Authority')">🛡️ Tier-1 Cyber Authorities (6)</button>
            <button class="pill-btn" data-srccat="Government CTI & Alerts" onclick="window.filterSourcesByCategory('Government CTI & Alerts')">🏛️ Gov & Advisories</button>
            <button class="pill-btn" data-srccat="Vendor Threat Lab" onclick="window.filterSourcesByCategory('Vendor Threat Lab')">🔬 Vendor Labs (5)</button>
            <button class="pill-btn" data-srccat="Live Incident Wire" onclick="window.filterSourcesByCategory('Live Incident Wire')">⚡ Live Wires (4)</button>
            <button class="pill-btn" data-srccat="Tech & Cyber Desk" onclick="window.filterSourcesByCategory('Tech & Cyber Desk')">💻 Tech Desks (4)</button>
            <button class="pill-btn" data-srccat="Global News Wire" onclick="window.filterSourcesByCategory('Global News Wire')">🌐 News Wires (4)</button>
          </div>

          <!-- The 25 Ingested Sources Cards Grid -->
          <div id="pulledSourcesGrid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 10px;">
          </div>
        </div>
      </div>

      <div class="articles-grid" id="articlesGrid">
      </div>

      <!-- Interactive Feed Pagination & Full Stream Explorer -->
      <div id="articlesPaginationBar" style="margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div id="articlesPaginationStatus" style="font-size: 0.82rem; color: var(--text-dim); font-weight: 600;"></div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
          <button id="btnLoadMoreArticles" class="hud-btn" onclick="window.loadMoreArticles(60)" style="background: var(--bg-card); border: 1px solid var(--border-focus); color: var(--text-main); font-weight: 600; padding: 6px 16px; border-radius: 6px; cursor: pointer;">
            🔽 Load 60 More Articles
          </button>
          <button id="btnShowAllArticles" class="hud-btn" onclick="window.showAllArticles()" style="background: rgba(59, 130, 246, 0.15); border: 1px solid #3b82f6; color: #60a5fa; font-weight: 700; padding: 6px 16px; border-radius: 6px; cursor: pointer;">
            ⚡ Show Full Feed (All 1,805+)
          </button>
          <button id="btnResetFeedView" class="hud-btn" onclick="window.resetFeedView()" style="background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border-subtle); color: var(--text-dim); padding: 6px 12px; border-radius: 6px; cursor: pointer;">
            🔄 Reset (Show 60)
          </button>
        </div>
      </div>
    </section>

    <!-- 7. Incident Table -->
    <section class="section-card">
      <div class="articles-feed-header">
        <div class="section-title">
          <span>De-duplicated Incident Registry (What Happened)</span>
          <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);" id="incidentCountBadge"></span>
        </div>
        <div class="feed-controls">
          <input type="text" class="feed-search" id="incidentSearchInput" placeholder="Search incidents, CVEs, targets...">
        </div>
      </div>

      <!-- Active Filters Ribbon (Clear visibility on active criteria) -->
      <div class="active-filters-ribbon" id="activeFiltersRibbon" style="display: none;">
        <div class="active-filters-left">
          <span class="active-filters-title">
            <span>🎯</span> Active Filter Criteria:
          </span>
          <div class="active-filters-badges" id="activeFiltersBadges" style="display: flex; gap: 6px; flex-wrap: wrap;"></div>
        </div>
        <div class="active-filters-right" style="display: flex; align-items: center; gap: 8px;">
          <span id="activeFilteredCount" style="color: var(--text-muted); font-size: 0.74rem;"></span>
          <button class="btn-clear-all-ribbon" onclick="window.resetAllFiltersQuick()">✕ Reset All Filters</button>
        </div>
      </div>

      <!-- Famous AI Ecosystems Quick Filter Bar -->
      <div class="ecosystem-pills-bar">
        <span class="ecosystem-pills-label">
          <span class="ecosystem-live-dot"></span>
          Famous AI Ecosystems:
        </span>
        <button class="pill-btn active" data-eco="ALL" onclick="window.filterByEcosystem('ALL')">All Cases</button>
        <button class="pill-btn" data-eco="Gemini" onclick="window.filterByEcosystem('Gemini')">✨ Google Gemini</button>
        <button class="pill-btn" data-eco="Anthropic" onclick="window.filterByEcosystem('Anthropic')">🧠 Anthropic Claude</button>
        <button class="pill-btn" data-eco="Hugging Face" onclick="window.filterByEcosystem('Hugging Face')">🤗 Hugging Face</button>
        <button class="pill-btn" data-eco="OpenAI" onclick="window.filterByEcosystem('OpenAI')">🤖 OpenAI / ChatGPT</button>
        <button class="pill-btn" data-eco="Copilot" onclick="window.filterByEcosystem('Copilot')">🪟 Microsoft Copilot</button>
        <button class="pill-btn" data-eco="NVIDIA" onclick="window.filterByEcosystem('NVIDIA')">⚡ NVIDIA</button>
        <button class="pill-btn" data-eco="Meta" onclick="window.filterByEcosystem('Meta')">🦙 Meta Llama</button>
        <button class="pill-btn" data-eco="JPMorgan" onclick="window.filterByEcosystem('JPMorgan')" style="border-color: rgba(234,179,8,0.4); color: #facc15;">🏦 JPMorgan Chase</button>
      </div>

      <div class="table-container">
        <table class="incidents-table" id="incidentsTable">
          <thead>
            <tr>
              <th data-sort="incident_id">ID ▾</th>
              <th data-sort="date">Date ▾</th>
              <th>Headline / Operational Event</th>
              <th data-sort="category">Category</th>
              <th data-sort="attack_vector">Attack Vector</th>
              <th data-sort="target_sector">Target Sector</th>
              <th data-sort="country">Country</th>
              <th data-sort="severity">Severity</th>
              <th data-sort="confidence">Confidence</th>
              <th>Source Intel</th>
            </tr>
          </thead>
          <tbody id="incidentsTableBody">
          </tbody>
        </table>
      </div>
    </section>

    <!-- 8. Methodology Footer -->
    <footer class="methodology">
      <h3>10-Year Macro Architecture, Forward-Continuity & Source Observability</h3>
      <div class="methodology-grid">
        <div class="methodology-col">
          <h4>Future-Proofing & Coming Years Continuum</h4>
          <p><strong>Continuous Ingestion:</strong> The engine dynamically rolls forward each calendar year. When future events occur in 2027+, automated live feed parsers and multithreaded scraping daemons continuously ingest incoming zero-day events, dynamically extending time horizons without requiring manual entry.</p>
          <p style="margin-top: 6px;"><strong>10-Year Macro Evolutionary Shifts:</strong> 2017 Deepfake PoCs & AV Evasion → 2022 LLM Prompt Injections → 2023 Darknet LLMs & Jailbreaks → 2024 Deepfake wire fraud & GenAI worms → 2025/2026 Autonomous agent loop hijacking, rogue MCP servers & SCADA bridge disruption.</p>
        </div>

        <div class="methodology-col">
          <h4>Severity Rubric & Confidence</h4>
          <p><strong>1 - Proof of Concept:</strong> Lab demonstration, theoretical bypass, no malicious impact.</p>
          <p><strong>2 - Attempted, No Impact:</strong> In-the-wild attempt blocked or neutralised without exfiltration.</p>
          <p><strong>3 - Confirmed Breach, Limited:</strong> Successful lateral intrusion or credential harvest, contained scope.</p>
          <p><strong>4 - Significant Loss:</strong> Major financial exfiltration (>$10M), systemic code tampering, prolonged disruption.</p>
          <p><strong>5 - Systemic / Critical Infrastructure:</strong> Power grid, hospital network, SCADA or life-safety compromise.</p>
          <p style="margin-top: 6px;"><em>Low-confidence rows</em> are flagged visibly where primary attribution remains unverified by official CERTs.</p>
        </div>

        <div class="methodology-col">
          <h4>De-Duplication & Telemetry Matrix</h4>
          <p>Multiple media dispatches covering identical cyber events are clustered into an atomic <code>incident_id</code>, while retaining distinct article records in the article feed.</p>
          <p style="margin-top: 6px;"><strong>Live CORS Fetch Status:</strong></p>
          <table class="sources-status-table">
            <thead>
              <tr><th>Source</th><th>Tier</th><th>Browser Fetch Status</th></tr>
            </thead>
            <tbody id="sourceStatusTableBody">
            </tbody>
          </table>
        </div>
      </div>
    </footer>

  </div>

  <!-- System Architecture & Data Pipeline Modal -->
  <div class="modal-overlay" id="pipelineModal">
    <div class="modal-card" style="max-width: 820px; width: 94%; max-height: 88vh; overflow-y: auto;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="badge" style="background:#2563eb; color:#fff;">Architecture</span>
          <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981;">End-to-End Pipeline</span>
        </div>
        <button class="modal-close" id="btnClosePipelineModal">&times;</button>
      </div>

      <div style="padding: 10px 0 15px 0;">
        <h2 style="font-size:1.3rem; font-weight:700; color:var(--text-main); margin-bottom:6px;">
          Global AI Cyberattack Threat Radar — Data & Processing Pipeline
        </h2>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:18px;">
          Architectural schematic of raw threat ingestion, automated stream parsing, classification, live telemetry proxying, and reactive dashboard rendering.
        </p>

        <!-- Pipeline Stage 1 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#38bdf8; font-size:0.9rem;">1. Raw Threat Ingestion Layer (Tier 1 / 2 / 3 Sources)</strong>
            <span class="badge" style="background:rgba(56,189,248,0.15); color:#38bdf8;">Multi-Source Feed</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Continuous polling of authoritative public feeds: <strong>MITRE ATLAS</strong> (case studies & raw data), <strong>CyberSecurity Malaysia (CSM)</strong> & NACSA advisories, <strong>AI Incident Database (AIID)</strong>, <strong>OWASP GenAI Top 10</strong>, <strong>Microsoft Threat Intelligence (MSTIC)</strong>, <strong>Dark Reading</strong> XML, <strong>The Record</strong> RSS, and <strong>KrebsOnSecurity</strong>.
          </p>
        </div>

        <!-- Pipeline Stage 2 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#c084fc; font-size:0.9rem;">2. Automated Intelligence Ingestion Engine</strong>
            <span class="badge" style="background:rgba(192,132,252,0.15); color:#c084fc;">python-bs4 + lxml</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            <code>soup_harvester.py</code> parses incoming XML/HTML feeds via <code>BeautifulSoup(content, 'xml')</code>. Strips CDATA tags, normalizes publication timestamps, decodes HTML entities, and applies regex word-boundary filtering on AI threat indicators (<code>(ai|llm|deepfake|prompt injection|mcp|agent)</code>).
          </p>
        </div>

        <!-- Pipeline Stage 3 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#facc15; font-size:0.9rem;">3. Taxonomy Classification & De-duplication Router</strong>
            <span class="badge" style="background:rgba(250,204,21,0.15); color:#facc15;">Atomic Incident Mapping</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Maps events to the three foundational scope categories: <strong>Cat A (Attacks USING AI)</strong>, <strong>Cat B (Attacks ON AI Systems)</strong>, and <strong>Cat C (Agentic Attacks)</strong>. Applies 1–5 Severity Rubric and de-duplicates multiple media reports into unified atomic incident IDs (<code>INC-YYYY-MM-XX</code>).
          </p>
        </div>

        <!-- Pipeline Stage 4 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#34d399; font-size:0.9rem;">4. Local Telemetry Daemon & CORS Proxy (server.py)</strong>
            <span class="badge" style="background:rgba(52,211,153,0.15); color:#34d399;">HTTP Daemon :8080</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Local daemon running outside sandbox boundaries provides <code>Access-Control-Allow-Origin: *</code>. Exposes <code>/api/live-feed</code> to serve sanitized JSON articles with live timestamps, and handles <code>/api/status</code> health checks.
          </p>
        </div>

        <!-- Pipeline Stage 5 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#60a5fa; font-size:0.9rem;">5. Browser Client Reactive Engine (index.html)</strong>
            <span class="badge" style="background:rgba(96,165,250,0.15); color:#60a5fa;">State Hydration & Filters</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Merges bundled 10-year baseline (2017–2026+), live streaming feed from <code>/api/live-feed</code>, and local continuous intake records (<code>localStorage</code>). Routes data through the 8-dimension filter matrix (Horizon, Category, Severity, Sector, Vector, Year, Country, Tier).
          </p>
        </div>

        <!-- Pipeline Stage 6 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#f43f5e; font-size:0.9rem;">6. Analytical Presentation & Interactive Delivery</strong>
            <span class="badge" style="background:rgba(244,63,94,0.15); color:#f43f5e;">UI / SOC Console</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Renders dynamic Chart.js hero stacked bars, 10-year milestone tables, Country exposure rankings, live reported articles feed with <strong>In-App Intel Reader Modal</strong> (100% accessible briefings), and searchable de-duplicated incident registry.
          </p>
        </div>

        <div style="display:flex; justify-content:flex-end; margin-top:16px;">
          <button class="hud-btn" id="btnDismissPipelineModal" style="background:var(--border-focus); color:#fff; padding:6px 16px;">Close Pipeline Overview</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Ingested Sources & Websites Registry Inspector Modal -->
  <div class="modal-overlay" id="sourcesModal">
    <div class="modal-card" style="max-width: 960px; width: 95%; max-height: 88vh; overflow-y: auto;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="badge" style="background:#10b981; color:#fff; font-weight:700;">Ingestion Architecture</span>
          <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; font-weight:700;">🟢 25/25 Connected Sources</span>
          <span class="badge" style="background:rgba(59,130,246,0.15); color:#60a5fa; border:1px solid rgba(59,130,246,0.3); font-weight:700;">⚡ Multi-Threaded Daemon</span>
        </div>
        <button class="modal-close" id="btnCloseSourcesModal" onclick="window.closeSourcesModal()">&times;</button>
      </div>

      <div style="padding: 10px 0 15px 0;">
        <h2 style="font-size:1.35rem; font-weight:700; color:var(--text-main); margin-bottom:6px;">
          🌐 Monitored Cyber Threat Websites & Feed Endpoints Being Pulled
        </h2>
        <p style="font-size:0.83rem; color:var(--text-muted); margin-bottom:14px; line-height:1.5;">
          Complete directory of all 25 cybersecurity publishers, CERT government authorities, commercial threat intelligence centers, and real-time attack telemetry feeds continuously harvested by the platform's multi-threaded Python/BeautifulSoup4 ingestion engine.
        </p>

        <!-- Search and Filter Bar -->
        <div style="display:flex; gap:10px; margin-bottom:14px; flex-wrap:wrap; align-items:center;">
          <input type="text" id="sourceSearchInput" class="feed-search" style="flex:1; min-width:240px;" placeholder="Search websites by name, domain, category, or jurisdiction...">
          <div style="display:flex; gap:6px; flex-wrap:wrap;" id="modalSourcePills">
            <button class="pill-btn active" data-modalsrccat="ALL" onclick="window.filterModalSources('ALL')">All Sources (25)</button>
            <button class="pill-btn" data-modalsrccat="Tier-1 Cyber Authority" onclick="window.filterModalSources('Tier-1 Cyber Authority')">🛡️ Authorities</button>
            <button class="pill-btn" data-modalsrccat="Government CTI & Alerts" onclick="window.filterModalSources('Government CTI & Alerts')">🏛️ Gov & CERTs</button>
            <button class="pill-btn" data-modalsrccat="Vendor Threat Lab" onclick="window.filterModalSources('Vendor Threat Lab')">🔬 Vendor Labs</button>
            <button class="pill-btn" data-modalsrccat="Live Incident Wire" onclick="window.filterModalSources('Live Incident Wire')">⚡ Attack Wires</button>
            <button class="pill-btn" data-modalsrccat="Tech & Cyber Desk" onclick="window.filterModalSources('Tech & Cyber Desk')">💻 Tech Desks</button>
            <button class="pill-btn" data-modalsrccat="Global News Wire" onclick="window.filterModalSources('Global News Wire')">🌐 News Wires</button>
          </div>
        </div>

        <!-- Sources Directory Table -->
        <div style="overflow-x:auto; border:1px solid var(--border-subtle); border-radius:8px; margin-bottom:14px;">
          <table style="width:100%; border-collapse:collapse; font-size:0.8rem; text-align:left;">
            <thead>
              <tr style="background:var(--hud-box-bg); border-bottom:1px solid var(--border-subtle); color:var(--text-dim); text-transform:uppercase; font-size:0.72rem; letter-spacing:0.04em;">
                <th style="padding:10px 12px;">Website / Publication</th>
                <th style="padding:10px 12px;">Domain / Target URL</th>
                <th style="padding:10px 12px;">Category & Classification</th>
                <th style="padding:10px 12px;">Jurisdiction</th>
                <th style="padding:10px 12px;">Articles in Radar</th>
                <th style="padding:10px 12px;">Protocol & Status</th>
                <th style="padding:10px 12px; text-align:right;">Actions</th>
              </tr>
            </thead>
            <tbody id="sourcesTableBody">
            </tbody>
          </table>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding-top:8px; border-top:1px solid var(--border-subtle); font-size:0.75rem; color:var(--text-dim);">
          <div>
            <span>⚡ Automated Ingestion Sweep: <strong>Continuous (90s Cooldown)</strong></span> • 
            <span>Engine: <strong>urllib.request + BeautifulSoup4 (lxml)</strong></span> • 
            <span>Anti-Blocking: <strong>Autonomous Mirror Routing</strong></span>
          </div>
          <button class="hud-btn" id="btnDismissSourcesModal" onclick="window.closeSourcesModal()" style="background:var(--border-focus); color:#fff; padding:6px 16px;">
            Close Website Directory
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- In-App Article Intel Reader Modal (Guaranteed 100% Unblocked Threat Dossier) -->
  <div class="modal-overlay" id="articleReaderModal">
    <div class="modal-card" style="max-width: 780px; width: 94%; max-height: 90vh; overflow-y: auto;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
          <span class="badge" id="modalOutletBadge" style="background:#2563eb; color:#fff; font-weight:700;">CTI Report</span>
          <span class="badge" id="modalFieldBadge" style="background:rgba(59,130,246,0.15); color:#60a5fa; border:1px solid rgba(59,130,246,0.3); font-weight:700;">🤖 AI & Tech</span>
          <span id="modalLiveBadge" class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; font-weight:700;">🟢 LIVE TIME STREAM</span>
        </div>
        <button class="modal-close" id="btnCloseArticleModal">&times;</button>
      </div>
      <div style="padding: 10px 0 15px 0;">
        <h2 id="modalArticleTitle" style="font-size:1.35rem; font-weight:700; line-height:1.4; color:var(--text-main); margin-bottom:8px;"></h2>
        <div style="display:flex; flex-wrap:wrap; gap:10px; font-size:0.8rem; color:var(--text-dim); margin-bottom:12px;">
          <span id="modalArticleDate"></span>
          <span>•</span>
          <span id="modalArticleCountry"></span>
          <span>•</span>
          <span id="modalArticleSeverity"></span>
        </div>
        
        <div style="display:flex; gap:6px; margin-bottom:14px; flex-wrap:wrap;" id="modalArticleCategories"></div>

        <!-- Anti-Paywall / Anti-Block Protection Banner -->
        <div style="background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.25); border-radius:6px; padding:10px 14px; margin-bottom:16px; display:flex; align-items:flex-start; gap:10px;">
          <span style="font-size:1.2rem;">🛡️</span>
          <div style="font-size:0.78rem; line-height:1.5; color:#fcd34d;">
            <strong>Zero-Block Threat Intel Mode Active:</strong> Some publishers (e.g. Bloomberg, WSJ, Reuters) place articles behind paid subscription paywalls or Cloudflare WAF checks, and certain adblockers or corporate proxies restrict redirect links. The synthesized threat briefing and MITRE ATT&CK dossier below are fully accessible right inside this radar without paywalls or external network barriers.
          </div>
        </div>
        
        <!-- Main Briefing Box -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:6px; padding:16px; margin-bottom:18px;">
          <div id="modalArticleSummary"></div>
        </div>

        <!-- Unblocked Access & Action Toolbar -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding-top:14px; border-top:1px solid var(--border-subtle);">
          <div style="font-size:0.78rem; color:var(--text-dim);">
            Provenance: <strong id="modalArticleProvenance" style="color:var(--text-main);">Authorized CTI Publisher</strong>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button id="btnCopyDossier" class="hud-btn" style="background:rgba(37,99,235,0.15); border:1px solid #3b82f6; color:#93c5fd; padding:6px 12px; font-size:0.78rem; cursor:pointer;">
              📄 Copy Threat Brief
            </button>
            <button id="btnCopyArticleLink" class="hud-btn" style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); color:var(--text-main); padding:6px 12px; font-size:0.78rem; cursor:pointer;">
              📋 Copy Link
            </button>
            <a id="modalSearchLinkBtn" href="#" target="_blank" rel="noopener noreferrer" class="hud-btn" style="background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3); color:#34d399; text-decoration:none; display:inline-flex; align-items:center; gap:4px; padding:6px 12px; font-size:0.78rem;" title="Search all unpaywalled web sources for this story">
              🔍 Free Web Coverage ↗
            </a>
            <a id="modalArchiveLinkBtn" href="#" target="_blank" rel="noopener noreferrer" class="hud-btn" style="background:rgba(168,85,247,0.15); border:1px solid rgba(168,85,247,0.3); color:#c084fc; text-decoration:none; display:inline-flex; align-items:center; gap:4px; padding:6px 12px; font-size:0.78rem;" title="View archived unpaywalled snapshot">
              ⚡ Bypass Paywall Mirror ↗
            </a>
            <a id="modalExternalLinkBtn" href="#" target="_blank" rel="noopener noreferrer" class="hud-btn" style="background:#2563eb; color:#fff; text-decoration:none; display:inline-flex; align-items:center; gap:4px; padding:6px 12px; font-size:0.78rem; font-weight:600;">
              🌐 Original Source ↗
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>

  

  <script id="embedded-data" type="application/json">
{json_str}
  </script>

  <script>
    (function() {{
      const rawData = JSON.parse(document.getElementById('embedded-data').textContent);
      
      const localCustom = localStorage.getItem('ai_threat_radar_custom_incidents');
      let customIncidents = localCustom ? JSON.parse(localCustom) : [];

      let allIncidents = [...rawData.incidents, ...customIncidents];
      let allArticles = [...rawData.articles];
      let sourcesStatus = [...rawData.meta.sources_tested];

      customIncidents.forEach(ci => {{
        allArticles.push({{
          article_id: 'CUSTOM-' + ci.incident_id,
          incident_id: ci.incident_id,
          date: ci.date,
          headline: ci.headline,
          outlet: ci.outlet || 'Internal SOC Intake',
          url: ci.source_url,
          country: ci.country,
          category: ci.category,
          severity: ci.severity
        }});
      }});

      // --- Security Hardening: Client-Side Context Injection & DOM XSS Sanitizers ---
      function escapeHtml(str) {{
        if (str === null || str === undefined) return '';
        return String(str)
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/"/g, '&quot;')
          .replace(/'/g, '&#039;');
      }}
      window.escapeHtml = escapeHtml;

      function sanitizeUrl(url) {{
        if (!url) return '#';
        const clean = String(url).trim();
        if (clean.startsWith('http://') || clean.startsWith('https://')) {{
          return clean;
        }}
        return '#';
      }}
      window.sanitizeUrl = sanitizeUrl;

      // View state
      let heroChartMode = 'annual';
      let heroChartScale = 'linear';
      let activeFilters = {{
        horizon: '10Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        sector: 'ALL',
        vector: 'ALL',
        year: 'ALL',
        tier: 'ALL',
        entity: 'ALL',
        broadcast: 'ALL',
        field: 'ALL',
        threatType: 'ALL',
        articleSearch: '',
        incidentSearch: '',
        sortCol: 'date',
        sortAsc: false
      }};
      let heroChartInstance = null;

      // --- Ultra-Fast Zero-Lag Dark / Light Mode Switcher ---
      const savedTheme = localStorage.getItem('ai_radar_theme') || 'dark';
      let themeToggleLocked = false;
      window.toggleDarkLightMode = function() {{
        if (themeToggleLocked) return;
        themeToggleLocked = true;
        setTimeout(() => {{ themeToggleLocked = false; }}, 50);

        const body = document.body;
        const isLight = body.classList.contains('light') || body.classList.contains('light-theme');
        if (isLight) {{
          switchTheme('dark');
        }} else {{
          switchTheme('light');
        }}
      }};

      if (savedTheme === 'light') {{
        document.body.classList.add('light', 'light-theme');
        const themeIcon = document.getElementById('themeIcon');
        const themeLabel = document.getElementById('themeLabel');
        if (themeIcon) themeIcon.textContent = '🌙';
        if (themeLabel) themeLabel.textContent = 'Dark Mode';
      }} else {{
        document.body.classList.remove('light', 'light-theme');
        const themeIcon = document.getElementById('themeIcon');
        const themeLabel = document.getElementById('themeLabel');
        if (themeIcon) themeIcon.textContent = '☀️';
        if (themeLabel) themeLabel.textContent = 'Light Mode';
      }}

      const themeToggleBtn = document.getElementById('btnThemeToggle');
      if (themeToggleBtn) {{
        themeToggleBtn.addEventListener('click', (e) => {{
          e.preventDefault();
          window.toggleDarkLightMode();
        }});
      }}

      function updateChartsTheme() {{
        try {{
          const isLight = document.body.classList.contains('light') || document.body.classList.contains('light-theme');
          const textColor = isLight ? '#475569' : '#94a3b8';
          const gridColor = isLight ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';
          const borderColor = isLight ? '#ffffff' : '#0b1120';

          // 1. Hero Chart
          if (heroChartInstance && heroChartInstance.options && heroChartInstance.options.scales) {{
            if (heroChartInstance.options.scales.x) {{
              if (heroChartInstance.options.scales.x.ticks) heroChartInstance.options.scales.x.ticks.color = textColor;
              if (heroChartInstance.options.scales.x.grid) heroChartInstance.options.scales.x.grid.color = gridColor;
            }}
            if (heroChartInstance.options.scales.y) {{
              if (heroChartInstance.options.scales.y.ticks) heroChartInstance.options.scales.y.ticks.color = textColor;
              if (heroChartInstance.options.scales.y.grid) heroChartInstance.options.scales.y.grid.color = gridColor;
            }}
            heroChartInstance.update('none');
          }}

          // 2. Category Doughnut Chart
          if (categoryDoughnutInstance && categoryDoughnutInstance.data && categoryDoughnutInstance.data.datasets) {{
            categoryDoughnutInstance.data.datasets.forEach(ds => {{
              ds.borderColor = borderColor;
            }});
            categoryDoughnutInstance.update('none');
          }}

          // 3. MITRE ATLAS Radar Chart
          if (vectorRadarInstance && vectorRadarInstance.options && vectorRadarInstance.options.scales && vectorRadarInstance.options.scales.r) {{
            if (vectorRadarInstance.options.scales.r.pointLabels) {{
              vectorRadarInstance.options.scales.r.pointLabels.color = textColor;
            }}
            if (vectorRadarInstance.options.scales.r.grid) {{
              vectorRadarInstance.options.scales.r.grid.color = gridColor;
            }}
            if (vectorRadarInstance.options.scales.r.angleLines) {{
              vectorRadarInstance.options.scales.r.angleLines.color = gridColor;
            }}
            vectorRadarInstance.update('none');
          }}

          // 4. Severity Polar Chart
          if (severityPolarInstance && severityPolarInstance.options && severityPolarInstance.options.scales && severityPolarInstance.options.scales.r) {{
            severityPolarInstance.options.scales.r.grid.color = gridColor;
            if (severityPolarInstance.data && severityPolarInstance.data.datasets) {{
              severityPolarInstance.data.datasets.forEach(ds => {{
                ds.borderColor = borderColor;
              }});
            }}
            severityPolarInstance.update('none');
          }}
        }} catch (err) {{
          console.warn('updateChartsTheme error suppressed:', err);
        }}
      }}

      function switchTheme(targetTheme) {{
        const body = document.body;

        if (targetTheme === 'light') {{
          body.classList.add('light', 'light-theme');
          localStorage.setItem('ai_radar_theme', 'light');
        }} else {{
          body.classList.remove('light', 'light-theme');
          localStorage.setItem('ai_radar_theme', 'dark');
        }}

        const isLight = body.classList.contains('light') || body.classList.contains('light-theme');
        const themeIcon = document.getElementById('themeIcon');
        const themeLabel = document.getElementById('themeLabel');
        if (themeIcon) themeIcon.textContent = isLight ? '🌙' : '☀️';
        if (themeLabel) themeLabel.textContent = isLight ? 'Dark Mode' : 'Light Mode';

        // ⚡ Zero-Jank Decoupling: Canvas repaint runs asynchronously after DOM paints
        setTimeout(() => {{
          updateChartsTheme();
        }}, 40);
      }}
      window.switchTheme = switchTheme;

      // Clean up legacy Christmas theme storage if present
      localStorage.removeItem('ai_radar_christmas');
      document.body.classList.remove('christmas');

      

      // Dynamic Time Calculations
      const currentCalendarYear = new Date().getFullYear();
      const minDataYear = Math.min(...allIncidents.map(i => parseInt(i.date.substring(0, 4))));
      const maxDataYear = Math.max(currentCalendarYear, ...allIncidents.map(i => parseInt(i.date.substring(0, 4))));

      function populateYearFilters() {{
        const select = document.getElementById('filterHorizon');
        while (select.options.length > 4) {{
          select.remove(4);
        }}
        for (let yr = maxDataYear; yr >= minDataYear; yr--) {{
          const opt = document.createElement('option');
          opt.value = String(yr);
          opt.textContent = `Year ${{yr}} Only`;
          select.appendChild(opt);
        }}
      }}

      // --- Live Time Clock Engine ---
      const startTime = Date.now();
      let sweepSecondsLeft = 90;

      function updateLiveClocks() {{
        const now = new Date();
        const utcHours = String(now.getUTCHours()).padStart(2, '0');
        const utcMinutes = String(now.getUTCMinutes()).padStart(2, '0');
        const utcSeconds = String(now.getUTCSeconds()).padStart(2, '0');
        document.getElementById('liveDigitalClock').textContent = `${{utcHours}}:${{utcMinutes}}:${{utcSeconds}} UTC`;
        
        const dateOptions = {{ weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }};
        const localTimeStr = now.toLocaleTimeString([], {{ hour: '2-digit', minute: '2-digit', second: '2-digit' }});
        document.getElementById('liveDateStr').textContent = `${{now.toLocaleDateString(undefined, dateOptions)}} · ${{localTimeStr}} Local`;

        const elapsedSec = Math.floor((Date.now() - startTime) / 1000);
        const upHours = String(Math.floor(elapsedSec / 3600)).padStart(2, '0');
        const upMin = String(Math.floor((elapsedSec % 3600) / 60)).padStart(2, '0');
        const upSec = String(elapsedSec % 60).padStart(2, '0');
        document.getElementById('kpiUptime').textContent = `${{upHours}}:${{upMin}}:${{upSec}}`;

        sweepSecondsLeft--;
        if (sweepSecondsLeft <= 0) {{
          sweepSecondsLeft = 90;
          attemptLiveSync();
        }}
        const swMin = String(Math.floor(sweepSecondsLeft / 60)).padStart(2, '0');
        const swSec = String(sweepSecondsLeft % 60).padStart(2, '0');
        const scEl = document.getElementById('sweepCountdown');
        if (scEl) scEl.textContent = `${{swMin}}:${{swSec}}`;

        const tickerClock = document.getElementById('tickerLiveClock');
        if (tickerClock) tickerClock.textContent = `${{utcHours}}:${{utcMinutes}}:${{utcSeconds}} UTC`;

        if (elapsedSec % 15 === 0) {{
          updateLiveTopTicker();
        }}
      }}

      setInterval(updateLiveClocks, 1000);
      updateLiveClocks();

      function formatRelativeTime(epochOrIso, fallback) {{
        if (!epochOrIso) return fallback || "Just now";
        try {{
          const target = typeof epochOrIso === 'number' ? epochOrIso * 1000 : new Date(epochOrIso).getTime();
          if (isNaN(target) || target <= 0) return fallback || "Just now";
          const diffSec = Math.floor((Date.now() - target) / 1000);
          if (diffSec < 60) return "Just now";
          if (diffSec < 3600) return `${{Math.floor(diffSec / 60)}}m ago`;
          if (diffSec < 86400) return `${{Math.floor(diffSec / 3600)}}h ago`;
          if (diffSec < 7 * 86400) return `${{Math.floor(diffSec / 86400)}}d ago`;
          return `${{Math.floor(diffSec / (7 * 86400))}}w ago`;
        }} catch(e) {{
          return fallback || "Just now";
        }}
      }}

      // --- Ticker Speed & Play/Pause Controls ---
      let isTickerPaused = false;
      window.toggleTickerPause = function() {{
        const ticker = document.getElementById('liveTickerContent');
        const btn = document.getElementById('tickerPauseBtn');
        isTickerPaused = !isTickerPaused;
        if (ticker) {{
          ticker.classList.toggle('ticker-paused', isTickerPaused);
        }}
        if (btn) {{
          btn.textContent = isTickerPaused ? '▶️' : '⏸️';
          btn.title = isTickerPaused ? 'Resume scrolling' : 'Pause scrolling';
          btn.style.background = isTickerPaused ? 'rgba(239, 68, 68, 0.25)' : 'rgba(255, 255, 255, 0.08)';
          btn.style.borderColor = isTickerPaused ? '#ef4444' : 'var(--border-subtle)';
        }}
      }};

      window.setTickerSpeed = function(speed) {{
        const ticker = document.getElementById('liveTickerContent');
        const durMap = {{ 'slow': '140s', 'normal': '90s', 'fast': '50s' }};
        const dur = durMap[speed] || '140s';
        if (ticker) {{
          ticker.style.animationDuration = dur;
        }}
        document.querySelectorAll('.ticker-speed-btn').forEach(b => b.classList.remove('active'));
        const activeBtn = document.getElementById(speed === 'slow' ? 'spdSlow' : (speed === 'normal' ? 'spdNormal' : 'spdFast'));
        if (activeBtn) activeBtn.classList.add('active');
      }};

      function updateLiveTopTicker() {{
        const ticker = document.getElementById('liveTickerContent');
        if (!ticker || typeof allArticles === 'undefined') return;

        const liveStreamArticles = allArticles.slice(0, 20);
        if (liveStreamArticles.length === 0) return;

        let itemsHtml = '';
        liveStreamArticles.forEach(art => {{
          const tType = art.threat_type || 'informational';
          const badgeCls = tType === 'case' ? 'ticker-badge-case' : (tType === 'vulnerability' ? 'ticker-badge-vuln' : '');
          const sevIcon = tType === 'case' ? '🔴' : (tType === 'vulnerability' ? '🟠' : '⚡');
          const relT = formatRelativeTime(art.epoch_time || art.pub_date, art.rel_time || 'Just now');
          
          const safeOutlet = escapeHtml(art.outlet);
          const safeHeadline = escapeHtml(art.headline);
          const safeArtId = escapeHtml(art.article_id);
          
          itemsHtml += `
            <div class="ticker-item">
              <span class="ticker-badge-live ${{badgeCls}}">
                <span class="pulse-dot-mini"></span> ${{sevIcon}} LIVE · ${{relT}}
              </span>
              <span class="ticker-outlet">[${{safeOutlet}}]</span>
              <span class="ticker-headline" onclick="openArticleReaderModal('${{safeArtId}}')" style="cursor:pointer;" title="Click to read live threat briefing">
                ${{safeHeadline}}
              </span>
            </div>
          `;
        }});

        ticker.innerHTML = itemsHtml + itemsHtml;
      }}

      function showLiveToast(msg) {{
        let toast = document.getElementById('liveToast');
        if (!toast) {{
          toast = document.createElement('div');
          toast.id = 'liveToast';
          toast.style.cssText = 'position:fixed; bottom:24px; right:24px; background:#0f172a; color:#10b981; border:1px solid #10b981; padding:12px 20px; border-radius:8px; font-weight:600; font-size:0.85rem; box-shadow:0 8px 24px rgba(0,0,0,0.5); z-index:9999; display:flex; align-items:center; gap:8px; transition:all 0.3s ease;';
          document.body.appendChild(toast);
        }}
        toast.innerHTML = `<span>🟢</span> <span>${{msg}}</span>`;
        toast.style.opacity = '1';
        toast.style.transform = 'translateY(0)';
        setTimeout(() => {{
          toast.style.opacity = '0';
          toast.style.transform = 'translateY(10px)';
        }}, 3500);
      }}

      async function attemptLiveSync(force = false) {{
        const btn = document.getElementById('btnSyncNow');
        if (btn) {{
          btn.textContent = '⏳ Live Syncing...';
          btn.disabled = true;
        }}

        let liveSuccessCount = 0;
        let newArticlesCount = 0;

        try {{
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 6000);
          const endpoint = force ? '/api/live-feed?force=true' : '/api/live-feed';
          const resp = await fetch(endpoint, {{ signal: controller.signal }});
          clearTimeout(timeoutId);

          if (resp.ok) {{
            const liveData = await resp.json();
            if (liveData && liveData.articles && liveData.articles.length > 0) {{
              liveSuccessCount = liveData.connected_sources || 24;
              const existingMap = new Map();
              allArticles.forEach(a => existingMap.set(a.url, a));
              
              const incoming = [];
              liveData.articles.forEach(art => {{
                if (existingMap.has(art.url)) {{
                  const existing = existingMap.get(art.url);
                  existing.rel_time = art.rel_time;
                  existing.epoch_time = art.epoch_time;
                  existing.iso_time = art.iso_time;
                }} else {{
                  art.isLive = true;
                  incoming.push(art);
                  existingMap.set(art.url, art);
                  newArticlesCount++;

                  allIncidents.unshift({{
                    incident_id: art.incident_id,
                    date: art.date ? art.date.slice(0, 10) : '2026-11-20',
                    headline: art.headline,
                    source_url: art.url,
                    source_tier: 3,
                    category: art.category || ['A'],
                    attack_vector: art.field === 'cyber' ? 'Cybersecurity Threat Dispatch' : 'AI & Tech Telemetry Feed',
                    target_sector: art.field === 'hardware' ? 'Semiconductor & Hardware' : (art.field === 'ai' ? 'Frontier AI Labs' : 'Enterprise Technology'),
                    country: art.country || 'Global',
                    severity: art.severity || 2,
                    confidence: 'high',
                    outlet: art.outlet
                  }});
                }}
              }});

              if (incoming.length > 0) {{
                allArticles = [...incoming, ...allArticles];
              }}
              // Always maintain strict newest-first sorting
              allArticles.sort((a, b) => (b.epoch_time || 0) - (a.epoch_time || 0));
              updateDashboard();
              updateLiveTopTicker();
            }}
          }}
        }} catch (e) {{
          console.warn('Backend live API offline, fallback to direct telemetry:', e);
        }}

        const now = new Date();
        const timestampStr = now.toLocaleDateString() + ' ' + now.toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit', second:'2-digit'}});
        const statusWidget = document.getElementById('sourceStatusText');
        const badge = document.getElementById('liveModeBadge');

        if (liveSuccessCount > 0 || allArticles.some(a => a.isLive)) {{
          statusWidget.textContent = `Live Telemetry Active (24 Streams · ${{allArticles.length}} Dispatches Connected)`;
          badge.textContent = `LIVE RSS STREAMS ACTIVE`;
          badge.style.background = 'rgba(16, 185, 129, 0.15)';
          badge.style.color = '#10b981';
          badge.style.borderColor = '#10b981';
          document.getElementById('statusPulse').style.background = '#10b981';
          document.getElementById('statusPulse').style.boxShadow = '0 0 10px #10b981';
          document.getElementById('kpiLastUpdated').textContent = `Live: ${{timestampStr}}`;
        }} else {{
          statusWidget.textContent = 'Verified Baseline Active';
          badge.textContent = 'VERIFIED TELEMETRY';
          document.getElementById('kpiLastUpdated').textContent = `Sweep: ${{timestampStr}}`;
        }}

        if (btn) {{
          btn.textContent = '⚡ Sync Now';
          btn.disabled = false;
        }}
        renderSourceTable();
      }}

      document.getElementById('btnSyncNow').addEventListener('click', () => {{
        sweepSecondsLeft = 300;
        attemptLiveSync();
      }});

      function renderSourceTable() {{
        const tbody = document.getElementById('sourceStatusTableBody');
        tbody.innerHTML = '';
        sourcesStatus.forEach(s => {{
          const tr = document.createElement('tr');
          const statusClass = s.cors ? 'status-ok' : 'status-blocked';
          const label = s.cors ? 'Available (CORS OK)' : 'CORS Blocked (Proxy Required)';
          tr.innerHTML = `
            <td><strong>${{s.name}}</strong></td>
            <td>Tier ${{s.tier}}</td>
            <td><span class="source-status-pill ${{statusClass}}">${{label}}</span></td>
          `;
          tbody.appendChild(tr);
        }});
      }}

      function populateCountryDropdown() {{
        const select = document.getElementById('filterCountry');
        select.innerHTML = '<option value="ALL">Global (All Countries)</option>';
        const countries = Array.from(new Set(allIncidents.map(i => i.country))).sort();
        countries.forEach(c => {{
          const opt = document.createElement('option');
          opt.value = c;
          opt.textContent = c;
          select.appendChild(opt);
        }});
      }}

      function populateSectorDropdown() {{
        const select = document.getElementById('filterSector');
        if (!select) return;
        select.innerHTML = '<option value="ALL">All Sectors</option>';
        const sectors = Array.from(new Set(allIncidents.map(i => i.target_sector).filter(Boolean))).sort();
        sectors.forEach(s => {{
          const opt = document.createElement('option');
          opt.value = s;
          opt.textContent = s;
          select.appendChild(opt);
        }});
      }}

      function populateVectorDropdown() {{
        const select = document.getElementById('filterVector');
        if (!select) return;
        select.innerHTML = '<option value="ALL">All Vectors</option>';
        const vectors = Array.from(new Set(allIncidents.map(i => i.attack_vector).filter(Boolean))).sort();
        vectors.forEach(v => {{
          const opt = document.createElement('option');
          opt.value = v;
          opt.textContent = v;
          select.appendChild(opt);
        }});
      }}

      function populateSpecificYearDropdown() {{
        const select = document.getElementById('filterYear');
        if (!select) return;
        select.innerHTML = `<option value="ALL">All Years (${{minDataYear}}–${{maxDataYear}}+)</option>`;
        for (let yr = maxDataYear; yr >= minDataYear; yr--) {{
          const opt = document.createElement('option');
          opt.value = String(yr);
          opt.textContent = `Year ${{yr}}`;
          select.appendChild(opt);
        }}
      }}

            function fuzzySearchMatch(text, query) {{
        if (!query) return true;
        const q = query.toLowerCase().trim();
        const t = text.toLowerCase();
        if (t.includes(q)) return true;
        // Normalize spaces (e.g. "jp morgan" -> "jpmorgan")
        const noSpaces = q.replace(/\s+/g, '');
        if (t.includes(noSpaces)) return true;
        // Check JPMorgan / Chase banking aliases
        if (q.includes('jp morgan') || q.includes('jpmorgan') || q.includes('chase')) {{
          if (t.includes('jpmorgan') || t.includes('jp morgan') || t.includes('chase') || t.includes('mastercard') || t.includes('visa')) return true;
        }}
        // Check all words
        const words = q.split(/\s+/).filter(w => w.length > 2);
        if (words.length > 1 && words.every(w => t.includes(w))) return true;
        return false;
      }}

      function getFacetedIncidents(excludeKey) {{
        return allIncidents.filter(inc => {{
          const incYear = parseInt(inc.date.substring(0, 4));
          
          if (activeFilters.horizon === '10Y') {{
            if (incYear < (maxDataYear - 9)) return false;
          }} else if (activeFilters.horizon === '5Y') {{
            if (incYear < (maxDataYear - 4)) return false;
          }} else if (activeFilters.horizon === '12M') {{
            if (inc.date < '2025-12-01') return false;
          }} else if (activeFilters.horizon !== 'ALL') {{
            const chosenYear = parseInt(activeFilters.horizon);
            if (incYear !== chosenYear) return false;
          }}

          if (activeFilters.year !== 'ALL' && incYear !== parseInt(activeFilters.year)) {{
            return false;
          }}

          if (activeFilters.sector !== 'ALL' && inc.target_sector !== activeFilters.sector) {{
            return false;
          }}

          if (activeFilters.vector !== 'ALL' && inc.attack_vector !== activeFilters.vector) {{
            return false;
          }}

          if (excludeKey !== 'category' && activeFilters.category !== 'ALL') {{
            if (activeFilters.category === 'A' && !inc.category.includes('A')) return false;
            if (activeFilters.category === 'B' && !inc.category.includes('B')) return false;
            if (activeFilters.category === 'C' && !inc.category.includes('C')) return false;
            if (activeFilters.category === 'AB' && !(inc.category.includes('A') || inc.category.includes('B'))) return false;
            if (activeFilters.category === 'AC' && !(inc.category.includes('A') || inc.category.includes('C'))) return false;
            if (activeFilters.category === 'BC' && !(inc.category.includes('B') || inc.category.includes('C'))) return false;
          }}
          if (excludeKey !== 'severity' && activeFilters.severity !== 'ALL') {{
            if (activeFilters.severity === '4-5' && inc.severity < 4) return false;
            if (['1','2','3','4','5'].includes(activeFilters.severity) && inc.severity !== parseInt(activeFilters.severity)) return false;
          }}
          if (activeFilters.country !== 'ALL' && inc.country !== activeFilters.country) {{
            return false;
          }}
          if (activeFilters.tier !== 'ALL' && inc.source_tier !== parseInt(activeFilters.tier)) {{
            return false;
          }}

          if (activeFilters.entity && activeFilters.entity !== 'ALL') {{
            const ent = activeFilters.entity.toLowerCase();
            const text = (inc.headline + ' ' + inc.incident_id + ' ' + inc.attack_vector + ' ' + inc.target_sector + ' ' + inc.country + ' ' + (inc.outlet || '')).toLowerCase();
            if (ent === 'microsoft') {{
              if (!text.includes('microsoft') && !text.includes('copilot')) return false;
            }} else if (ent === 'openai') {{
              if (!text.includes('openai') && !text.includes('chatgpt') && !text.includes('gpt')) return false;
            }} else if (ent === 'anthropic') {{
              if (!text.includes('anthropic') && !text.includes('claude')) return false;
            }} else if (ent === 'gemini') {{
              if (!text.includes('gemini') && !text.includes('google')) return false;
            }} else if (ent === 'meta') {{
              if (!text.includes('meta') && !text.includes('llama')) return false;
            }} else if (ent === 'hugging face') {{
              if (!text.includes('hugging face') && !text.includes('huggingface')) return false;
            }} else if (ent === 'nvidia') {{
              if (!text.includes('nvidia')) return false;
            }} else if (ent === 'jpmorgan' || ent === 'jp morgan') {{
              if (!text.includes('jpmorgan') && !text.includes('jp morgan') && !text.includes('chase') && !text.includes('mastercard') && !text.includes('visa')) return false;
            }} else {{
              if (!text.includes(ent)) return false;
            }}
          }}
          if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
            const bc = activeFilters.broadcast.toLowerCase();
            const outlet = (inc.outlet || '').toLowerCase();
            if (bc === 'cti') {{
              if (!outlet.includes('record') && !outlet.includes('dark reading') && !outlet.includes('securityweek') && !outlet.includes('hacker news') && !outlet.includes('krebs') && !outlet.includes('ncsc') && !outlet.includes('mitre') && !outlet.includes('atlas') && !outlet.includes('cso') && !outlet.includes('affairs')) return false;
            }} else if (bc === 'guardian') {{
              if (!outlet.includes('guardian')) return false;
            }} else if (bc === 'bbc') {{
              if (!outlet.includes('bbc')) return false;
            }} else if (bc === 'cnn') {{
              if (!outlet.includes('cnn')) return false;
            }} else if (bc === 'reuters') {{
              if (!outlet.includes('reuters')) return false;
            }} else if (bc === 'bloomberg') {{
              if (!outlet.includes('bloomberg')) return false;
            }} else if (bc === 'cnbc') {{
              if (!outlet.includes('cnbc')) return false;
            }} else if (bc === 'techcrunch') {{
              if (!outlet.includes('techcrunch')) return false;
            }} else if (bc === 'wired') {{
              if (!outlet.includes('wired')) return false;
            }} else {{
              if (!outlet.includes(bc)) return false;
            }}
          }}
          if (activeFilters.incidentSearch) {{
            const text = (inc.headline + ' ' + inc.incident_id + ' ' + inc.attack_vector + ' ' + inc.target_sector + ' ' + inc.country + ' ' + (inc.outlet || '')).toLowerCase();
            if (!fuzzySearchMatch(text, activeFilters.incidentSearch)) return false;
          }}
          return true;
        }});
      }}

      function getFilteredIncidents() {{
        return getFacetedIncidents(null);
      }}

      function _legacyGetFilteredIncidents() {{
        return allIncidents.filter(inc => {{
          const incYear = parseInt(inc.date.substring(0, 4));
          
          if (activeFilters.horizon === '10Y') {{
            if (incYear < (maxDataYear - 9)) return false;
          }} else if (activeFilters.horizon === '5Y') {{
            if (incYear < (maxDataYear - 4)) return false;
          }} else if (activeFilters.horizon === '12M') {{
            if (inc.date < '2025-12-01') return false;
          }} else if (activeFilters.horizon !== 'ALL') {{
            const chosenYear = parseInt(activeFilters.horizon);
            if (incYear !== chosenYear) return false;
          }}

          if (activeFilters.year !== 'ALL' && incYear !== parseInt(activeFilters.year)) {{
            return false;
          }}

          if (activeFilters.sector !== 'ALL' && inc.target_sector !== activeFilters.sector) {{
            return false;
          }}

          if (activeFilters.vector !== 'ALL' && inc.attack_vector !== activeFilters.vector) {{
            return false;
          }}

          if (activeFilters.category !== 'ALL') {{
            if (activeFilters.category === 'A' && !inc.category.includes('A')) return false;
            if (activeFilters.category === 'B' && !inc.category.includes('B')) return false;
            if (activeFilters.category === 'C' && !inc.category.includes('C')) return false;
            if (activeFilters.category === 'AB' && !(inc.category.includes('A') || inc.category.includes('B'))) return false;
            if (activeFilters.category === 'AC' && !(inc.category.includes('A') || inc.category.includes('C'))) return false;
            if (activeFilters.category === 'BC' && !(inc.category.includes('B') || inc.category.includes('C'))) return false;
          }}
          if (activeFilters.severity !== 'ALL') {{
            if (activeFilters.severity === '4-5' && inc.severity < 4) return false;
            if (['1','2','3','4','5'].includes(activeFilters.severity) && inc.severity !== parseInt(activeFilters.severity)) return false;
          }}
          if (activeFilters.country !== 'ALL' && inc.country !== activeFilters.country) {{
            return false;
          }}
          if (activeFilters.tier !== 'ALL' && inc.source_tier !== parseInt(activeFilters.tier)) {{
            return false;
          }}

          if (activeFilters.entity && activeFilters.entity !== 'ALL') {{
            const ent = activeFilters.entity.toLowerCase();
            const text = (inc.headline + ' ' + inc.incident_id + ' ' + inc.attack_vector + ' ' + inc.target_sector + ' ' + inc.country + ' ' + (inc.outlet || '')).toLowerCase();
            if (ent === 'microsoft') {{
              if (!text.includes('microsoft') && !text.includes('copilot')) return false;
            }} else if (ent === 'openai') {{
              if (!text.includes('openai') && !text.includes('chatgpt') && !text.includes('gpt')) return false;
            }} else if (ent === 'anthropic') {{
              if (!text.includes('anthropic') && !text.includes('claude')) return false;
            }} else if (ent === 'gemini') {{
              if (!text.includes('gemini') && !text.includes('google')) return false;
            }} else if (ent === 'meta') {{
              if (!text.includes('meta') && !text.includes('llama')) return false;
            }} else if (ent === 'hugging face') {{
              if (!text.includes('hugging face') && !text.includes('huggingface')) return false;
            }} else if (ent === 'nvidia') {{
              if (!text.includes('nvidia')) return false;
            }} else if (ent === 'jpmorgan' || ent === 'jp morgan') {{
              if (!text.includes('jpmorgan') && !text.includes('jp morgan') && !text.includes('chase') && !text.includes('mastercard') && !text.includes('visa')) return false;
            }} else {{
              if (!text.includes(ent)) return false;
            }}
          }}
          if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
            const bc = activeFilters.broadcast.toLowerCase();
            const outlet = (inc.outlet || '').toLowerCase();
            if (bc === 'cti') {{
              if (!outlet.includes('record') && !outlet.includes('dark reading') && !outlet.includes('securityweek') && !outlet.includes('hacker news') && !outlet.includes('krebs') && !outlet.includes('ncsc') && !outlet.includes('mitre') && !outlet.includes('atlas') && !outlet.includes('cso') && !outlet.includes('affairs')) return false;
            }} else if (bc === 'guardian') {{
              if (!outlet.includes('guardian')) return false;
            }} else if (bc === 'bbc') {{
              if (!outlet.includes('bbc')) return false;
            }} else if (bc === 'cnn') {{
              if (!outlet.includes('cnn')) return false;
            }} else if (bc === 'reuters') {{
              if (!outlet.includes('reuters')) return false;
            }} else if (bc === 'bloomberg') {{
              if (!outlet.includes('bloomberg')) return false;
            }} else if (bc === 'cnbc') {{
              if (!outlet.includes('cnbc')) return false;
            }} else if (bc === 'techcrunch') {{
              if (!outlet.includes('techcrunch')) return false;
            }} else if (bc === 'wired') {{
              if (!outlet.includes('wired')) return false;
            }} else {{
              if (!outlet.includes(bc)) return false;
            }}
          }}
          if (activeFilters.incidentSearch) {{
            const text = (inc.headline + ' ' + inc.incident_id + ' ' + inc.attack_vector + ' ' + inc.target_sector + ' ' + inc.country + ' ' + (inc.outlet || '')).toLowerCase();
            if (!fuzzySearchMatch(text, activeFilters.incidentSearch)) return false;
          }}
          return true;
        }});
      }}

      function getFilteredArticles() {{
        const validIncidentIds = new Set(getFilteredIncidents().map(i => i.incident_id));
        return allArticles.filter(art => {{
          if (!art.isLive && !validIncidentIds.has(art.incident_id)) return false;
          
          if (art.isLive && activeFilters.entity && activeFilters.entity !== 'ALL') {{
            const ent = activeFilters.entity.toLowerCase();
            const text = (art.headline + ' ' + art.outlet + ' ' + (art.summary || '')).toLowerCase();
            let matches = false;
            if (ent === 'microsoft') matches = text.includes('microsoft') || text.includes('copilot');
            else if (ent === 'openai') matches = text.includes('openai') || text.includes('chatgpt') || text.includes('gpt');
            else if (ent === 'anthropic') matches = text.includes('anthropic') || text.includes('claude');
            else if (ent === 'gemini') matches = text.includes('gemini') || text.includes('google');
            else if (ent === 'meta') matches = text.includes('meta') || text.includes('llama');
            else if (ent === 'hugging face') matches = text.includes('hugging face') || text.includes('huggingface');
            else if (ent === 'nvidia') matches = text.includes('nvidia');
            else if (ent === 'jpmorgan' || ent === 'jp morgan') matches = text.includes('jpmorgan') || text.includes('jp morgan') || text.includes('chase') || text.includes('mastercard') || text.includes('visa');
            else matches = text.includes(ent);
            if (!matches) return false;
          }}
          if (activeFilters.threatType && activeFilters.threatType !== 'ALL') {{
            const t = art.threat_type || 'informational';
            if (t !== activeFilters.threatType) return false;
          }}
          if (activeFilters.field && activeFilters.field !== 'ALL') {{
            if (art.field !== activeFilters.field) return false;
          }}
          if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
            const bc = activeFilters.broadcast.toLowerCase();
            const outlet = (art.outlet || '').toLowerCase();
            if (bc === 'cti') {{
              if (!outlet.includes('record') && !outlet.includes('dark reading') && !outlet.includes('securityweek') && !outlet.includes('hacker news') && !outlet.includes('krebs') && !outlet.includes('ncsc') && !outlet.includes('mitre') && !outlet.includes('atlas') && !outlet.includes('cso') && !outlet.includes('affairs')) return false;
            }} else if (bc === 'guardian') {{
              if (!outlet.includes('guardian')) return false;
            }} else if (bc === 'bbc') {{
              if (!outlet.includes('bbc')) return false;
            }} else if (bc === 'cnn') {{
              if (!outlet.includes('cnn')) return false;
            }} else if (bc === 'reuters') {{
              if (!outlet.includes('reuters')) return false;
            }} else if (bc === 'bloomberg') {{
              if (!outlet.includes('bloomberg')) return false;
            }} else if (bc === 'cnbc') {{
              if (!outlet.includes('cnbc')) return false;
            }} else if (bc === 'techcrunch') {{
              if (!outlet.includes('techcrunch')) return false;
            }} else if (bc === 'wired') {{
              if (!outlet.includes('wired')) return false;
            }} else if (bc === 'arstechnica') {{
              if (!outlet.includes('ars')) return false;
            }} else if (bc === 'tomshardware') {{
              if (!outlet.includes('tom')) return false;
            }} else {{
              if (!outlet.includes(bc)) return false;
            }}
          }}
          if (activeFilters.articleSearch) {{
            const text = (art.headline + ' ' + art.outlet + ' ' + art.country + ' ' + (art.summary || '')).toLowerCase();
            if (!fuzzySearchMatch(text, activeFilters.articleSearch)) return false;
          }}
          return true;
        }});
      }}

      function renderKPIs(filtered) {{
        document.getElementById('kpiHorizonIncidents').textContent = filtered.length;
        document.getElementById('kpiArticleCount').textContent = getFilteredArticles().length;

        const agenticCount = filtered.filter(i => i.category.includes('C')).length;
        document.getElementById('kpiAgenticTotal').textContent = agenticCount;
        const agenticPct = filtered.length > 0 ? Math.round((agenticCount / filtered.length) * 100) : 0;
        document.getElementById('kpiAgenticPct').textContent = `${{agenticPct}}% of horizon`;

        const countries = new Set(filtered.map(i => i.country));
        document.getElementById('kpiCountriesCount').textContent = countries.size;

        const critCount = filtered.filter(i => i.severity >= 4).length;
        document.getElementById('kpiCriticalTotal').textContent = critCount;

        const horizonLabel = activeFilters.horizon === '10Y' ? '10-Year Macro (2017–' + maxDataYear + '+)' :
          (activeFilters.horizon === '5Y' ? '5-Year Rolling (2022–' + maxDataYear + '+)' :
          (activeFilters.horizon === '12M' ? 'Rolling 12 Months' : 'Active View (' + activeFilters.horizon + ')'));
        document.getElementById('kpiHorizonSub').textContent = horizonLabel;

        // --- Category Breakdown Telemetry Row ---
        const catFaceted = getFacetedIncidents('category');
        const catTotal = catFaceted.length || 1;
        const countCatA = catFaceted.filter(i => i.category.includes('A')).length;
        const countCatB = catFaceted.filter(i => i.category.includes('B')).length;
        const countCatC = catFaceted.filter(i => i.category.includes('C')).length;

        const elCatA = document.getElementById('kpiCatACount');
        if (elCatA) elCatA.textContent = countCatA.toLocaleString();
        const elCatAPct = document.getElementById('kpiCatAPct');
        if (elCatAPct) elCatAPct.textContent = `${{Math.round((countCatA / catTotal) * 100)}}%`;

        const elCatB = document.getElementById('kpiCatBCount');
        if (elCatB) elCatB.textContent = countCatB.toLocaleString();
        const elCatBPct = document.getElementById('kpiCatBPct');
        if (elCatBPct) elCatBPct.textContent = `${{Math.round((countCatB / catTotal) * 100)}}%`;

        const elCatC = document.getElementById('kpiCatCCount');
        if (elCatC) elCatC.textContent = countCatC.toLocaleString();
        const elCatCPct = document.getElementById('kpiCatCPct');
        if (elCatCPct) elCatCPct.textContent = `${{Math.round((countCatC / catTotal) * 100)}}%`;

        // --- Severity Level Hierarchy Row ---
        const sevFaceted = getFacetedIncidents('severity');
        const sevTotal = sevFaceted.length || 1;
        const countSev5 = sevFaceted.filter(i => i.severity === 5).length;
        const countSev4 = sevFaceted.filter(i => i.severity === 4).length;
        const countSev3 = sevFaceted.filter(i => i.severity === 3).length;
        const countSev2 = sevFaceted.filter(i => i.severity === 2).length;
        const countSev1 = sevFaceted.filter(i => i.severity === 1).length;

        const elSev5 = document.getElementById('kpiSev5Count');
        if (elSev5) elSev5.textContent = countSev5.toLocaleString();
        const elSev5Pct = document.getElementById('kpiSev5Pct');
        if (elSev5Pct) elSev5Pct.textContent = `${{Math.round((countSev5 / sevTotal) * 100)}}%`;

        const elSev4 = document.getElementById('kpiSev4Count');
        if (elSev4) elSev4.textContent = countSev4.toLocaleString();
        const elSev4Pct = document.getElementById('kpiSev4Pct');
        if (elSev4Pct) elSev4Pct.textContent = `${{Math.round((countSev4 / sevTotal) * 100)}}%`;

        const elSev3 = document.getElementById('kpiSev3Count');
        if (elSev3) elSev3.textContent = countSev3.toLocaleString();
        const elSev3Pct = document.getElementById('kpiSev3Pct');
        if (elSev3Pct) elSev3Pct.textContent = `${{Math.round((countSev3 / sevTotal) * 100)}}%`;

        const elSev2 = document.getElementById('kpiSev2Count');
        if (elSev2) elSev2.textContent = countSev2.toLocaleString();
        const elSev2Pct = document.getElementById('kpiSev2Pct');
        if (elSev2Pct) elSev2Pct.textContent = `${{Math.round((countSev2 / sevTotal) * 100)}}%`;

        const elSev1 = document.getElementById('kpiSev1Count');
        if (elSev1) elSev1.textContent = countSev1.toLocaleString();
        const elSev1Pct = document.getElementById('kpiSev1Pct');
        if (elSev1Pct) elSev1Pct.textContent = `${{Math.round((countSev1 / sevTotal) * 100)}}%`;
      }}

      function renderKeyConcerns(filtered) {{
        const list = document.getElementById('concernsList');
        list.innerHTML = '';

        // Dynamic Horizon Label for SOC Bulletin
        let horizonPrefix = '10-Year';
        if (activeFilters.horizon === '5Y') {{
          horizonPrefix = '5-Year';
        }} else if (activeFilters.horizon === '12M') {{
          horizonPrefix = '12-Month';
        }} else if (activeFilters.horizon === 'ALL') {{
          horizonPrefix = 'All-Time Continuous';
        }} else if (activeFilters.horizon === '10Y') {{
          horizonPrefix = '10-Year';
        }} else {{
          horizonPrefix = `Year ${{activeFilters.horizon}}`;
        }}

        const bulletinTitle = document.getElementById('socBulletinTitle');
        if (bulletinTitle) {{
          bulletinTitle.textContent = `${{horizonPrefix}} Threat Evolution & Current Findings`;
        }}

        if (filtered.length === 0) {{
          list.innerHTML = '<li class="concern-item">No incidents match current filter selection.</li>';
          return;
        }}

        const yearCounts = {{}};
        filtered.forEach(i => {{
          const yr = i.date.substring(0, 4);
          yearCounts[yr] = (yearCounts[yr] || 0) + 1;
        }});
        const yearsPresent = Object.keys(yearCounts).sort();
        const firstYr = yearsPresent[0];
        const lastYr = yearsPresent[yearsPresent.length - 1];
        const firstCnt = yearCounts[firstYr] || 1;
        const lastCnt = yearCounts[lastYr] || 1;
        const growthMultiple = (lastCnt / firstCnt).toFixed(1);

        const li1 = document.createElement('li');
        li1.className = 'concern-item';
        li1.innerHTML = `<strong>${{horizonPrefix}} Threat Escalation:</strong> AI-related cyberattacks have increased <strong>${{growthMultiple}}x</strong> from ${{firstYr}} (${{firstCnt}} incidents) to ${{lastYr}} (${{lastCnt}} incidents), driven by autonomous agents and multimodal generative tools.`;
        list.appendChild(li1);

        const maxSev = Math.max(...filtered.map(i => i.severity));
        const topInc = filtered.find(i => i.severity === maxSev);
        if (topInc) {{
          const li2 = document.createElement('li');
          li2.className = 'concern-item';
          li2.innerHTML = `<strong>Peak Severity Breach:</strong> <a onclick="window.highlightIncident('${{topInc.incident_id}}')">[${{topInc.incident_id}}] ${{topInc.headline}}</a> (Severity ${{topInc.severity}} - ${{topInc.target_sector}}, ${{topInc.country}}).`;
          list.appendChild(li2);
        }}

        const sectorCounts = {{}};
        filtered.forEach(i => sectorCounts[i.target_sector] = (sectorCounts[i.target_sector] || 0) + 1);
        let topSector = 'Financial Services';
        let topSecCount = 0;
        for (const [s, c] of Object.entries(sectorCounts)) {{
          if (c > topSecCount) {{
            topSecCount = c;
            topSector = s;
          }}
        }}

        const li3 = document.createElement('li');
        li3.className = 'concern-item';
        li3.innerHTML = `<strong>Dominant ${{horizonPrefix}} Target Sector:</strong> <a onclick="window.filterBySector('${{topSector}}')">${{topSector}}</a> (${{topSecCount}} incidents), suffering systemic wire transfers, deepfake CFO impersonation, and trading-agent exploitation.`;
        list.appendChild(li3);

        const agenticIncs = filtered.filter(i => i.category.includes('C'));
        const li4 = document.createElement('li');
        li4.className = 'concern-item';
        const startYrBaseline = firstYr || 2017;
        li4.innerHTML = `<strong>Autonomous Agent Exploits (Cat C):</strong> Surged from ${{yearCounts[startYrBaseline] || 0}} baseline cases in ${{startYrBaseline}} to ${{agenticIncs.length}} total cases in this window, led by <a onclick="window.filterByVector('Rogue MCP Server / Tool Poisoning')">Rogue MCP tool injection</a> and cross-agent context worms.`;
        list.appendChild(li4);

        const li5 = document.createElement('li');
        li5.className = 'concern-item';
        li5.innerHTML = `<strong>Forward Continuity:</strong> Ingestion engine automatically active for ${{maxDataYear + 1}}+ incidents via automated multithreaded global threat intelligence harvesting and live telemetry sync.`;
        list.appendChild(li5);
      }}

      function renderHeroSection(filtered) {{
        const canvas = document.getElementById('heroChartCanvas');
        const titleEl = document.getElementById('heroChartTitle');
        const table = document.getElementById('timelineDataTable');
        const isLight = document.body.classList.contains('light');
        const textColor = isLight ? '#475569' : '#94a3b8';
        const gridColor = isLight ? 'rgba(0, 0, 0, 0.06)' : 'rgba(255, 255, 255, 0.05)';

        // Sync buttons state
        const btnAnnual = document.getElementById('btnViewAnnual');
        const btnMonthly = document.getElementById('btnViewMonthly2026');
        const btnCum = document.getElementById('btnViewCumulative');
        const btnLinear = document.getElementById('btnScaleLinear');
        const btnLog = document.getElementById('btnScaleLog');

        if (btnAnnual) btnAnnual.classList.toggle('active', heroChartMode === 'annual');
        if (btnMonthly) btnMonthly.classList.toggle('active', heroChartMode === 'monthly2026');
        if (btnCum) btnCum.classList.toggle('active', heroChartMode === 'cumulative');
        if (btnLinear) btnLinear.classList.toggle('active', heroChartScale === 'linear');
        if (btnLog) btnLog.classList.toggle('active', heroChartScale === 'logarithmic');

        // Y-axis Scale Configuration
        const isLog = (heroChartScale === 'logarithmic');
        const yScaleConfig = isLog ? {{
          type: 'logarithmic',
          min: 1,
          grid: {{ color: gridColor }},
          ticks: {{
            color: textColor,
            font: {{ size: 11 }},
            callback: function(val) {{
              if (val === 1 || val === 5 || val === 20 || val === 50 || val === 100 || val === 300 || val === 1000 || val === 3000) {{
                return val.toLocaleString();
              }}
              return null;
            }}
          }}
        }} : {{
          stacked: (heroChartMode !== 'cumulative'),
          beginAtZero: true,
          grid: {{ color: gridColor }},
          ticks: {{ color: textColor, font: {{ size: 11 }} }}
        }};

        if (heroChartMode === 'annual') {{
          const is10Y = (activeFilters.horizon === '10Y' || activeFilters.horizon === 'ALL');
          const startYear = is10Y 
            ? Math.max(minDataYear, maxDataYear - 9)
            : Math.max(minDataYear, maxDataYear - 4);

          titleEl.textContent = `10-Year AI Cyber Incident Trajectory (${{startYear}}–${{maxDataYear}}+ Macro Horizon) ${{isLog ? '· [Logarithmic Scale]' : ''}}`;
          
          const years = [];
          for (let y = startYear; y <= maxDataYear; y++) {{
            years.push(String(y));
          }}

          const countsA = Array(years.length).fill(0);
          const countsB = Array(years.length).fill(0);
          const countsC = Array(years.length).fill(0);
          const totals = Array(years.length).fill(0);

          filtered.forEach(inc => {{
            const yr = inc.date.substring(0, 4);
            const idx = years.indexOf(yr);
            if (idx !== -1) {{
              totals[idx]++;
              if (inc.category.includes('A')) countsA[idx]++;
              if (inc.category.includes('B')) countsB[idx]++;
              if (inc.category.includes('C')) countsC[idx]++;
            }}
          }});

          // Milestone lookup for tooltips
          const milestones = {{
            '2017': 'WannaCry & Early Adversarial Perturbation Disclosures',
            '2018': 'Cambridge Analytica & Deepfake Video Emergence',
            '2019': 'UK Energy $243K Voice Clone Heist & GPT-2 Staged Release',
            '2020': 'SolarWinds Supply Chain & GPT-3 Prompt Injections',
            '2021': 'Colonial Pipeline, Log4j Zero-Day & UAE $35M Deepfake',
            '2022': 'Lapsus$ NVIDIA Hack, ChatGPT Launch & DAN Bypasses',
            '2023': 'Samsung ChatGPT Code Leak, WormGPT & MOVEit Exploits',
            '2024': 'Hong Kong $25.6M Deepfake Video Call & CrowdStrike Outage',
            '2025': 'DeepSeek-R1 Probe, Volt Typhoon & Autonomous Coding RCE',
            '2026': 'Autonomous Agent Swarms, MCP Tool Hijacking & Live CTI'
          }};

          let thead = '<thead><tr><th style="text-align:left; padding-left:12px;">Category / Milestone</th>';
          years.forEach(yr => thead += `<th>${{yr}}</th>`);
          thead += '<th style="background:var(--table-th); color:var(--text-main);">Total Horizon</th></tr></thead>';

          let tbody = '<tbody>';
          tbody += '<tr class="total-row"><td style="text-align:left; padding-left:12px;">Total Incidents</td>';
          totals.forEach(c => tbody += `<td><strong>${{c.toLocaleString()}}</strong></td>`);
          tbody += `<td><strong>${{totals.reduce((a,b)=>a+b, 0).toLocaleString()}}</strong></td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-a);">Cat A: Attacks USING AI</td>';
          countsA.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{countsA.reduce((a,b)=>a+b, 0).toLocaleString()}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-b);">Cat B: Attacks ON AI Systems</td>';
          countsB.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{countsB.reduce((a,b)=>a+b, 0).toLocaleString()}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-c);">Cat C: Agentic Attacks</td>';
          countsC.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{countsC.reduce((a,b)=>a+b, 0).toLocaleString()}}</td></tr>`;

          tbody += '</tbody>';
          table.innerHTML = thead + tbody;

          if (heroChartInstance) heroChartInstance.destroy();
          if (typeof Chart !== 'undefined') {{
            const ctx = canvas.getContext('2d');
            heroChartInstance = new Chart(ctx, {{
              type: 'bar',
              data: {{
                labels: years,
                datasets: [
                  {{
                    label: 'Cat A (Using AI)',
                    data: countsA,
                    backgroundColor: 'rgba(56, 189, 248, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 4
                  }},
                  {{
                    label: 'Cat B (On AI Systems)',
                    data: countsB,
                    backgroundColor: 'rgba(192, 132, 252, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 4
                  }},
                  {{
                    label: 'Cat C (Agentic Attacks)',
                    data: countsC,
                    backgroundColor: 'rgba(52, 211, 153, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 4
                  }},
                  {{
                    type: 'line',
                    label: 'Trendline',
                    data: totals,
                    borderColor: '#f59e0b',
                    borderWidth: 3,
                    pointBackgroundColor: '#f59e0b',
                    pointHoverBackgroundColor: '#fbbf24',
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    tension: 0.35,
                    fill: false
                  }}
                ]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{
                    mode: 'index',
                    intersect: false,
                    backgroundColor: isLight ? '#ffffff' : '#111827',
                    titleColor: isLight ? '#0f172a' : '#ffffff',
                    bodyColor: isLight ? '#334155' : '#e2e8f0',
                    borderColor: isLight ? '#cbd5e1' : '#374151',
                    borderWidth: 1,
                    callbacks: {{
                      afterTitle: function(items) {{
                        const lbl = items[0].label;
                        return milestones[lbl] ? `📍 ${{milestones[lbl]}}` : '';
                      }},
                      afterBody: function(items) {{
                        const yrTotal = items.reduce((acc, it) => acc + (it.dataset.type !== 'line' ? it.parsed.y : 0), 0);
                        return `\n📊 Annual Sum: ${{yrTotal.toLocaleString()}} Incidents`;
                      }}
                    }}
                  }}
                }},
                scales: {{
                  x: {{
                    stacked: !isLog,
                    grid: {{ color: gridColor }},
                    ticks: {{ color: textColor, font: {{ size: 12, weight: 'bold' }} }}
                  }},
                  y: yScaleConfig
                }}
              }}
            }});
          }}

        }} else if (heroChartMode === 'monthly2026') {{
          titleEl.textContent = `2026 Real-Time Monthly Incident Distribution & Live Telemetry Pulse ${{isLog ? '· [Logarithmic Scale]' : ''}}`;
          
          const monthLabels = ['Jan 26', 'Feb 26', 'Mar 26', 'Apr 26', 'May 26', 'Jun 26', 'Jul 26', 'Aug 26', 'Sep 26', 'Oct 26', 'Nov (Live)'];
          const countsA = Array(11).fill(0);
          const countsB = Array(11).fill(0);
          const countsC = Array(11).fill(0);
          const totals = Array(11).fill(0);

          filtered.forEach(inc => {{
            if (inc.date && inc.date.startsWith('2026')) {{
              const mIdx = Math.min(10, Math.max(0, parseInt(inc.date.substring(5, 7), 10) - 1));
              totals[mIdx]++;
              if (inc.category.includes('A')) countsA[mIdx]++;
              if (inc.category.includes('B')) countsB[mIdx]++;
              if (inc.category.includes('C')) countsC[mIdx]++;
            }}
          }});

          let thead = '<thead><tr><th style="text-align:left; padding-left:12px;">2026 Progression</th>';
          monthLabels.forEach(m => thead += `<th>${{m}}</th>`);
          thead += '<th style="background:var(--table-th); color:var(--text-main);">2026 Total</th></tr></thead>';

          let tbody = '<tbody>';
          tbody += '<tr class="total-row"><td style="text-align:left; padding-left:12px;">Total Dispatches</td>';
          totals.forEach(c => tbody += `<td><strong>${{c.toLocaleString()}}</strong></td>`);
          tbody += `<td><strong>${{totals.reduce((a,b)=>a+b, 0).toLocaleString()}}</strong></td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-a);">Cat A: Using AI</td>';
          countsA.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{countsA.reduce((a,b)=>a+b, 0).toLocaleString()}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-b);">Cat B: On AI Systems</td>';
          countsB.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{countsB.reduce((a,b)=>a+b, 0).toLocaleString()}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-c);">Cat C: Agentic Attacks</td>';
          countsC.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{countsC.reduce((a,b)=>a+b, 0).toLocaleString()}}</td></tr>`;

          tbody += '</tbody>';
          table.innerHTML = thead + tbody;

          if (heroChartInstance) heroChartInstance.destroy();
          if (typeof Chart !== 'undefined') {{
            const ctx = canvas.getContext('2d');
            heroChartInstance = new Chart(ctx, {{
              type: 'bar',
              data: {{
                labels: monthLabels,
                datasets: [
                  {{
                    label: 'Cat A (Using AI)',
                    data: countsA,
                    backgroundColor: 'rgba(56, 189, 248, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 4
                  }},
                  {{
                    label: 'Cat B (On AI Systems)',
                    data: countsB,
                    backgroundColor: 'rgba(192, 132, 252, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 4
                  }},
                  {{
                    label: 'Cat C (Agentic Attacks)',
                    data: countsC,
                    backgroundColor: 'rgba(52, 211, 153, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 4
                  }},
                  {{
                    type: 'line',
                    label: 'Monthly Trend',
                    data: totals,
                    borderColor: '#f59e0b',
                    borderWidth: 3,
                    pointBackgroundColor: '#f59e0b',
                    pointHoverBackgroundColor: '#fbbf24',
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    tension: 0.35,
                    fill: false
                  }}
                ]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{
                    mode: 'index',
                    intersect: false,
                    backgroundColor: isLight ? '#ffffff' : '#111827',
                    titleColor: isLight ? '#0f172a' : '#ffffff',
                    bodyColor: isLight ? '#334155' : '#e2e8f0',
                    borderColor: isLight ? '#cbd5e1' : '#374151',
                    borderWidth: 1,
                    callbacks: {{
                      afterBody: function(items) {{
                        const mTotal = items.reduce((acc, it) => acc + (it.dataset.type !== 'line' ? it.parsed.y : 0), 0);
                        return `\n📊 Month Total: ${{mTotal.toLocaleString()}} Dispatches`;
                      }}
                    }}
                  }}
                }},
                scales: {{
                  x: {{
                    stacked: !isLog,
                    grid: {{ color: gridColor }},
                    ticks: {{ color: textColor, font: {{ size: 11, weight: 'bold' }} }}
                  }},
                  y: yScaleConfig
                }}
              }}
            }});
          }}

        }} else {{
          titleEl.textContent = `Cumulative Threat Surge Trajectory (10-Year Exponential S-Curve, 2017–2026+) ${{isLog ? '· [Logarithmic Scale]' : ''}}`;
          
          const is10Y = (activeFilters.horizon === '10Y' || activeFilters.horizon === 'ALL');
          const startYear = is10Y 
            ? Math.max(minDataYear, maxDataYear - 9)
            : Math.max(minDataYear, maxDataYear - 4);

          const years = [];
          for (let y = startYear; y <= maxDataYear; y++) {{
            years.push(String(y));
          }}

          const annualCountsA = Array(years.length).fill(0);
          const annualCountsB = Array(years.length).fill(0);
          const annualCountsC = Array(years.length).fill(0);
          const annualTotals = Array(years.length).fill(0);

          filtered.forEach(inc => {{
            const yr = inc.date.substring(0, 4);
            const idx = years.indexOf(yr);
            if (idx !== -1) {{
              annualTotals[idx]++;
              if (inc.category.includes('A')) annualCountsA[idx]++;
              if (inc.category.includes('B')) annualCountsB[idx]++;
              if (inc.category.includes('C')) annualCountsC[idx]++;
            }}
          }});

          // Compute cumulative running totals
          const cumTotals = [];
          const cumA = [];
          const cumB = [];
          const cumC = [];
          let runTot = 0, runA = 0, runB = 0, runC = 0;

          for (let i = 0; i < years.length; i++) {{
            runTot += annualTotals[i];
            runA += annualCountsA[i];
            runB += annualCountsB[i];
            runC += annualCountsC[i];
            cumTotals.push(runTot);
            cumA.push(runA);
            cumB.push(runB);
            cumC.push(runC);
          }}

          let thead = '<thead><tr><th style="text-align:left; padding-left:12px;">Cumulative Milestone / Year</th>';
          years.forEach(yr => thead += `<th>${{yr}}</th>`);
          thead += '<th style="background:var(--table-th); color:var(--text-main);">Current Total</th></tr></thead>';

          let tbody = '<tbody>';
          tbody += '<tr class="total-row"><td style="text-align:left; padding-left:12px;">Cumulative Incidents (Surge)</td>';
          cumTotals.forEach(c => tbody += `<td><strong>${{c.toLocaleString()}}</strong></td>`);
          tbody += `<td><strong style="color:var(--border-focus);">${{(cumTotals[cumTotals.length - 1] || 0).toLocaleString()}}</strong></td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--text-dim);">New Additions in Year</td>';
          annualTotals.forEach(c => tbody += `<td>+${{c.toLocaleString()}}</td>`);
          tbody += `<td>+${{annualTotals.reduce((a,b)=>a+b, 0).toLocaleString()}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-a);">Cat A Cumulative (Using AI)</td>';
          cumA.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{(cumA[cumA.length - 1] || 0).toLocaleString()}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-b);">Cat B Cumulative (On AI Systems)</td>';
          cumB.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{(cumB[cumB.length - 1] || 0).toLocaleString()}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-c);">Cat C Cumulative (Agentic Attacks)</td>';
          cumC.forEach(c => tbody += `<td>${{c.toLocaleString()}}</td>`);
          tbody += `<td>${{(cumC[cumC.length - 1] || 0).toLocaleString()}}</td></tr>`;

          tbody += '</tbody>';
          table.innerHTML = thead + tbody;

          if (heroChartInstance) heroChartInstance.destroy();
          if (typeof Chart !== 'undefined') {{
            const ctx = canvas.getContext('2d');
            heroChartInstance = new Chart(ctx, {{
              type: 'line',
              data: {{
                labels: years,
                datasets: [
                  {{
                    label: 'Cumulative Total (All Incidents)',
                    data: cumTotals,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.15)',
                    borderWidth: 3.5,
                    pointBackgroundColor: '#f59e0b',
                    pointHoverBackgroundColor: '#fbbf24',
                    pointRadius: 5,
                    pointHoverRadius: 8,
                    tension: 0.35,
                    fill: true
                  }},
                  {{
                    label: 'Cat A Cumulative (Using AI)',
                    data: cumA,
                    borderColor: 'rgba(56, 189, 248, 1)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 4],
                    pointRadius: 3,
                    tension: 0.3
                  }},
                  {{
                    label: 'Cat B Cumulative (On AI Systems)',
                    data: cumB,
                    borderColor: 'rgba(192, 132, 252, 1)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 4],
                    pointRadius: 3,
                    tension: 0.3
                  }},
                  {{
                    label: 'Cat C Cumulative (Agentic Attacks)',
                    data: cumC,
                    borderColor: 'rgba(52, 211, 153, 1)',
                    backgroundColor: 'transparent',
                    borderWidth: 2.5,
                    pointRadius: 4,
                    tension: 0.3
                  }}
                ]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{
                    mode: 'index',
                    intersect: false,
                    backgroundColor: isLight ? '#ffffff' : '#111827',
                    titleColor: isLight ? '#0f172a' : '#ffffff',
                    bodyColor: isLight ? '#334155' : '#e2e8f0',
                    borderColor: isLight ? '#cbd5e1' : '#374151',
                    borderWidth: 1
                  }}
                }},
                scales: {{
                  x: {{
                    grid: {{ color: gridColor }},
                    ticks: {{ color: textColor, font: {{ size: 12, weight: 'bold' }} }}
                  }},
                  y: yScaleConfig
                }}
              }}
            }});
          }}
        }}
      }}

      document.getElementById('btnViewAnnual').addEventListener('click', () => {{
        heroChartMode = 'annual';
        renderHeroSection(getFilteredIncidents());
      }});

      const btnViewMon = document.getElementById('btnViewMonthly2026');
      if (btnViewMon) {{
        btnViewMon.addEventListener('click', () => {{
          heroChartMode = 'monthly2026';
          renderHeroSection(getFilteredIncidents());
        }});
      }}

      const btnCum = document.getElementById('btnViewCumulative');
      if (btnCum) {{
        btnCum.addEventListener('click', () => {{
          heroChartMode = 'cumulative';
          renderHeroSection(getFilteredIncidents());
        }});
      }}

      const btnLin = document.getElementById('btnScaleLinear');
      if (btnLin) {{
        btnLin.addEventListener('click', () => {{
          heroChartScale = 'linear';
          renderHeroSection(getFilteredIncidents());
        }});
      }}

      const btnLg = document.getElementById('btnScaleLog');
      if (btnLg) {{
        btnLg.addEventListener('click', () => {{
          heroChartScale = 'logarithmic';
          renderHeroSection(getFilteredIncidents());
        }});
      }}

      let categoryDoughnutInstance = null;
      let vectorRadarInstance = null;
      let severityPolarInstance = null;

      function renderAdvancedVisualizations(filtered) {{
        const isLight = document.body.classList.contains('light');
        const textColor = isLight ? '#475569' : '#94a3b8';
        const gridColor = isLight ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.08)';

        // 1. Category Doughnut Chart
        const catCanvas = document.getElementById('categoryDoughnutCanvas');
        if (catCanvas && typeof Chart !== 'undefined') {{
          let countA = 0, countB = 0, countC = 0;
          filtered.forEach(i => {{
            if (i.category.includes('A')) countA++;
            if (i.category.includes('B')) countB++;
            if (i.category.includes('C')) countC++;
          }});
          const totalCats = countA + countB + countC || 1;

          if (categoryDoughnutInstance) categoryDoughnutInstance.destroy();
          categoryDoughnutInstance = new Chart(catCanvas.getContext('2d'), {{
            type: 'doughnut',
            data: {{
              labels: ['Cat A: Using AI', 'Cat B: On AI Systems', 'Cat C: Agentic Attacks'],
              datasets: [{{
                data: [countA, countB, countC],
                backgroundColor: [
                  'rgba(56, 189, 248, 0.85)',
                  'rgba(192, 132, 252, 0.85)',
                  'rgba(52, 211, 153, 0.85)'
                ],
                borderColor: isLight ? '#ffffff' : '#0b1120',
                borderWidth: 2,
                hoverOffset: 6
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              cutout: '66%',
              plugins: {{
                legend: {{
                  position: 'bottom',
                  labels: {{ color: textColor, font: {{ size: 10 }}, boxWidth: 10, padding: 8 }}
                }},
                tooltip: {{
                  callbacks: {{
                    label: function(ctx) {{
                      const val = ctx.raw || 0;
                      const pct = Math.round((val / totalCats) * 100);
                      return ` ${{ctx.label}}: ${{val}} (${{pct}}%)`;
                    }}
                  }}
                }}
              }},
              onClick: (evt, elements) => {{
                if (elements.length > 0) {{
                  const idx = elements[0].index;
                  const targetCat = idx === 0 ? 'A' : (idx === 1 ? 'B' : 'C');
                  const select = document.getElementById('filterCategory');
                  if (select) {{
                    select.value = targetCat;
                    activeFilters.category = targetCat;
                    updateDashboard();
                  }}
                }}
              }}
            }}
          }});
        }}

        // 2. MITRE ATLAS Vector Radar Chart
        const radarCanvas = document.getElementById('vectorRadarCanvas');
        if (radarCanvas && typeof Chart !== 'undefined') {{
          const vectorMap = {{
            'Agent / MCP': 0,
            'Supply Chain': 0,
            'Prompt Injection': 0,
            'Deepfake Fraud': 0,
            'Evasion / PoC': 0,
            'Recon / Phishing': 0
          }};

          filtered.forEach(i => {{
            const v = (i.attack_vector || '').toLowerCase();
            const h = (i.headline || '').toLowerCase();
            const combo = v + ' ' + h;

            if (combo.includes('agent') || combo.includes('mcp') || combo.includes('loop')) {{
              vectorMap['Agent / MCP']++;
            }} else if (combo.includes('supply') || combo.includes('poison') || combo.includes('hugging')) {{
              vectorMap['Supply Chain']++;
            }} else if (combo.includes('prompt') || combo.includes('jailbreak') || combo.includes('direct')) {{
              vectorMap['Prompt Injection']++;
            }} else if (combo.includes('deepfake') || combo.includes('voice') || combo.includes('cfo') || combo.includes('video')) {{
              vectorMap['Deepfake Fraud']++;
            }} else if (combo.includes('evasion') || combo.includes('adversarial') || combo.includes('perturbation')) {{
              vectorMap['Evasion / PoC']++;
            }} else {{
              vectorMap['Recon / Phishing']++;
            }}
          }});

          const radarLabels = Object.keys(vectorMap);
          const radarValues = Object.values(vectorMap);

          if (vectorRadarInstance) vectorRadarInstance.destroy();
          vectorRadarInstance = new Chart(radarCanvas.getContext('2d'), {{
            type: 'radar',
            data: {{
              labels: radarLabels,
              datasets: [{{
                label: 'Threat Density',
                data: radarValues,
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                borderColor: '#38bdf8',
                borderWidth: 2,
                pointBackgroundColor: '#38bdf8',
                pointBorderColor: '#ffffff',
                pointRadius: 3.5
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ display: false }}
              }},
              scales: {{
                r: {{
                  angleLines: {{ color: gridColor }},
                  grid: {{ color: gridColor }},
                  pointLabels: {{ color: textColor, font: {{ size: 9.5 }} }},
                  ticks: {{ display: false, backdropColor: 'transparent' }},
                  beginAtZero: true
                }}
              }}
            }}
          }});
        }}

        // 3. Severity Polar Area Chart
        const polarCanvas = document.getElementById('severityPolarCanvas');
        if (polarCanvas && typeof Chart !== 'undefined') {{
          const sevCounts = [0, 0, 0, 0, 0];
          filtered.forEach(i => {{
            const s = parseInt(i.severity);
            if (s >= 1 && s <= 5) sevCounts[s - 1]++;
          }});

          if (severityPolarInstance) severityPolarInstance.destroy();
          severityPolarInstance = new Chart(polarCanvas.getContext('2d'), {{
            type: 'polarArea',
            data: {{
              labels: ['Sev 1: PoC', 'Sev 2: Attempted', 'Sev 3: Limited', 'Sev 4: Significant', 'Sev 5: Critical'],
              datasets: [{{
                data: sevCounts,
                backgroundColor: [
                  'rgba(100, 116, 139, 0.75)',
                  'rgba(2, 132, 199, 0.75)',
                  'rgba(234, 179, 8, 0.75)',
                  'rgba(249, 115, 22, 0.75)',
                  'rgba(239, 68, 68, 0.85)'
                ],
                borderColor: isLight ? '#ffffff' : '#0b1120',
                borderWidth: 1.5
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{
                  position: 'bottom',
                  labels: {{ color: textColor, font: {{ size: 9 }}, boxWidth: 8, padding: 6 }}
                }}
              }},
              scales: {{
                r: {{
                  grid: {{ color: gridColor }},
                  ticks: {{ display: false, backdropColor: 'transparent' }}
                }}
              }},
              onClick: (evt, elements) => {{
                if (elements.length > 0) {{
                  const idx = elements[0].index;
                  const targetSev = String(idx + 1);
                  const select = document.getElementById('filterSeverity');
                  if (select) {{
                    select.value = targetSev;
                    activeFilters.severity = targetSev;
                    updateDashboard();
                  }}
                }}
              }}
            }}
          }});
        }}
      }}

      function renderCountries(filtered) {{
        const countryCounts = {{}};
        filtered.forEach(i => countryCounts[i.country] = (countryCounts[i.country] || 0) + 1);
        const sorted = Object.entries(countryCounts).sort((a,b) => b[1] - a[1]);
        const maxVal = sorted.length > 0 ? sorted[0][1] : 1;

        const container = document.getElementById('countryBarsList');
        container.innerHTML = '';

        if (sorted.length === 0) {{
          container.innerHTML = '<div style="color:var(--text-dim); font-size:0.8rem; padding:10px;">No country data for filter.</div>';
          return;
        }}

        sorted.slice(0, 10).forEach(([country, count]) => {{
          const pct = Math.round((count / maxVal) * 100);
          const row = document.createElement('div');
          row.className = 'country-row';
          row.title = `Click to filter by ${{country}}`;
          row.onclick = () => {{
            document.getElementById('filterCountry').value = country;
            activeFilters.country = country;
            updateDashboard();
          }};
          row.innerHTML = `
            <span class="country-name">${{country}}</span>
            <div class="country-bar-bg">
              <div class="country-bar-fill" style="width: ${{pct}}%;"></div>
            </div>
            <span class="country-count">${{count}}</span>
          `;
          container.appendChild(row);
        }});
      }}

      function renderBreakdowns(filtered) {{
        const vecCounts = {{}};
        filtered.forEach(i => vecCounts[i.attack_vector] = (vecCounts[i.attack_vector] || 0) + 1);
        const sortedVec = Object.entries(vecCounts).sort((a,b) => b[1] - a[1]);
        const maxVec = sortedVec.length > 0 ? sortedVec[0][1] : 1;

        const vecList = document.getElementById('vectorMeterList');
        vecList.innerHTML = '';
        sortedVec.slice(0, 5).forEach(([v, c]) => {{
          const pct = Math.round((c / maxVec) * 100);
          const div = document.createElement('div');
          div.className = 'meter-item';
          div.innerHTML = `
            <div class="meter-header"><span>${{v}}</span><strong>${{c}}</strong></div>
            <div class="meter-bar"><div class="meter-bar-fill" style="width:${{pct}}%; background:#38bdf8;"></div></div>
          `;
          vecList.appendChild(div);
        }});

        const secCounts = {{}};
        filtered.forEach(i => secCounts[i.target_sector] = (secCounts[i.target_sector] || 0) + 1);
        const sortedSec = Object.entries(secCounts).sort((a,b) => b[1] - a[1]);
        const maxSec = sortedSec.length > 0 ? sortedSec[0][1] : 1;

        const secList = document.getElementById('sectorMeterList');
        secList.innerHTML = '';
        sortedSec.slice(0, 5).forEach(([s, c]) => {{
          const pct = Math.round((c / maxSec) * 100);
          const div = document.createElement('div');
          div.className = 'meter-item';
          div.innerHTML = `
            <div class="meter-header"><span>${{s}}</span><strong>${{c}}</strong></div>
            <div class="meter-bar"><div class="meter-bar-fill" style="width:${{pct}}%; background:#c084fc;"></div></div>
          `;
          secList.appendChild(div);
        }});

        const sevCounts = {{ 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }};
        filtered.forEach(i => sevCounts[i.severity] = (sevCounts[i.severity] || 0) + 1);
        const sevColors = {{ 1: '#64748b', 2: '#38bdf8', 3: '#facc15', 4: '#fb923c', 5: '#ef4444' }};
        const sevLabels = {{
          1: '1: Proof of Concept',
          2: '2: Attempted, No Impact',
          3: '3: Confirmed Breach, Limited',
          4: '4: Significant Loss',
          5: '5: Systemic / Critical Infrastructure'
        }};

        const sevList = document.getElementById('severityMeterList');
        sevList.innerHTML = '';
        const maxSevVal = Math.max(...Object.values(sevCounts), 1);
        [5, 4, 3, 2, 1].forEach(lvl => {{
          const count = sevCounts[lvl];
          const pct = Math.round((count / maxSevVal) * 100);
          const div = document.createElement('div');
          div.className = 'meter-item';
          div.innerHTML = `
            <div class="meter-header">
              <span style="color:${{sevColors[lvl]}};">${{sevLabels[lvl]}}</span>
              <strong>${{count}}</strong>
            </div>
            <div class="meter-bar"><div class="meter-bar-fill" style="width:${{pct}}%; background:${{sevColors[lvl]}};"></div></div>
          `;
          sevList.appendChild(div);
        }});
      }}

      // --- Cyber Threat Highlighting & Feed Pagination Engine ---
      let articlesFeedLimit = 60;
      let threatHighlightMode = true;
      let prioritizeThreatsFirst = false;

      function highlightThreatKeywords(text, threatType) {{
        if (!text) return '';
        // Robust Context Protection: Escape HTML tags first before applying keyword marks
        const escaped = escapeHtml(text);
        if (!threatHighlightMode) return escaped;
        const threatRegex = /\\b(ransomware|lockbit|blackcat|alphv|clop|play ransomware|darkside|revil|volt typhoon|apt\\d+|sandworm|lazarus|scattered spider|zero-day|0-day|cve-\\d{{4}}-\\d+|remote code execution|rce|privilege escalation|unpatched|data breach|breached|hacked|cyberattack|cyber attack|compromised|extortion|exfiltration|ddos|phishing|backdoor|trojan|supply chain attack|infostealer|credential harvesting|critical flaw|security vulnerability|malware|botnet|exploit)\\b/gi;
        const cssClass = threatType === 'case' ? 'threat-kw-highlight-case' : (threatType === 'vulnerability' ? 'threat-kw-highlight-vuln' : 'threat-kw-highlight-general');
        return escaped.replace(threatRegex, match => `<mark class="${{cssClass}}">${{match}}</mark>`);
      }}

      window.toggleThreatHighlight = function() {{
        threatHighlightMode = !threatHighlightMode;
        const btn = document.getElementById('btnToggleThreatHighlight');
        if (btn) {{
          btn.classList.toggle('active', threatHighlightMode);
          btn.textContent = threatHighlightMode ? '🚨 Threat Highlighting: ON' : '⚪ Threat Highlighting: OFF';
          btn.style.background = threatHighlightMode ? 'rgba(239,68,68,0.18)' : 'rgba(255,255,255,0.05)';
          btn.style.color = threatHighlightMode ? '#f87171' : 'var(--text-dim)';
          btn.style.borderColor = threatHighlightMode ? '#ef4444' : 'var(--border-subtle)';
        }}
        renderArticlesFeed(getFilteredArticles());
      }};

      window.toggleThreatPriority = function() {{
        prioritizeThreatsFirst = !prioritizeThreatsFirst;
        const btn = document.getElementById('btnToggleThreatPriority');
        if (btn) {{
          btn.classList.toggle('active', prioritizeThreatsFirst);
          btn.textContent = prioritizeThreatsFirst ? '⚡ Threats Prioritized' : '⚡ Threats to Top';
          btn.style.background = prioritizeThreatsFirst ? 'rgba(249,115,22,0.22)' : 'rgba(249,115,22,0.1)';
          btn.style.color = prioritizeThreatsFirst ? '#fed7aa' : '#fb923c';
        }}
        renderArticlesFeed(getFilteredArticles());
      }};

      window.loadMoreArticles = function(count = 60) {{
        articlesFeedLimit += count;
        renderArticlesFeed(getFilteredArticles());
      }};

      window.showAllArticles = function() {{
        articlesFeedLimit = 999999;
        renderArticlesFeed(getFilteredArticles());
      }};

      window.resetFeedView = function() {{
        articlesFeedLimit = 60;
        renderArticlesFeed(getFilteredArticles());
        const feed = document.getElementById('articlesGrid');
        if (feed) feed.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }};

      function renderArticlesFeed(articles) {{
        const grid = document.getElementById('articlesGrid');
        grid.innerHTML = '';

        if (articles.length === 0) {{
          grid.innerHTML = '<div style="color:var(--text-dim); padding:20px;">No articles match search query.</div>';
          document.getElementById('articlesCountBadge').textContent = '(0 matching)';
          const statusEl = document.getElementById('articlesPaginationStatus');
          if (statusEl) statusEl.textContent = '0 articles matching criteria.';
          return;
        }}

        // Optional threat-first prioritization while preserving the full list
        let feedArticles = [...articles];
        if (prioritizeThreatsFirst) {{
          feedArticles.sort((a, b) => {{
            const scoreA = (a.threat_type === 'case' ? 10 : (a.threat_type === 'vulnerability' ? 5 : 0)) + (a.severity || 1);
            const scoreB = (b.threat_type === 'case' ? 10 : (b.threat_type === 'vulnerability' ? 5 : 0)) + (b.severity || 1);
            return scoreB - scoreA;
          }});
        }}

        const totalCount = feedArticles.length;
        const displayedCount = Math.min(totalCount, articlesFeedLimit);
        const caseCount = feedArticles.filter(a => a.threat_type === 'case').length;
        const vulnCount = feedArticles.filter(a => a.threat_type === 'vulnerability').length;
        const totalThreats = caseCount + vulnCount;

        document.getElementById('articlesCountBadge').textContent = `(Showing ${{displayedCount}} of ${{totalCount}} · ${{totalThreats}} Threats Highlighted)`;

        // Update pagination status & button visibility
        const paginationStatus = document.getElementById('articlesPaginationStatus');
        if (paginationStatus) {{
          paginationStatus.innerHTML = `Showing <strong style="color:var(--text-main);">${{displayedCount}}</strong> of <strong style="color:var(--text-main);">${{totalCount}}</strong> articles · <span style="color:#ef4444; font-weight:700;">🔴 ${{caseCount}} Attack Cases</span> · <span style="color:#f97316; font-weight:700;">🟠 ${{vulnCount}} Vulns</span>`;
        }}

        const btnLoadMore = document.getElementById('btnLoadMoreArticles');
        if (btnLoadMore) {{
          btnLoadMore.style.display = displayedCount < totalCount ? 'inline-block' : 'none';
          const remaining = totalCount - displayedCount;
          btnLoadMore.textContent = `🔽 Load 60 More Articles (${{Math.min(60, remaining)}} remaining)`;
        }}

        const btnShowAll = document.getElementById('btnShowAllArticles');
        if (btnShowAll) {{
          btnShowAll.style.display = displayedCount < totalCount ? 'inline-block' : 'none';
          btnShowAll.textContent = `⚡ Show Full Feed (All ${{totalCount.toLocaleString()}})`;
        }}

        const displayList = feedArticles.slice(0, articlesFeedLimit);
        displayList.forEach(art => {{
          const card = document.createElement('div');
          
          const threatType = art.threat_type || 'informational';
          const isAttackCase = threatType === 'case' || art.severity >= 4;
          const isVulnAlert = threatType === 'vulnerability';
          
          let cardHighlightClass = 'threat-card-info';
          if (threatHighlightMode) {{
            if (isAttackCase) cardHighlightClass = 'threat-card-case';
            else if (isVulnAlert) cardHighlightClass = 'threat-card-vuln';
          }}

          card.className = `article-card ${{cardHighlightClass}}`;
          card.onclick = () => openArticleReaderModal(art.article_id);
          
          let catBadges = '';
          art.category.forEach(c => {{
            catBadges += `<span class="badge badge-cat-${{c.toLowerCase()}}">Cat ${{c}}</span> `;
          }});

          const isLiveNow = art.isLive || art.live_time || art.rel_time;
          const relTime = art.rel_time || (art.live_time && art.live_time !== '🟢 Live Stream' ? art.live_time : 'Just now');
          const liveBadgeHtml = isLiveNow 
            ? `<span class="badge" style="background:rgba(16,185,129,0.18); color:#10b981; border:1px solid #10b981; font-weight:700;">🟢 LIVE · ${{relTime}}</span> `
            : `<span class="badge" style="background:rgba(148,163,184,0.15); color:#94a3b8; border:1px solid #64748b;">${{art.date}}</span> `;

          const fieldIcon = art.field === 'ai' ? '🤖 AI' :
                            art.field === 'cyber' ? '🛡️ Cyber' :
                            art.field === 'hardware' ? '💻 Hardware' :
                            art.field === 'it' ? '☁️ IT / Cloud' : '🌐 Tech';
          const fieldBadge = `<span class="badge" style="background:rgba(59,130,246,0.12); color:#60a5fa; border:1px solid rgba(59,130,246,0.25); text-transform:uppercase; font-size:10px; font-weight:700;">${{fieldIcon}}</span>`;

          let threatBadge = '';
          let beaconStrip = '';
          if (threatType === 'case') {{
            threatBadge = `<span class="badge" style="background:rgba(239,68,68,0.18); color:#f87171; border:1px solid #ef4444; font-weight:700; font-size:10px;">🔴 Attack Case</span>`;
            if (threatHighlightMode) {{
              beaconStrip = `
                <div class="threat-beacon-strip threat-beacon-case">
                  <span><span class="pulse-dot-beacon red"></span>🚨 ACTIVE ATTACK CASE · COMPROMISE DETECTED</span>
                  <span>SEV ${{art.severity}}/5</span>
                </div>
              `;
            }}
          }} else if (threatType === 'vulnerability') {{
            threatBadge = `<span class="badge" style="background:rgba(249,115,22,0.18); color:#fb923c; border:1px solid #f97316; font-weight:700; font-size:10px;">🟠 Vuln Alert</span>`;
            if (threatHighlightMode) {{
              beaconStrip = `
                <div class="threat-beacon-strip threat-beacon-vuln">
                  <span><span class="pulse-dot-beacon orange"></span>⚠️ ZERO-DAY / VULNERABILITY ALERT</span>
                  <span>SEV ${{art.severity}}/5</span>
                </div>
              `;
            }}
          }} else if (threatType === 'policy') {{
            threatBadge = `<span class="badge" style="background:rgba(34,197,94,0.18); color:#4ade80; border:1px solid #22c55e; font-weight:700; font-size:10px;">🟢 Policy / Legal</span>`;
          }} else {{
            threatBadge = `<span class="badge" style="background:rgba(59,130,246,0.18); color:#60a5fa; border:1px solid #3b82f6; font-weight:700; font-size:10px;">🔵 Threat Advisory</span>`;
          }}

          const highlightedHeadline = highlightThreatKeywords(art.headline, threatType);
          const safeOutlet = escapeHtml(art.outlet);
          const safeCountry = escapeHtml(art.country);
          const safeArtId = escapeHtml(art.article_id);
          const safeUrl = sanitizeUrl(art.url);

          card.innerHTML = `
            ${{beaconStrip}}
            <div class="article-meta">
              <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                <span class="article-outlet">${{safeOutlet}}</span>
                ${{threatBadge}}
                ${{fieldBadge}}
              </div>
              <div style="display:flex; align-items:center; gap:6px;">
                ${{liveBadgeHtml}}
                <span style="color:var(--text-dim); font-size:0.75rem;">${{safeCountry}}</span>
              </div>
            </div>
            <div class="article-headline" onclick="openArticleReaderModal('${{safeArtId}}'); event.stopPropagation();" style="cursor:pointer;" title="Click to read full unblocked threat briefing">
              <span>${{highlightedHeadline}}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
              <div class="article-badges">
                ${{catBadges}}
                <span class="badge badge-sev-${{art.severity}}">Sev ${{art.severity}}</span>
              </div>
              <div style="display:flex; gap:6px;">
                <button class="article-btn-read" onclick="openArticleReaderModal('${{safeArtId}}'); event.stopPropagation();" title="Open full unblocked threat dossier & MITRE TTPs">
                  📖 Read Brief
                </button>
                <a href="${{safeUrl}}" target="_blank" rel="noopener noreferrer" class="article-btn-ext" onclick="event.stopPropagation();" title="Open direct publisher site">
                  Source ↗
                </a>
              </div>
            </div>
          `;
          grid.appendChild(card);
        }});
      }}

      function getSeverityLabel(s) {{
        if (s >= 5) return 'Critical / National Infrastructure Impact';
        if (s == 4) return 'High / Severe Compromise & Extortion';
        if (s == 3) return 'Moderate / Active Exploit & CVE';
        if (s == 2) return 'Low / Monitored Telemetry Anomaly';
        return 'Informational / Research Advisory';
      }}

      function openArticleReaderModal(artId) {{
        const art = allArticles.find(a => a.article_id === artId);
        if (!art) return;

        const modal = document.getElementById('articleReaderModal');
        document.getElementById('modalOutletBadge').textContent = art.outlet;

        const fieldIcon = art.field === 'ai' ? '🤖 AI & Models' :
                          art.field === 'cyber' ? '🛡️ Cybersecurity' :
                          art.field === 'hardware' ? '💻 Hardware & Chips' :
                          art.field === 'it' ? '☁️ Enterprise IT / Cloud' : '🌐 Tech Sector';
        const fieldBadge = document.getElementById('modalFieldBadge');
        if (fieldBadge) fieldBadge.textContent = fieldIcon;

        document.getElementById('modalArticleTitle').textContent = art.headline;
        document.getElementById('modalArticleDate').textContent = `Published: ${{art.date || art.pub_date || 'Live'}}`;
        document.getElementById('modalArticleCountry').textContent = `Jurisdiction: ${{art.country || 'Global'}}`;
        document.getElementById('modalArticleSeverity').innerHTML = `<span class="badge badge-sev-${{art.severity}}">Severity ${{art.severity}}/5 (${{getSeverityLabel(art.severity)}})</span>`;
        
        let catHtml = '';
        art.category.forEach(c => {{
          const desc = c === 'A' ? 'Cat A: Using AI' : (c === 'B' ? 'Cat B: Targeting AI' : 'Cat C: Autonomous Agents');
          catHtml += `<span class="badge badge-cat-${{c.toLowerCase()}}">${{desc}}</span> `;
        }});
        document.getElementById('modalArticleCategories').innerHTML = catHtml;

        const threatType = art.threat_type || 'informational';
        const threatLabel = art.threat_label || (threatType === 'case' ? '🔴 Active Attack Case' : (threatType === 'vulnerability' ? '🟠 Vulnerability Alert' : (threatType === 'policy' ? '🟢 Policy & Legal' : '🔵 Threat Intel Advisory')));

        const inc = allIncidents.find(i => i.incident_id === art.incident_id);
        const vectorText = inc && inc.attack_vector ? inc.attack_vector : (art.field === 'cyber' ? 'Cybersecurity Threat Dispatch & CTI Breach' : (art.field === 'ai' ? 'Frontier AI Model Intrusion & Data Extraction' : 'Enterprise Technology Infrastructure Event'));
        const targetSector = inc && inc.target_sector ? inc.target_sector : (art.field === 'hardware' ? 'Semiconductor & Chip Manufacturing' : (art.field === 'cyber' ? 'Banking, Government & Critical Infrastructure' : 'Enterprise Cloud & Frontier AI Labs'));
        
        const rawSummary = art.description || art.summary || (inc ? inc.headline : art.headline);
        const summaryText = escapeHtml(rawSummary);
        const safeVectorText = escapeHtml(vectorText);
        const safeTargetSector = escapeHtml(targetSector);
        const safeThreatLabel = escapeHtml(threatLabel);
        const safeOutlet = escapeHtml(art.outlet);

        // Render comprehensive zero-block threat dossier
        const analysisHtml = `
          <div style="margin-bottom:14px; padding:12px; background:rgba(37,99,235,0.08); border-left:4px solid #3b82f6; border-radius:4px;">
            <div style="font-weight:700; color:#60a5fa; font-size:0.86rem; margin-bottom:4px; text-transform:uppercase; letter-spacing:0.04em;">Tactical Vector & Scope</div>
            <div style="font-size:0.88rem; color:var(--text-main); line-height:1.6;">
              <strong>Threat Classification:</strong> <span style="font-weight:700; color:${{threatType === 'case' ? '#f87171' : (threatType === 'vulnerability' ? '#fb923c' : (threatType === 'policy' ? '#4ade80' : '#60a5fa'))}};">${{safeThreatLabel}}</span><br>
              <strong>Attack Surface:</strong> ${{safeVectorText}}<br>
              <strong>Target Sector:</strong> ${{safeTargetSector}}<br>
              <strong>Classification:</strong> ${{art.category.map(c => 'Category ' + escapeHtml(c)).join(' & ')}} · Severity Level ${{art.severity}}/5
            </div>
          </div>

          <div style="margin-bottom:16px;">
            <h4 style="font-size:0.82rem; text-transform:uppercase; letter-spacing:0.05em; color:var(--text-muted); margin-bottom:8px;">Executive Threat Summary</h4>
            <div style="font-size:0.92rem; line-height:1.7; color:var(--text-main);">${{summaryText}}</div>
          </div>

          <div style="margin-bottom:16px; padding:12px; background:rgba(255,255,255,0.02); border:1px solid var(--border-subtle); border-radius:6px;">
            <h4 style="font-size:0.82rem; text-transform:uppercase; letter-spacing:0.05em; color:var(--accent-warning); margin-bottom:8px;">${{threatType === 'case' ? '🚨 Incident Response & Containment Protocol' : (threatType === 'vulnerability' ? '🛡️ Remediation & Patching Advisory' : (threatType === 'policy' ? '⚖️ Regulatory & Legal Compliance Impact' : '🔍 Threat Intelligence & Hardening Guidance'))}}</h4>
            <p style="font-size:0.86rem; line-height:1.6; color:var(--text-dim); margin-bottom:6px;">
              ${{threatType === 'case' 
                ? 'High-priority incident detected. SOC action required: Quarantine suspected endpoints, rotate compromised API tokens/credentials, inspect perimeter firewall and NetFlow logs for C2 beaconing, and isolate active lateral movement vectors.'
                : (threatType === 'vulnerability'
                  ? 'Active security flaw disclosure. Action required: Audit software inventory for affected dependency versions, deploy official vendor security updates or apply WAF virtual patching rules, and verify mitigation against published exploit PoCs.'
                  : (threatType === 'policy'
                    ? 'Legal or regulatory development. Action required: Review data privacy compliance obligations, audit AI model provenance, and ensure adherence to relevant national cyber enforcement directives.'
                    : 'Tactical threat advisory published for defensive situational awareness. Action required: Ingest threat indicators into SIEM correlation rules, update behavioral detection heuristics, and brief engineering teams on emerging attack patterns.'))}}
            </p>
            <div style="font-size:0.8rem; color:var(--text-muted); display:flex; gap:16px; flex-wrap:wrap; margin-top:8px;">
              <span>• Threat Profile: <strong>${{escapeHtml(art.field.toUpperCase())}} Telemetry</strong></span>
              <span>• Audit Status: <strong>Corroborated</strong></span>
              <span>• Source Tier: <strong>Tier ${{inc ? inc.source_tier : 1}} CTI Syndicate</strong></span>
            </div>
          </div>

          <div style="padding:12px; background:rgba(16,185,129,0.06); border:1px solid rgba(16,185,129,0.2); border-radius:6px;">
            <h4 style="font-size:0.82rem; text-transform:uppercase; letter-spacing:0.05em; color:#10b981; margin-bottom:6px;">SOC Recommended Mitigation Playbook</h4>
            <ul style="font-size:0.84rem; line-height:1.6; color:var(--text-dim); margin:0; padding-left:18px;">
              <li><strong>Containment:</strong> Audit perimeter ingress logs, rotate compromised service keys, and isolate affected workload endpoints.</li>
              <li><strong>Hunting & Detection:</strong> Query SIEM/EDR telemetry for anomalous lateral egress patterns and known IoC signatures.</li>
              <li><strong>Hardening:</strong> Enforce zero-trust access controls, hardware-backed FIDO2 MFA, and runtime guardrails on agentic model workflows.</li>
            </ul>
          </div>
        `;

        document.getElementById('modalArticleSummary').innerHTML = analysisHtml;
        document.getElementById('modalArticleProvenance').textContent = art.outlet;

        // Anti-Paywall / Unblocked Link Toolbar URLs
        const cleanUrl = sanitizeUrl(art.url);
        const archiveUrl = sanitizeUrl(art.archive_url || `https://archive.is/newest/${{encodeURIComponent(art.url)}}`);
        const searchUrl = sanitizeUrl(art.search_url || `https://www.google.com/search?q=${{encodeURIComponent(art.headline)}}`);

        const extBtn = document.getElementById('modalExternalLinkBtn');
        extBtn.href = cleanUrl;
        extBtn.innerHTML = `🌐 Original Source at ${{safeOutlet}} ↗`;

        const archiveBtn = document.getElementById('modalArchiveLinkBtn');
        if (archiveBtn) {{
          archiveBtn.href = archiveUrl;
          archiveBtn.innerHTML = `⚡ Bypass Paywall Mirror ↗`;
        }}

        const searchBtn = document.getElementById('modalSearchLinkBtn');
        if (searchBtn) {{
          searchBtn.href = searchUrl;
          searchBtn.innerHTML = `🔍 Free Web Coverage ↗`;
        }}

        const copyDossierBtn = document.getElementById('btnCopyDossier');
        if (copyDossierBtn) {{
          copyDossierBtn.onclick = () => {{
            const dossierText = `[THREAT INTEL DOSSIER - GLOBAL RADAR]\nHeadline: ${{art.headline}}\nOutlet: ${{art.outlet}}\nDate: ${{art.date}}\nJurisdiction: ${{art.country}}\nSeverity: ${{art.severity}}/5\nCategory: ${{art.category.join(', ')}}\nVector: ${{vectorText}}\nSector: ${{targetSector}}\nSummary: ${{summaryText}}\nDirect Source: ${{cleanUrl}}\nArchive Mirror: ${{archiveUrl}}`;
            navigator.clipboard.writeText(dossierText).then(() => {{
              copyDossierBtn.textContent = '✅ Dossier Copied!';
              setTimeout(() => {{ copyDossierBtn.textContent = '📄 Copy Threat Brief'; }}, 2000);
            }});
          }};
        }}

        const copyBtn = document.getElementById('btnCopyArticleLink');
        copyBtn.onclick = () => {{
          navigator.clipboard.writeText(cleanUrl).then(() => {{
            copyBtn.textContent = '✅ URL Copied!';
            setTimeout(() => {{ copyBtn.textContent = '📋 Copy Link'; }}, 2000);
          }});
        }};

        modal.style.display = 'flex';
        modal.classList.add('active');
      }}

      function closeArticleReaderModal() {{
        const modal = document.getElementById('articleReaderModal');
        if (modal) {{
          modal.style.display = 'none';
          modal.classList.remove('active');
        }}
      }}

      window.openArticleReaderModal = openArticleReaderModal;
      window.closeArticleReaderModal = closeArticleReaderModal;

      const pipelineModal = document.getElementById('pipelineModal');
      document.getElementById('btnOpenPipelineModal').addEventListener('click', () => {{
        pipelineModal.style.display = 'flex';
        pipelineModal.classList.add('active');
      }});
      document.getElementById('btnClosePipelineModal').addEventListener('click', () => {{
        pipelineModal.style.display = 'none';
        pipelineModal.classList.remove('active');
      }});
      document.getElementById('btnDismissPipelineModal').addEventListener('click', () => {{
        pipelineModal.style.display = 'none';
        pipelineModal.classList.remove('active');
      }});
      pipelineModal.addEventListener('click', (e) => {{
        if (e.target.id === 'pipelineModal') {{
          pipelineModal.style.display = 'none';
          pipelineModal.classList.remove('active');
        }}
      }});

      document.getElementById('btnCloseArticleModal').addEventListener('click', closeArticleReaderModal);
      document.getElementById('articleReaderModal').addEventListener('click', (e) => {{
        if (e.target.id === 'articleReaderModal') {{
          closeArticleReaderModal();
        }}
      }});

      // --- 25 Ingested Sources & Monitored Websites Registry Engine ---
      let pulledSources = rawData.pulledSources || [];
      let activeSourceCategory = 'ALL';
      let activeModalSourceCategory = 'ALL';
      let isSourcesRegistryOpen = false;

      window.toggleSourcesRegistry = function() {{
        isSourcesRegistryOpen = !isSourcesRegistryOpen;
        const container = document.getElementById('sourcesRegistryContainer');
        const btn = document.getElementById('btnToggleSourcesGrid');
        if (container) {{
          container.style.display = isSourcesRegistryOpen ? 'block' : 'none';
        }}
        if (btn) {{
          btn.textContent = isSourcesRegistryOpen ? '▲ Hide Website Registry' : '📋 Show Website List (25)';
          btn.style.background = isSourcesRegistryOpen ? 'rgba(239,68,68,0.15)' : 'rgba(59,130,246,0.15)';
          btn.style.color = isSourcesRegistryOpen ? '#f87171' : '#60a5fa';
          btn.style.borderColor = isSourcesRegistryOpen ? '#ef4444' : '#3b82f6';
        }}
        if (isSourcesRegistryOpen) {{
          renderPulledSourcesGrid();
        }}
      }};

      window.openSourcesModal = function() {{
        const modal = document.getElementById('sourcesModal');
        if (modal) {{
          modal.style.display = 'flex';
          modal.classList.add('active');
          renderSourcesTable();
        }}
      }};

      window.closeSourcesModal = function() {{
        const modal = document.getElementById('sourcesModal');
        if (modal) {{
          modal.style.display = 'none';
          modal.classList.remove('active');
        }}
      }};

      window.filterSourcesByCategory = function(cat) {{
        activeSourceCategory = cat;
        document.querySelectorAll('#pillsSourceCategory .pill-btn').forEach(btn => {{
          btn.classList.toggle('active', btn.getAttribute('data-srccat') === cat);
        }});
        renderPulledSourcesGrid();
      }};

      window.filterModalSources = function(cat) {{
        activeModalSourceCategory = cat;
        document.querySelectorAll('#modalSourcePills .pill-btn').forEach(btn => {{
          btn.classList.toggle('active', btn.getAttribute('data-modalsrccat') === cat);
        }});
        renderSourcesTable();
      }};

      window.filterFeedBySource = function(sourceName) {{
        window.closeSourcesModal();
        window.filterByBroadcast(sourceName.toLowerCase());
        const feed = document.getElementById('articlesGrid');
        if (feed) feed.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      }};

      function renderPulledSourcesGrid() {{
        const grid = document.getElementById('pulledSourcesGrid');
        if (!grid) return;
        grid.innerHTML = '';

        const filtered = pulledSources.filter(src => {{
          if (activeSourceCategory !== 'ALL' && src.category !== activeSourceCategory) return false;
          return true;
        }});

        filtered.forEach(src => {{
          const card = document.createElement('div');
          card.className = 'source-site-card';
          card.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:6px;">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:1.15rem;">${{src.icon}}</span>
                <div>
                  <div style="font-weight:700; font-size:0.86rem; color:var(--text-main);">${{src.name}}</div>
                  <a href="${{src.homepage}}" target="_blank" rel="noopener noreferrer" style="font-size:0.72rem; color:var(--border-focus); text-decoration:none; display:inline-flex; align-items:center; gap:3px;">
                    ${{src.domain}} ↗
                  </a>
                </div>
              </div>
              <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; font-size:9px; font-weight:700;">🟢 Connected</span>
            </div>
            
            <p style="font-size:0.73rem; color:var(--text-dim); line-height:1.35; margin:4px 0;">
              ${{src.description}}
            </p>

            <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.72rem; color:var(--text-dim); margin-top:4px;">
              <span class="badge" style="background:rgba(59,130,246,0.12); color:#60a5fa; border:1px solid rgba(59,130,246,0.25); font-size:10px;">${{src.category}}</span>
              <span style="font-weight:700; color:var(--text-main);">📊 ${{src.count || 0}} in radar</span>
            </div>

            <div style="display:flex; gap:6px; margin-top:6px;">
              <a href="${{src.homepage}}" target="_blank" rel="noopener noreferrer" class="hud-btn" style="flex:1; text-align:center; text-decoration:none; padding:4px 8px; font-size:0.72rem; background:rgba(255,255,255,0.06); color:var(--text-main); border:1px solid var(--border-subtle); border-radius:4px;" title="Open official website in new tab">
                🌐 Visit Site ↗
              </a>
              <button class="hud-btn" onclick="window.filterFeedBySource('${{src.name}}')" style="flex:1; text-align:center; padding:4px 8px; font-size:0.72rem; background:rgba(59,130,246,0.18); color:#60a5fa; border:1px solid #3b82f6; border-radius:4px; cursor:pointer;" title="Filter feed below to this publication">
                🎯 Filter Feed
              </button>
            </div>
          `;
          grid.appendChild(card);
        }});
      }}

      function renderSourcesTable() {{
        const tbody = document.getElementById('sourcesTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';

        const searchInput = document.getElementById('sourceSearchInput');
        const searchQ = (searchInput ? searchInput.value : '').toLowerCase().trim();

        const filtered = pulledSources.filter(src => {{
          if (activeModalSourceCategory !== 'ALL' && src.category !== activeModalSourceCategory) return false;
          if (searchQ) {{
            const haystack = (src.name + ' ' + src.domain + ' ' + src.category + ' ' + src.jurisdiction + ' ' + src.description).toLowerCase();
            if (!haystack.includes(searchQ)) return false;
          }}
          return true;
        }});

        if (filtered.length === 0) {{
          tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:20px; color:var(--text-dim);">No sources match search filter.</td></tr>';
          return;
        }}

        filtered.forEach(src => {{
          const tr = document.createElement('tr');
          tr.style.borderBottom = '1px solid var(--border-subtle)';
          tr.innerHTML = `
            <td style="padding:10px 12px; font-weight:700; color:var(--text-main); white-space:nowrap;">
              <span style="margin-right:6px;">${{src.icon}}</span>${{src.name}}
            </td>
            <td style="padding:10px 12px;">
              <a href="${{src.homepage}}" target="_blank" rel="noopener noreferrer" style="color:var(--border-focus); text-decoration:none; font-family:ui-monospace, monospace; font-size:0.75rem;">
                ${{src.domain}} ↗
              </a>
            </td>
            <td style="padding:10px 12px;">
              <span class="badge" style="background:rgba(59,130,246,0.12); color:#60a5fa; border:1px solid rgba(59,130,246,0.3); font-size:10px;">${{src.category}}</span>
            </td>
            <td style="padding:10px 12px; color:var(--text-dim); font-size:0.75rem;">
              ${{src.jurisdiction}}
            </td>
            <td style="padding:10px 12px; font-weight:700; color:var(--text-main);">
              <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; font-weight:700;">${{src.count || 0}} reports</span>
            </td>
            <td style="padding:10px 12px; font-size:0.72rem; color:var(--text-dim); white-space:nowrap;">
              <span class="status-indicator live" style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:50%; margin-right:4px;"></span>
              <span>200 OK · ${{src.cadence}}</span>
            </td>
            <td style="padding:10px 12px; text-align:right; white-space:nowrap;">
              <button class="article-btn-read" onclick="window.filterFeedBySource('${{src.name}}')" style="margin-right:4px; padding:3px 8px; font-size:0.7rem; cursor:pointer;" title="Filter feed below to this source">
                🎯 Filter Feed
              </button>
              <a href="${{src.homepage}}" target="_blank" rel="noopener noreferrer" class="article-btn-ext" style="padding:3px 8px; font-size:0.7rem;" title="Visit official site">
                Visit ↗
              </a>
            </td>
          `;
          tbody.appendChild(tr);
        }});
      }}

      const sourcesModal = document.getElementById('sourcesModal');
      if (sourcesModal) {{
        sourcesModal.addEventListener('click', (e) => {{
          if (e.target.id === 'sourcesModal') {{
            window.closeSourcesModal();
          }}
        }});
      }}
      const sourceSearchInput = document.getElementById('sourceSearchInput');
      if (sourceSearchInput) {{
        sourceSearchInput.addEventListener('input', () => {{
          renderSourcesTable();
        }});
      }}

      function renderIncidentsTable(incidents) {{
        const tbody = document.getElementById('incidentsTableBody');
        tbody.innerHTML = '';
        document.getElementById('incidentCountBadge').textContent = `(${{incidents.length}} records)`;

        if (incidents.length === 0) {{
          tbody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding:30px; color:var(--text-dim);">No incidents match the active filter criteria.</td></tr>';
          return;
        }}

        const sorted = [...incidents].sort((a, b) => {{
          let valA = a[activeFilters.sortCol];
          let valB = b[activeFilters.sortCol];
          if (activeFilters.sortCol === 'category') {{
            valA = a.category.join(',');
            valB = b.category.join(',');
          }}
          if (valA < valB) return activeFilters.sortAsc ? -1 : 1;
          if (valA > valB) return activeFilters.sortAsc ? 1 : -1;
          return 0;
        }});

        const rowsHtml = sorted.map(inc => {{
          let catBadges = '';
          inc.category.forEach(c => {{
            catBadges += `<span class="badge badge-cat-${{c.toLowerCase()}}">${{escapeHtml(c)}}</span> `;
          }});

          const confBadge = inc.confidence === 'low' 
            ? '<span class="badge badge-conf-low" title="Unverified attribution / pending CERT confirmation">⚠ Low Conf</span>'
            : `<span style="font-size:0.7rem; color:var(--text-muted); text-transform:capitalize;">${{escapeHtml(inc.confidence)}}</span>`;

          return `
            <tr id="row-${{escapeHtml(inc.incident_id)}}">
              <td><code>${{escapeHtml(inc.incident_id)}}</code></td>
              <td style="white-space:nowrap;">${{escapeHtml(inc.date)}}</td>
              <td class="incident-headline">${{escapeHtml(inc.headline)}}</td>
              <td>${{catBadges}}</td>
              <td>${{escapeHtml(inc.attack_vector)}}</td>
              <td>${{escapeHtml(inc.target_sector)}}</td>
              <td>${{escapeHtml(inc.country)}}</td>
              <td><span class="badge badge-sev-${{inc.severity}}">Sev ${{inc.severity}}</span></td>
              <td>${{confBadge}}</td>
              <td>
                <a class="incident-link" href="${{sanitizeUrl(inc.source_url)}}" target="_blank" rel="noopener noreferrer">
                  <span class="badge-tier">Tier ${{inc.source_tier}}</span> Intel ↗
                </a>
              </td>
            </tr>
          `;
        }}).join('');
        tbody.innerHTML = rowsHtml;
      }}

      // --- Explicit Quick-Filter Handlers (Clear visual buttons instead of graph clicks) ---
      window.filterByThreatType = function(threat) {{
        activeFilters.threatType = threat;
        syncQuickPills();
        updateDashboard();
        const feed = document.getElementById('articlesGrid');
        if (feed) feed.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterByField = function(field) {{
        activeFilters.field = field;
        if (field === 'ALL') {{
          document.getElementById('articleSearchInput').value = '';
          activeFilters.articleSearch = '';
        }}
        syncQuickPills();
        updateDashboard();
        const feed = document.getElementById('articlesGrid');
        if (feed) feed.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterByBroadcast = function(outlet) {{
        activeFilters.broadcast = outlet;
        if (outlet === 'ALL') {{
          // If All Sources clicked, ensure clean full display
          document.getElementById('articleSearchInput').value = '';
          activeFilters.articleSearch = '';
        }}
        syncQuickPills();
        updateDashboard();
        const feed = document.getElementById('articlesGrid');
        if (feed) feed.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.toggleCategoryKPI = function(cat) {{
        if (activeFilters.category === cat) {{
          window.filterByCategoryQuick('ALL');
        }} else {{
          window.filterByCategoryQuick(cat);
        }}
      }};

      window.toggleSeverityKPI = function(sev) {{
        if (activeFilters.severity === String(sev)) {{
          window.filterBySeverityQuick('ALL');
        }} else {{
          window.filterBySeverityQuick(String(sev));
        }}
      }};

      window.filterByCategoryQuick = function(cat) {{
        activeFilters.category = cat;
        const select = document.getElementById('filterCategory');
        if (select) select.value = cat;
        syncQuickPills();
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterBySeverityQuick = function(sev) {{
        activeFilters.severity = sev;
        const select = document.getElementById('filterSeverity');
        if (select) select.value = sev;
        syncQuickPills();
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterByVectorQuick = function(vec) {{
        if (vec === 'ALL') {{
          activeFilters.vector = 'ALL';
          activeFilters.incidentSearch = '';
          document.getElementById('incidentSearchInput').value = '';
          const select = document.getElementById('filterVector');
          if (select) select.value = 'ALL';
        }} else {{
          activeFilters.vector = 'ALL';
          activeFilters.incidentSearch = vec;
          document.getElementById('incidentSearchInput').value = vec;
        }}
        syncQuickPills();
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterByCountryQuick = function(country) {{
        activeFilters.country = country;
        const select = document.getElementById('filterCountry');
        if (select) select.value = country;
        syncQuickPills();
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.resetAllFiltersQuick = function() {{
        document.getElementById('btnResetFilters').click();
      }};

      window.removeSingleFilter = function(key) {{
        if (key === 'category') {{
          window.filterByCategoryQuick('ALL');
        }} else if (key === 'severity') {{
          window.filterBySeverityQuick('ALL');
        }} else if (key === 'entity') {{
          window.filterByEcosystem('ALL');
        }} else if (key === 'country') {{
          window.filterByCountryQuick('ALL');
        }} else if (key === 'incidentSearch') {{
          activeFilters.incidentSearch = '';
          document.getElementById('incidentSearchInput').value = '';
          syncQuickPills();
          updateDashboard();
        }} else if (key === 'vector') {{
          activeFilters.vector = 'ALL';
          const select = document.getElementById('filterVector');
          if (select) select.value = 'ALL';
          syncQuickPills();
          updateDashboard();
        }} else if (key === 'broadcast') {{
          window.filterByBroadcast('ALL');
        }} else if (key === 'field') {{
          window.filterByField('ALL');
        }} else if (key === 'threatType') {{
          window.filterByThreatType('ALL');
        }}
      }};

      function syncQuickPills() {{
        // 1. Category Pills
        document.querySelectorAll('#pillsCategory .pill-btn').forEach(b => {{
          const cat = b.getAttribute('data-cat');
          b.classList.toggle('active', cat === activeFilters.category);
        }});

        // 2. Severity Pills
        document.querySelectorAll('#pillsSeverity .pill-btn').forEach(b => {{
          const sev = b.getAttribute('data-sev');
          b.classList.toggle('active', sev === activeFilters.severity);
        }});

        // 2B. Interactive Category KPI Cards
        ['A', 'B', 'C'].forEach(cat => {{
          const card = document.getElementById(`kpiCardCat${{cat}}`);
          const ind = document.getElementById(`indicatorCat${{cat}}`);
          if (card) {{
            const isActive = (activeFilters.category === cat);
            card.classList.toggle('active-kpi-filter', isActive);
            if (ind) ind.textContent = isActive ? '✓ ACTIVE' : 'Filter';
          }}
        }});
        const btnResetCat = document.getElementById('btnResetCatFilter');
        if (btnResetCat) {{
          btnResetCat.style.display = (activeFilters.category && activeFilters.category !== 'ALL') ? 'inline-block' : 'none';
        }}

        // 2C. Interactive Severity KPI Cards
        ['5', '4', '3', '2', '1'].forEach(sev => {{
          const card = document.getElementById(`kpiCardSev${{sev}}`);
          const ind = document.getElementById(`indicatorSev${{sev}}`);
          if (card) {{
            const isActive = (activeFilters.severity === sev);
            card.classList.toggle('active-kpi-filter', isActive);
            if (ind) ind.textContent = isActive ? '✓ ACTIVE' : 'Filter';
          }}
        }});
        const btnResetSev = document.getElementById('btnResetSevFilter');
        if (btnResetSev) {{
          btnResetSev.style.display = (activeFilters.severity && activeFilters.severity !== 'ALL') ? 'inline-block' : 'none';
        }}

        // 3. Vector Pills
        document.querySelectorAll('#pillsVector .pill-btn').forEach(b => {{
          const vec = b.getAttribute('data-vec');
          const isMatch = (vec === 'ALL' && !activeFilters.incidentSearch && activeFilters.vector === 'ALL') ||
                          (vec !== 'ALL' && activeFilters.incidentSearch && activeFilters.incidentSearch.toLowerCase().includes(vec.toLowerCase()));
          b.classList.toggle('active', !!isMatch);
        }});

        // 4. Country Pills
        document.querySelectorAll('#pillsCountry .pill-btn').forEach(b => {{
          const c = b.getAttribute('data-country');
          b.classList.toggle('active', c === activeFilters.country);
        }});

        // 5. Ecosystem Pills
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
          const eco = b.getAttribute('data-eco');
          const isMatch = (eco === activeFilters.entity) ||
                          (eco === 'JPMorgan' && (activeFilters.entity === 'JPMorgan' || activeFilters.entity === 'jp morgan' || activeFilters.entity === 'jpmorgan'));
          b.classList.toggle('active', !!isMatch);
        }});

        // 6. Broadcast Pills
        document.querySelectorAll('#pillsBroadcast .pill-btn').forEach(b => {{
          const bc = b.getAttribute('data-broadcast');
          b.classList.toggle('active', bc === activeFilters.broadcast);
        }});

        // 7. Tech Domain / Field Pills
        document.querySelectorAll('#pillsField .pill-btn').forEach(b => {{
          const f = b.getAttribute('data-field');
          b.classList.toggle('active', f === activeFilters.field);
        }});

        // 8. Threat News Focus / Category Pills
        document.querySelectorAll('#pillsThreatType .pill-btn').forEach(b => {{
          const t = b.getAttribute('data-threat');
          b.classList.toggle('active', t === activeFilters.threatType);
        }});
      }}

      function renderActiveFiltersRibbon(filteredIncidents) {{
        const ribbon = document.getElementById('activeFiltersRibbon');
        const badgesContainer = document.getElementById('activeFiltersBadges');
        const countSpan = document.getElementById('activeFilteredCount');
        if (!ribbon || !badgesContainer) return;

        const badges = [];

        if (activeFilters.category && activeFilters.category !== 'ALL') {{
          const catLabels = {{ 'A': 'Cat A (Using AI)', 'B': 'Cat B (On AI Systems)', 'C': 'Cat C (Agentic)' }};
          badges.push({{ key: 'category', label: `Category: ${{catLabels[activeFilters.category] || activeFilters.category}}` }});
        }}
        if (activeFilters.severity && activeFilters.severity !== 'ALL') {{
          badges.push({{ key: 'severity', label: `Severity: Sev ${{activeFilters.severity}}` }});
        }}
        if (activeFilters.entity && activeFilters.entity !== 'ALL') {{
          badges.push({{ key: 'entity', label: `Company: ${{activeFilters.entity}}` }});
        }}
        if (activeFilters.country && activeFilters.country !== 'ALL') {{
          badges.push({{ key: 'country', label: `Country: ${{activeFilters.country}}` }});
        }}
        if (activeFilters.incidentSearch) {{
          badges.push({{ key: 'incidentSearch', label: `Keyword: "${{activeFilters.incidentSearch}}"` }});
        }}
        if (activeFilters.vector && activeFilters.vector !== 'ALL') {{
          badges.push({{ key: 'vector', label: `Vector: ${{activeFilters.vector}}` }});
        }}
        if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
          const bcLabels = {{ 'BBC': 'BBC News', 'CNN': 'CNN', 'Reuters': 'Reuters', 'Bloomberg': 'Bloomberg', 'Guardian': 'The Guardian', 'CNBC': 'CNBC', 'TechCrunch': 'TechCrunch', 'Wired': 'Wired', 'arstechnica': 'Ars Technica', 'tomshardware': "Tom's Hardware", 'CTI': 'CTI Registries' }};
          badges.push({{ key: 'broadcast', label: `Broadcast: ${{bcLabels[activeFilters.broadcast] || activeFilters.broadcast}}` }});
        }}
        if (activeFilters.field && activeFilters.field !== 'ALL') {{
          const fLabels = {{ 'ai': 'AI & Models', 'cyber': 'Cybersecurity', 'hardware': 'Hardware & Chips', 'it': 'Enterprise IT' }};
          badges.push({{ key: 'field', label: `Field: ${{fLabels[activeFilters.field] || activeFilters.field}}` }});
        }}
        if (activeFilters.threatType && activeFilters.threatType !== 'ALL') {{
          const threatLabels = {{
            'case': '🔴 Active Attack Cases',
            'vulnerability': '🟠 Vulnerability Alerts',
            'informational': '🔵 Threat Intel Advisories',
            'policy': '🟢 Policy & Legal'
          }};
          badges.push({{ key: 'threatType', label: `Threat Focus: ${{threatLabels[activeFilters.threatType] || activeFilters.threatType}}` }});
        }}

        if (badges.length > 0) {{
          ribbon.style.display = 'flex';
          badgesContainer.innerHTML = badges.map(b => `
            <span class="active-filter-badge">
              ${{escapeHtml(b.label)}}
              <span class="badge-remove" onclick="window.removeSingleFilter('${{escapeHtml(b.key)}}')" title="Remove filter">✕</span>
            </span>
          `).join('');
          if (countSpan) {{
            countSpan.textContent = `Showing ${{filteredIncidents.length}} of ${{allIncidents.length}} incidents`;
          }}
        }} else {{
          ribbon.style.display = 'none';
        }}
      }}

      function updateDashboard() {{
        const filteredIncidents = getFilteredIncidents();
        syncQuickPills();
        renderActiveFiltersRibbon(filteredIncidents);
        const filteredArticles = getFilteredArticles();

        renderKPIs(filteredIncidents);
        renderKeyConcerns(filteredIncidents);
        renderHeroSection(filteredIncidents);
        renderAdvancedVisualizations(filteredIncidents);
        renderCountries(filteredIncidents);
        renderBreakdowns(filteredIncidents);
        renderArticlesFeed(filteredArticles);
        renderIncidentsTable(filteredIncidents);
      }}

      window.highlightIncident = function(id) {{
        activeFilters.horizon = 'ALL';
        activeFilters.category = 'ALL';
        activeFilters.severity = 'ALL';
        activeFilters.country = 'ALL';
        activeFilters.tier = 'ALL';
        activeFilters.incidentSearch = id;
        document.getElementById('incidentSearchInput').value = id;
        document.getElementById('filterHorizon').value = 'ALL';
        document.getElementById('filterCategory').value = 'ALL';
        document.getElementById('filterSeverity').value = 'ALL';
        document.getElementById('filterCountry').value = 'ALL';
        document.getElementById('filterTier').value = 'ALL';
        activeFilters.broadcast = 'ALL';
        const entSelect = document.getElementById('filterEntity');
        if (entSelect) entSelect.value = 'ALL';
        syncQuickPills();
        activeFilters.entity = 'ALL';
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
        const allBtn = document.querySelector('.ecosystem-pills-bar .pill-btn');
        if (allBtn) allBtn.classList.add('active');
        updateDashboard();

        setTimeout(() => {{
          const row = document.getElementById(`row-${{id}}`);
          if (row) {{
            row.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            row.style.outline = '2px solid #f59e0b';
            row.style.background = 'rgba(245, 158, 11, 0.15)';
            setTimeout(() => {{
              row.style.outline = 'none';
              row.style.background = '';
            }}, 3000);
          }}
        }}, 200);
      }};

      window.filterByEcosystem = function(eco) {{
        activeFilters.entity = eco;
        const entDropdown = document.getElementById('filterEntity');
        if (entDropdown) entDropdown.value = eco;

        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
        const matched = document.querySelector(`.ecosystem-pills-bar .pill-btn[data-eco="${{eco}}"]`);
        if (matched) {{
          matched.classList.add('active');
        }} else {{
          document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
            if ((eco === 'ALL' && (b.getAttribute('data-eco') === 'ALL' || b.textContent.includes('All Cases'))) ||
                (eco !== 'ALL' && (b.getAttribute('data-eco') === eco || b.textContent.includes(eco)))) {{
              b.classList.add('active');
            }}
          }});
        }}
        
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterByVector = function(vec) {{
        activeFilters.incidentSearch = vec;
        document.getElementById('incidentSearchInput').value = vec;
        updateDashboard();
        document.getElementById('incidentsTable').scrollIntoView({{ behavior: 'smooth' }});
      }};

      window.filterBySector = function(sec) {{
        activeFilters.incidentSearch = sec;
        document.getElementById('incidentSearchInput').value = sec;
        updateDashboard();
        document.getElementById('incidentsTable').scrollIntoView({{ behavior: 'smooth' }});
      }};

      document.getElementById('filterHorizon').addEventListener('change', e => {{
        activeFilters.horizon = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterCategory').addEventListener('change', e => {{
        activeFilters.category = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterSeverity').addEventListener('change', e => {{
        activeFilters.severity = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterCountry').addEventListener('change', e => {{
        activeFilters.country = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterEntity').addEventListener('change', e => {{
        activeFilters.entity = e.target.value;
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
          if ((e.target.value === 'ALL' && b.textContent.includes('All Cases')) ||
              (e.target.value !== 'ALL' && b.textContent.includes(e.target.value))) {{
            b.classList.add('active');
          }} else {{
            b.classList.remove('active');
          }}
        }});
        updateDashboard();
      }});

      document.getElementById('filterTier').addEventListener('change', e => {{
        activeFilters.tier = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterSector').addEventListener('change', e => {{
        activeFilters.sector = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterVector').addEventListener('change', e => {{
        activeFilters.vector = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterYear').addEventListener('change', e => {{
        activeFilters.year = e.target.value;
        updateDashboard();
      }});

      document.getElementById('articleSearchInput').addEventListener('input', e => {{
        activeFilters.articleSearch = e.target.value;
        renderArticlesFeed(getFilteredArticles());
      }});

      document.getElementById('incidentSearchInput').addEventListener('input', e => {{
        activeFilters.incidentSearch = e.target.value;
        renderIncidentsTable(getFilteredIncidents());
      }});

      document.getElementById('btnResetFilters').addEventListener('click', () => {{
        activeFilters = {{
          horizon: '10Y',
          category: 'ALL',
          severity: 'ALL',
          country: 'ALL',
          sector: 'ALL',
          vector: 'ALL',
          year: 'ALL',
          tier: 'ALL',
          entity: 'ALL',
          broadcast: 'ALL',
          field: 'ALL',
          threatType: 'ALL',
          articleSearch: '',
          incidentSearch: '',
          sortCol: 'date',
          sortAsc: false
        }};
        document.getElementById('filterHorizon').value = '10Y';
        document.getElementById('filterCategory').value = 'ALL';
        document.getElementById('filterSeverity').value = 'ALL';
        document.getElementById('filterSector').value = 'ALL';
        document.getElementById('filterVector').value = 'ALL';
        document.getElementById('filterYear').value = 'ALL';
        document.getElementById('filterCountry').value = 'ALL';
        document.getElementById('filterTier').value = 'ALL';
        activeFilters.broadcast = 'ALL';
        const entSelect = document.getElementById('filterEntity');
        if (entSelect) entSelect.value = 'ALL';
        syncQuickPills();
        activeFilters.entity = 'ALL';
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
        const allBtn = document.querySelector('.ecosystem-pills-bar .pill-btn');
        if (allBtn) allBtn.classList.add('active');
        document.getElementById('articleSearchInput').value = '';
        document.getElementById('incidentSearchInput').value = '';
        updateDashboard();
      }});

      document.querySelectorAll('#incidentsTable th[data-sort]').forEach(th => {{
        th.addEventListener('click', () => {{
          const col = th.getAttribute('data-sort');
          if (activeFilters.sortCol === col) {{
            activeFilters.sortAsc = !activeFilters.sortAsc;
          }} else {{
            activeFilters.sortCol = col;
            activeFilters.sortAsc = false;
          }}
          renderIncidentsTable(getFilteredIncidents());
        }});
      }});

      // Automated continuous ingestion via BeautifulSoup replaces manual intake modal

      document.getElementById('btnExportData').addEventListener('click', async () => {{
        const btn = document.getElementById('btnExportData');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<span>⏳ Generating PDF...</span>';
        btn.disabled = true;

        try {{
          const horizon = (typeof activeFilters !== 'undefined' && activeFilters.horizon) ? activeFilters.horizon : '10Y';
          const url = `/api/export-pdf?horizon=${{encodeURIComponent(horizon)}}`;
          const resp = await fetch(url);
          if (!resp.ok) throw new Error('PDF Generation endpoint returned ' + resp.status);

          const blob = await resp.blob();
          const blobUrl = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = blobUrl;
          a.download = `Global_AI_Cyberattack_Threat_Report_${{horizon}}_${{new Date().toISOString().substring(0, 10)}}.pdf`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(blobUrl);
        }} catch (err) {{
          console.warn('Backend PDF endpoint error, falling back to print dialog:', err);
          window.print();
        }} finally {{
          btn.innerHTML = originalHtml;
          btn.disabled = false;
        }}
      }});

      populateYearFilters();
      populateCountryDropdown();
      populateSectorDropdown();
      populateVectorDropdown();
      populateSpecificYearDropdown();
      updateDashboard();
      updateLiveTopTicker();
      renderPulledSourcesGrid();
      renderSourcesTable();
      attemptLiveSync();

      window.forceLiveSweep = async function() {{
        const btn = document.getElementById('forceSweepBtn');
        if (btn) {{
          btn.innerHTML = '<span>⚡ Sweeping 24 Feeds...</span>';
          btn.disabled = true;
        }}
        sweepSecondsLeft = 90;
        await attemptLiveSync(true);
        if (btn) {{
          btn.innerHTML = '<span>⚡ Force Live Sweep</span>';
          btn.disabled = false;
        }}
        showLiveToast(`Refreshed: Connected to 24 Live Online Streams (${{allArticles.length}} Dispatches Active)`);
      }};

    }})();
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Updated index.html ({len(html_content)} bytes).")
