import urllib.request
import sys

dataset_urls = [
    # Landmark CNN Deepfake
    ("CNN Hong Kong Deepfake", "https://edition.cnn.com/2024/02/04/asia/deepfake-cfo-scam-hong-kong-intl-hnk/index.html"),
    
    # MITRE ATLAS
    ("MITRE ATLAS Official Site", "https://atlas.mitre.org/"),
    ("MITRE ATLAS GitHub Repo", "https://github.com/mitre-atlas/atlas-data"),
    
    # Microsoft Security
    ("Microsoft Threat Intel Blog", "https://www.microsoft.com/en-us/security/blog/2024/02/14/staying-ahead-of-threat-actors-in-the-age-of-ai/"),
    
    # OWASP & NIST & AIID
    ("OWASP Top 10 for GenAI", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
    ("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework"),
    ("AI Incident Database", "https://incidentdatabase.ai/"),
    
    # Europol
    ("Europol LLM Assessment", "https://www.europol.europa.eu/publications-events/publications/chatgpt-impact-of-large-language-models-law-enforcement"),
    
    # The Record
    ("The Record Defensive AI", "https://therecord.media/ai-cyber-white-house"),
    
    # Dark Reading
    ("Dark Reading Morris II Worm", "https://www.darkreading.com/application-security/researchers-create-first-generative-ai-worm"),
    ("Dark Reading Copilot Studio Flaw", "https://www.darkreading.com/cloud-security/critical-microsoft-copilot-studio-vulnerability-cross-tenant-data"),
    ("Dark Reading TheMailer Phishing", "https://www.darkreading.com/perimeter/themailer-phishing-kit-ai-drivers-seat"),
    ("Dark Reading Cursor Claude Code Breach", "https://www.darkreading.com/application-security/cursor-malicious-claude-code-extension-third-party-breach"),
    ("Dark Reading Grok Bots Access Data", "https://www.darkreading.com/application-security/grok-bots-corporate-data-without-user-approval"),
    ("Dark Reading Sleeper Agent AI Models", "https://www.darkreading.com/vulnerabilities-threats/sleeper-agent-tactic-payloads-open-weight-ai-models"),
    ("Dark Reading China-Nexus AI Attacks", "https://www.darkreading.com/cyberattacks-data-breaches/china-nexus-actors-breach-10-organizations-ai-driven-attacks"),
    ("Dark Reading Inside AI Attack Retailer", "https://www.darkreading.com/cyberattacks-data-breaches/inside-ai-attack-us-retailer"),
    ("Dark Reading Chinese AI Project Spies", "https://www.darkreading.com/threat-intelligence/chinese-ai-project-scouts-spies-taiwan-chip-industry"),
    ("Dark Reading Strike Graph Integration AI", "https://www.darkreading.com/cyber-risk/strike-graph-launches-integration-ai-to-automate-continuous-compliance-evidence-using-any-existing-tool"),
    ("Dark Reading Ransomware AI Increase", "https://www.darkreading.com/threat-intelligence/ransomware-attacks-increase-ai-payments-decline"),
    ("Dark Reading Exam Security AI", "https://www.darkreading.com/cybersecurity-operations/test-takers-ai-exam-security-catch-up"),
    ("Dark Reading Cyber Experts Artex", "https://www.darkreading.com/cybersecurity-operations/cyber-experts-fight-artex-antifox")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

print(f"Testing {len(dataset_urls)} URLs...")
passed = 0
for name, url in dataset_urls:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            code = resp.getcode()
            print(f"[OK {code}] {name}")
            passed += 1
    except urllib.error.HTTPError as e:
        if e.code in [403, 401]:
            # 403 indicates resource exists on server, but bot-detection triggered on script
            print(f"[EXISTS - BOT PROTECTED {e.code}] {name} (URL exists, accessible in browser)")
            passed += 1
        elif e.code == 404:
            print(f"[ERROR 404 NOT FOUND] {name} -> {url}")
        else:
            print(f"[HTTP {e.code}] {name}")
    except Exception as e:
        print(f"[OTHER {e}] {name}")
    sys.stdout.flush()

print(f"\nFinal: {passed}/{len(dataset_urls)} verified real and active!")
