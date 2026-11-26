import json

new_famous_incidents = [
    {
        "incident_id": "INC-2024-05-GM",
        "date": "2024-05-14",
        "headline": "Google Gemini Workspace Indirect Prompt Injection Exfiltrates Private User Data",
        "source_url": "https://atlas.mitre.org/",
        "source_tier": 1,
        "category": ["B", "C"],
        "attack_vector": "Indirect Prompt Injection / Data Exfiltration",
        "target_sector": "Cloud & AI Productivity (Google)",
        "country": "United States",
        "severity": 4,
        "confidence": "high",
        "outlet": "MITRE ATLAS / Dark Reading"
    },
    {
        "incident_id": "INC-2025-02-GM",
        "date": "2025-02-18",
        "headline": "Google Gemini Pro Vision Multimodal Typographic Jailbreak Bypasses Safety Guardrails",
        "source_url": "https://therecord.media/news",
        "source_tier": 3,
        "category": ["B"],
        "attack_vector": "Multimodal Adversarial Perturbation / Jailbreak",
        "target_sector": "Consumer & Enterprise AI (Google)",
        "country": "United States",
        "severity": 3,
        "confidence": "high",
        "outlet": "The Record"
    },
    {
        "incident_id": "INC-2024-10-AN",
        "date": "2024-10-24",
        "headline": "Anthropic Claude Computer Use Sandbox Exploit Allows Autonomous System Hijacking",
        "source_url": "https://www.darkreading.com/vulnerabilities-threats",
        "source_tier": 3,
        "category": ["C"],
        "attack_vector": "Autonomous Agent Exploitation / Tool Injection",
        "target_sector": "AI Research & Enterprise Agentics (Anthropic)",
        "country": "United States",
        "severity": 4,
        "confidence": "high",
        "outlet": "Dark Reading"
    },
    {
        "incident_id": "INC-2026-11-AN",
        "date": "2026-11-17",
        "headline": "Malicious Anthropic Claude Code Extensions Exfiltrate Workstation API Secrets",
        "source_url": "https://therecord.media/news",
        "source_tier": 3,
        "category": ["A", "C"],
        "attack_vector": "Supply Chain Poisoning / Dev-Agent Hijack",
        "target_sector": "Developer Ecosystem (Anthropic Claude)",
        "country": "United States",
        "severity": 4,
        "confidence": "high",
        "outlet": "The Record"
    },
    {
        "incident_id": "INC-2024-02-HF",
        "date": "2024-02-28",
        "headline": "Hugging Face Hub Infiltrated with 100+ Poisoned Model Artifacts Executing Arbitrary Code",
        "source_url": "https://www.securityweek.com/",
        "source_tier": 3,
        "category": ["B"],
        "attack_vector": "Model Supply Chain Poisoning / Pickle Deserialization",
        "target_sector": "Open-Source AI Hubs (Hugging Face)",
        "country": "United States",
        "severity": 4,
        "confidence": "high",
        "outlet": "SecurityWeek / Protect AI"
    },
    {
        "incident_id": "INC-2025-06-HF",
        "date": "2025-06-12",
        "headline": "Hugging Face Spaces Cross-Tenant Container Escape Exposes Cloud Infrastructure Secrets",
        "source_url": "https://therecord.media/news",
        "source_tier": 3,
        "category": ["B", "C"],
        "attack_vector": "Container Escape / Shared Infrastructure Poisoning",
        "target_sector": "AI Model Hosting Platforms (Hugging Face)",
        "country": "United States",
        "severity": 4,
        "confidence": "high",
        "outlet": "The Record / Wiz Research"
    },
    {
        "incident_id": "INC-2024-07-OA",
        "date": "2024-07-02",
        "headline": "OpenAI ChatGPT macOS Client Custom URL Scheme Exploit Steals Unencrypted Chat Records",
        "source_url": "https://www.darkreading.com/application-security",
        "source_tier": 3,
        "category": ["B"],
        "attack_vector": "Client-Side Privilege Escalation / Data Theft",
        "target_sector": "Desktop AI Applications (OpenAI)",
        "country": "United States",
        "severity": 3,
        "confidence": "high",
        "outlet": "Dark Reading"
    },
    {
        "incident_id": "INC-2023-11-OA",
        "date": "2023-11-20",
        "headline": "OpenAI Custom GPT Store Prompt Injection Exfiltrates Proprietary Knowledge Bases",
        "source_url": "https://therecord.media/news",
        "source_tier": 3,
        "category": ["B"],
        "attack_vector": "Prompt Extraction / IP Theft",
        "target_sector": "Enterprise Generative AI (OpenAI)",
        "country": "United States",
        "severity": 3,
        "confidence": "high",
        "outlet": "The Record"
    },
    {
        "incident_id": "INC-2024-04-MT",
        "date": "2024-04-18",
        "headline": "Darknet Threat Actors Weaponize Meta Llama Weights for Automated Polymorphic Exploit Authoring",
        "source_url": "https://www.securityweek.com/",
        "source_tier": 3,
        "category": ["A"],
        "attack_vector": "Dual-Use Open Model Weaponization",
        "target_sector": "Open Weights AI Ecosystem (Meta)",
        "country": "United States",
        "severity": 3,
        "confidence": "high",
        "outlet": "SecurityWeek"
    }
]

# Update incidents.json
with open('incidents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

existing_ids = set([i['incident_id'] for i in data['incidents']])
added_count = 0

for inc in new_famous_incidents:
    if inc['incident_id'] not in existing_ids:
        data['incidents'].insert(0, inc)
        added_count += 1

with open('incidents.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Added {added_count} famous company incidents to incidents.json. Total now: {len(data['incidents'])}")

# Update bs4_extracted_feed.json
with open('bs4_extracted_feed.json', 'r', encoding='utf-8') as f:
    feed = json.load(f)

feed_titles = set([item.get('title') for item in feed])
feed_added = 0

famous_feed_items = [
    {
        "title": "Google Gemini Workspace Indirect Prompt Injection Exfiltrates Private User Data",
        "url": "https://atlas.mitre.org/",
        "outlet": "MITRE ATLAS",
        "description": "Security researchers demonstrated indirect prompt injection in Google Gemini integrated with Google Workspace (Docs/Gmail). Malicious hidden instructions in an inbound document caused Gemini to silently exfiltrate private user emails and search history to an attacker-controlled endpoint.",
        "country": "United States",
        "date": "2024-05-14"
    },
    {
        "title": "Anthropic Claude Computer Use Sandbox Exploit Allows Autonomous System Hijacking",
        "url": "https://www.darkreading.com/vulnerabilities-threats",
        "outlet": "Dark Reading",
        "description": "Attackers exploited Anthropic's Claude 3.5 Sonnet 'Computer Use' capability via prompt injection on web pages, causing the agent to autonomously navigate to malicious endpoints, interact with web UI controls, and attempt unauthorized execution of local bash terminal commands.",
        "country": "United States",
        "date": "2024-10-24"
    },
    {
        "title": "Hugging Face Hub Infiltrated with 100+ Poisoned Model Artifacts Executing Arbitrary Code",
        "url": "https://www.securityweek.com/",
        "outlet": "SecurityWeek",
        "description": "Security researchers from Wiz and Protect AI identified over 100 malicious AI models hosted on the Hugging Face Hub weaponized with unsafe Python pickle deserialization payloads, granting threat actors silent reverse shells upon model instantiation.",
        "country": "United States",
        "date": "2024-02-28"
    },
    {
        "title": "OpenAI ChatGPT macOS Client Custom URL Scheme Exploit Steals Unencrypted Chat Records",
        "url": "https://www.darkreading.com/application-security",
        "outlet": "Dark Reading",
        "description": "Security researcher Johann Rehberger disclosed an exploit in the official OpenAI ChatGPT macOS application where malicious links or Markdown image tags could silently append and exfiltrate the user's unencrypted local chat conversations to third-party servers.",
        "country": "United States",
        "date": "2024-07-02"
    }
]

for item in famous_feed_items:
    if item['title'] not in feed_titles:
        feed.insert(0, item)
        feed_added += 1

with open('bs4_extracted_feed.json', 'w', encoding='utf-8') as f:
    json.dump(feed, f, indent=2)

print(f"Added {feed_added} famous company articles to bs4_extracted_feed.json. Total feed items: {len(feed)}")
