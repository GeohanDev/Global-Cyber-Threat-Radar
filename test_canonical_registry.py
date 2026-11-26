import urllib.request
import sys

candidate_urls = [
    ("CNN Hong Kong Deepfake", "https://edition.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk/index.html"),
    ("MITRE ATLAS Official Site", "https://atlas.mitre.org/"),
    ("MITRE ATLAS GitHub", "https://github.com/mitre-atlas/atlas-data"),
    ("Microsoft Threat Intel AI", "https://www.microsoft.com/en-us/security/blog/2024/02/14/staying-ahead-of-threat-actors-in-the-age-of-ai/"),
    ("OWASP GenAI Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
    ("NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework"),
    ("CISA AI Roadmap", "https://www.cisa.gov/ai"),
    ("AI Incident Database", "https://incidentdatabase.ai/"),
    ("The Record AI Cyber White House", "https://therecord.media/ai-cyber-white-house"),
    ("Europol LLM Law Enforcement", "https://www.europol.europa.eu/publications-events/publications/chatgpt-impact-of-large-language-models-law-enforcement"),
    ("US FTC AI Impersonation Rule", "https://www.ftc.gov/news-events/news/press-releases/2024/02/ftc-proposes-new-protections-combat-ai-impersonation-government-business")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

verified = []
for name, url in candidate_urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            print(f"[200 OK] {name} -> {url}")
            verified.append((name, url, True))
    except Exception as e:
        print(f"[FAILED {e}] {name} -> {url}")
        verified.append((name, url, False))
    sys.stdout.flush()

print(f"\nVerified {sum(1 for v in verified if v[2])}/{len(verified)} URLs successfully!")
