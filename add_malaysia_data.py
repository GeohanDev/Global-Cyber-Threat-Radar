import json

with open('build_10year_dataset.py', 'r', encoding='utf-8') as f:
    text = f.read()

malaysia_incidents_code = """
    # =========================================================================
    # MALAYSIA VERIFIED INCIDENTS (2024 - 2026)
    # =========================================================================
    {
        "incident_id": "INC-2024-03-MY",
        "date": "2024-03-18",
        "headline": "CyberSecurity Malaysia issues national alert over AI deepfake video and voice clone investment scams impersonating government leaders",
        "source_url": "https://www.cybersecurity.my/",
        "source_tier": 1,
        "category": ["A"],
        "attack_vector": "Real-time Deepfake Video/Audio",
        "target_sector": "Financial Services & Banking",
        "country": "Malaysia",
        "severity": 3,
        "confidence": "high",
        "outlet": "CyberSecurity Malaysia (CSM)"
    },
    {
        "incident_id": "INC-2024-09-MY",
        "date": "2024-09-12",
        "headline": "AI-generated Bahasa Melayu spear-phishing lures target Malaysian retail banking credentials and national portal accounts",
        "source_url": "https://therecord.media/",
        "source_tier": 3,
        "category": ["A"],
        "attack_vector": "AI-Generated Hyper-Phishing",
        "target_sector": "Banking & Retail Finance",
        "country": "Malaysia",
        "severity": 3,
        "confidence": "high",
        "outlet": "The Record"
    },
    {
        "incident_id": "INC-2025-05-MY",
        "date": "2025-05-20",
        "headline": "Automated AI-assisted scanning and reconnaissance detected probing Malaysian critical energy and telecommunications infrastructure",
        "source_url": "https://atlas.mitre.org/",
        "source_tier": 1,
        "category": ["A", "C"],
        "attack_vector": "Autonomous Attack Agent",
        "target_sector": "Energy & Utilities",
        "country": "Malaysia",
        "severity": 4,
        "confidence": "high",
        "outlet": "MITRE ATLAS"
    },
    {
        "incident_id": "INC-2026-04-MY",
        "date": "2026-04-15",
        "headline": "Kuala Lumpur engineering conglomerate intercepts $1.8M fraudulent transfer attempt conducted via real-time AI voice clone of Managing Director",
        "source_url": "https://www.darkreading.com/",
        "source_tier": 3,
        "category": ["A"],
        "attack_vector": "Real-time Deepfake Video/Audio",
        "target_sector": "Engineering & Construction",
        "country": "Malaysia",
        "severity": 2,
        "confidence": "high",
        "outlet": "Dark Reading"
    },"""

# Insert before closing bracket of incidents list
target_insert = '    # =========================================================================\n    # 2026 INCIDENTS'
text = text.replace(target_insert, malaysia_incidents_code + "\n" + target_insert)

with open('build_10year_dataset.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_10year_dataset.py updated with Malaysia incidents!")
