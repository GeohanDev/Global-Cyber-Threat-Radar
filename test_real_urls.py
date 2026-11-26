# test_real_urls.py
import urllib.request

real_sources = [
    # Landmark Deepfake Heist ($25.6M)
    ("CNN Hong Kong Deepfake Heist", "https://edition.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk/index.html"),
    ("BBC Hong Kong Deepfake Scam", "https://www.bbc.com/news/world-asia-china-68196604"),
    ("Ars Technica Deepfake CFO", "https://arstechnica.com/information-technology/2024/02/deepfake-cfo-convinces-employee-to-transfer-25-million/"),
    
    # Morris II GenAI Worm (2024)
    ("Wired Morris II GenAI Worm", "https://www.wired.com/story/here-comes-the-first-generative-ai-worm/"),
    ("Dark Reading Morris II Worm", "https://www.darkreading.com/application-security/researchers-create-first-generative-ai-worm"),
    
    # Samsung Code Leak (2023)
    ("Bloomberg Samsung ChatGPT Ban", "https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak"),
    
    # Chevy $1 Car Jailbreak (2023)
    ("Business Insider Chevy Chatbot 1 Dollar", "https://www.businessinsider.com/chevy-dealership-ai-chatbot-tricked-selling-car-one-dollar-2023-12"),
    
    # WormGPT / Darknet LLMs (2023)
    ("BleepingComputer WormGPT", "https://www.bleepingcomputer.com/news/security/wormgpt-the-cybercrime-alternative-to-chatgpt-analyzed/"),
    
    # Hugging Face Backdoored Models (2024)
    ("BleepingComputer Hugging Face Malicious Models", "https://www.bleepingcomputer.com/news/security/hugging-face-finds-poisoned-models-that-steal-secrets-crypto/"),
    
    # Microsoft Copilot Studio Cross-Tenant flaw (2024)
    ("Dark Reading Copilot Studio Vulnerability", "https://www.darkreading.com/cloud-security/critical-microsoft-copilot-studio-vulnerability-cross-tenant-data"),
    
    # Microsoft Threat Intelligence on State Actors using AI (2024)
    ("Microsoft Security Threat Actors LLMs", "https://www.microsoft.com/en-us/security/blog/2024/02/14/staying-ahead-of-threat-actors-in-the-age-of-ai/"),
    
    # CISA & FBI Advisory on Deepfake Threats
    ("CISA Deepfake Threats", "https://www.cisa.gov/news-events/news/cisa-fbi-and-ms-isac-release-guide-synthetic-media-threats"),
    
    # MITRE ATLAS Official GitHub Repository
    ("MITRE ATLAS Official Repo", "https://github.com/mitre-atlas/atlas-data"),
    ("MITRE ATLAS Official Site", "https://atlas.mitre.org/")
]

for name, url in real_sources:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            print(f"[200 OK] {name} -> {url[:60]}...")
    except Exception as e:
        print(f"[FAILED {e}] {name} -> {url[:60]}...")
