# verify_canonical_urls.py
import urllib.request

urls = [
    ("CNN Landmark Deepfake Heist", "https://edition.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk/index.html"),
    ("Dark Reading Morris II Worm", "https://www.darkreading.com/application-security/researchers-create-first-generative-ai-worm"),
    ("Microsoft Threat Actors using AI", "https://www.microsoft.com/en-us/security/blog/2024/02/14/staying-ahead-of-threat-actors-in-the-age-of-ai/"),
    ("The Record AI Cyber Defense", "https://therecord.media/ai-cyber-white-house"),
    ("The Record Lead Portal", "https://therecord.media/"),
    ("MITRE ATLAS Official Site", "https://atlas.mitre.org/"),
    ("MITRE ATLAS GitHub Database", "https://github.com/mitre-atlas/atlas-data"),
    ("UK NCSC Official AI Threat Report", "https://www.ncsc.gov.uk/report/impact-of-ai-on-cyber-threat"),
    ("US FTC AI Impersonation Fraud Action", "https://www.ftc.gov/news-events/news/press-releases/2024/01/ftc-proposes-new-protections-combat-ai-impersonation-fraud"),
    ("CISA AI Security Guidance", "https://www.cisa.gov/ai")
]

for name, url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            print(f"[VERIFIED 200] {name} -> {resp.status}")
    except Exception as e:
        print(f"[CHECK] {name} -> {e}")
