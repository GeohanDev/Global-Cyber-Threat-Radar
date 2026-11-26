import urllib.request

urls = [
    ("CNN Hong Kong Deepfake", "https://edition.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk/index.html"),
    ("Dark Reading Morris II Worm", "https://www.darkreading.com/application-security/researchers-create-first-generative-ai-worm"),
    ("Microsoft Threat Intel AI", "https://www.microsoft.com/en-us/security/blog/2024/02/14/staying-ahead-of-threat-actors-in-the-age-of-ai/"),
    ("Dark Reading Copilot Studio Flaw", "https://www.darkreading.com/cloud-security/critical-microsoft-copilot-studio-vulnerability-cross-tenant-data"),
    ("Dark Reading TheMailer AI Phishing", "https://www.darkreading.com/perimeter/themailer-phishing-kit-ai-drivers-seat"),
    ("Dark Reading Cursor Claude Code Breach", "https://www.darkreading.com/application-security/cursor-malicious-claude-code-extension-third-party-breach"),
    ("Dark Reading Grok Bots Access Data", "https://www.darkreading.com/application-security/grok-bots-corporate-data-without-user-approval"),
    ("Dark Reading Sleeper Agent AI Models", "https://www.darkreading.com/vulnerabilities-threats/sleeper-agent-tactic-payloads-open-weight-ai-models"),
    ("Dark Reading China-Nexus AI Attacks", "https://www.darkreading.com/cyberattacks-data-breaches/china-nexus-actors-breach-10-organizations-ai-driven-attacks"),
    ("Dark Reading ArcticRAT AI Profiling", "https://www.darkreading.com/mobile-security/arcticrat-cybercrime-gang-profiles-victim-finances-ai"),
    ("Dark Reading Inside AI Attack Retailer", "https://www.darkreading.com/cyberattacks-data-breaches/inside-ai-attack-us-retailer"),
    ("The Record Lawmakers AI Cyber", "https://therecord.media/ai-cyber-white-house"),
    ("MITRE ATLAS Official Site", "https://atlas.mitre.org/"),
    ("MITRE ATLAS GitHub Repo", "https://github.com/mitre-atlas/atlas-data")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

results = []
for name, url in urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            code = resp.getcode()
            print(f"[{code} OK] {name} -> {url}")
            results.append((name, url, True))
    except Exception as e:
        print(f"[FAIL] {name} -> {url}: {e}")
        results.append((name, url, False))

print(f"\nTested {len(results)} URLs, passed: {sum(1 for r in results if r[2])}/{len(results)}")
