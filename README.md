# 🛡️ Global AI Cyberattack Threat Radar (2017–2026+)
### Real-Time Executive Cyber Threat Intelligence (CTI) & SOC Observability Dashboard

[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-10b981?style=for-the-badge)](http://localhost:8080)
[![Classification: TLP:CLEAR](https://img.shields.io/badge/Classification-TLP%3ACLEAR-38bdf8?style=for-the-badge)](#)
[![Telemetry: Live Stream Active](https://img.shields.io/badge/Telemetry-Live%20Stream%20Active-10b981?style=for-the-badge)](http://localhost:8080)
[![Framework: MITRE ATLAS](https://img.shields.io/badge/Framework-MITRE%20ATLAS%20aligned-f59e0b?style=for-the-badge)](#)

---

## 📋 Overview

The **Global AI Cyberattack Threat Radar** is an enterprise-grade Security Operations Center (SOC) dashboard that delivers unified visibility into the global AI threat landscape spanning **2017 through 2026 and forward**.

It tracks real-time adversarial operations, automated vulnerability weaponization, model extraction, and agentic compromises across Fortune 500 enterprises, frontier AI labs, and regional infrastructures (including specialized **Malaysia Threat Telemetry**).

---

## ⚡ Core Capabilities

### 1. 🌐 Continuous Live Threat Intelligence Stream
* **Automated Multi-Source Broadcast Ingestion:** Background harvesting daemon continuously pulls live AI and cyber threat intelligence dispatches from mainstream global broadcasters (**BBC News, CNN, Reuters, Bloomberg, The Guardian, CNBC, TechCrunch, Wired**) alongside specialized CTI feeds (The Record, Dark Reading, SecurityWeek, The Hacker News, Krebs on Security, and NCSC UK).
* **Zero External API Cost:** Runs entirely via local Python XML/HTML parsers—no paid news API keys, third-party subscriptions, or quota rate limits required.
* **Auto-Sweep Cycle:** Automatically refreshes dispatches on an adaptive countdown timer with optional manual **`⚡ Sync Now`** trigger.

### 2. 📈 10-Year Macro Horizon & Cumulative Surge Trajectory
* **Macro Horizon (2017–2026+):** Complete historical record from early adversarial ML attacks (2017–2021) to generative AI weaponization (2022–2024) and autonomous agentic compromises (2025–2026+).
* **Cumulative Threat Surge (Exponential S-Curve):** Replaces sparse rolling views with cumulative velocity analytics tracking total breach volume and category surges.
* **Milestone Benchmark Table:** Year-by-year SOC operational checkpoints highlighting critical historical turning points.

### 3. 🎯 Famous AI Ecosystem Tracking
Dedicated monitoring and single-click quick-filtering for leading frontier AI environments:
* ✨ **Google Gemini:** Workspace integration prompt injections, multimodal exfiltration vectors.
* 🧠 **Anthropic Claude:** Artifact parser jailbreaks, indirect prompt injection risks.
* 🤗 **Hugging Face:** Malicious serialized model checkpoints, backdoored weights, PyTorch/safetensors exploits.
* 🤖 **OpenAI / ChatGPT:** Custom GPT server-side request forgery (SSRF), rogue plugin exfiltration.
* 🪟 **Microsoft Copilot:** Cross-tenant search boundary extraction, Office 365 indexing manipulation.
* ⚡ **NVIDIA:** GPU container privilege escalation, NeMo memory corruptions, Triton inference exploits.
* 🦙 **Meta Llama:** Direct open weights tampering, dataset poisoning, parameter inversion.

### 4. 📊 3-Card Advanced Visual Deck & Explicit Filter Controls
Each visualization card includes dedicated executive analytical context AND explicit interactive quick-filter button decks (eliminating the need to click tiny canvas slices):
* **Scope Category Quick Pills:** Single-click toggle between All Categories, Cat A (Using AI), Cat B (On AI Systems), and Cat C (Agentic Attacks).
* **MITRE ATLAS Vector Pills:** Instant filtering by Prompt Injection, Rogue MCP / Tool Poisoning, Supply Chain, and Evasion tactics.
* **Severity Profile Pills:** Color-coded severity tiers from Sev 1 (PoC) to Sev 5 (Critical Breach).
* **Active Filters Ribbon:** Dynamic notification strip displaying all active criteria tags with dismissal ✕ buttons and filtered volume telemetry.
Each visualization card includes dedicated executive analytical context:
1. **Scope Category Distribution (Doughnut):** Structural breakdown across *Category A (Using AI)*, *Category B (On AI Systems)*, and *Category C (Agentic Attacks)*.
2. **MITRE ATLAS Vector Radar:** Multi-axial tactical footprint covering Reconnaissance, Prompt Injection, Evasion, Exfiltration, Supply Chain, and Tool Poisoning.
3. **Severity & Impact Velocity (Polar Area):** Granular distribution from Sev-1 (Informational) through Sev-5 (Catastrophic Enterprise Breach).

### 5. 🇲🇾 Dedicated Malaysia Regional Telemetry
* Monitored threats spanning critical infrastructure, banking & payment systems (PayNet/DuitNow), government portals (MySejahtera/MyDigital ID), telecommunications, and cloud data centers in Cyberjaya and Johor.

### 6. 📄 Automated Executive PDF Briefing Export
* Click **`📥 Export PDF`** to generate a multi-page, publication-grade executive intelligence report (`Global_AI_Cyberattack_Threat_Report.pdf`) with executive KPI summaries, taxonomy methodology, and complete incident registries.

### 7. ⏱️ Livetime Telemetry Engine
* Centered dual digital clock with ticking UTC telemetry and local time.
* Real-time session uptime counter and live status indicator (`🟢 Live Telemetry Active`).

---

## 📂 Project Structure

```
├── server.py                        # Multithreaded Python HTTP/CTI server & scraper daemon
├── soup_harvester.py                # Live RSS/Atom/XML feed parsing engine
├── generate_dashboard.py            # Primary dashboard compiler & template engine
├── build_5year_dataset.py           # Canonical baseline threat dataset & taxonomy
├── pdf_generator.py                 # Pure Python executive PDF briefing generator
├── convert_doc_to_word.py           # Documentation DOCX generator (python-docx)
├── index.html                       # Compiled production dashboard (self-contained)
├── incidents.json                   # Structured incident database snapshot
├── Global_AI_Cyberattack_Threat_Report.pdf # Generated executive threat report
├── DOCUMENTATION.docx               # Comprehensive Word briefing documentation
├── DOCUMENTATION.md                 # Full markdown architectural reference
└── README.md                        # Quick-start guide & repository overview
```

---

## 🚀 Quick Start Guide

### Prerequisites
* Python 3.10 or higher
* Recommended libraries: `beautifulsoup4`, `lxml`, `python-docx` (optional for docx generation)

```powershell
pip install beautifulsoup4 lxml python-docx
```

### 1. Launch the Live Telemetry Server
Run the background server which hosts the dashboard, runs the automated live threat scraper daemon, and handles PDF generation endpoints:

```powershell
python server.py
```

Open your browser and navigate to:
👉 **`http://localhost:8080`**

### 2. Re-compile the Dashboard (Optional)
If you update `incidents.json` or customize the HTML/CSS/JS template:

```powershell
python generate_dashboard.py
```
This re-compiles `index.html` with all charts, datasets, and styling bundled.

### 3. Export Executive Reports
* **Via Web Dashboard:** Click **`📥 Export PDF`** in the top navigation bar.
* **Via CLI:**
  ```powershell
  python -c "import pdf_generator; pdf_data = pdf_generator.generate_threat_radar_pdf(); open('Global_AI_Cyberattack_Threat_Report.pdf', 'wb').write(pdf_data)"
  ```
* **Generate Word Documentation:**
  ```powershell
  python convert_doc_to_word.py
  ```

---

## 🔌 API Endpoints

The integrated `server.py` exposes lightweight JSON and binary endpoints:

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/live-feed` | `GET` | Returns freshly ingested live threat dispatches from global CTI feeds. |
| `/api/export-pdf` | `GET` | Streams the compiled, multi-page executive PDF threat report directly to the client. |

---

## 🛡️ Threat Classification Taxonomy

Incidents are classified in compliance with **MITRE ATLAS** and the **EU AI Act / NIST AI RMF**:

* **Category A: Attacks USING AI (Offensive AI Weaponization)**  
  Adversaries deploying AI for polymorphic malware generation, deepfake voice cloning, automated vulnerability discovery, and AI-driven spear-phishing.
* **Category B: Attacks ON AI Systems (Adversarial ML & Infrastructure)**  
  Direct exploits against AI models, training pipelines, and inference runtimes: direct prompt injection, training dataset poisoning, model theft, and pickled checkpoint deserialization.
* **Category C: Autonomous Agentic Attacks (Agent Compromise)**  
  Exploitations targeting multi-step autonomous AI agents: Model Context Protocol (MCP) tool poisoning, indirect prompt injection across tenant boundaries, and unauthorized autonomous tool execution.

---

## 🎨 Themes & UI

The dashboard includes a real-time theme switcher in the top navigation bar:
* **Dark Mode (Default):** High-contrast SOC command room aesthetic (`#080c14` base palette).
* **Light Mode:** Executive presentation palette optimized for boardrooms and daylight viewing (`#f1f5f9` base palette).

---

## 📄 License & Attribution

* **Classification:** TLP:CLEAR (Public threat intelligence & research telemetry).
* **Framework Attribution:** Aligned with [MITRE ATLAS™](https://atlas.mitre.org/) and the [AI Incident Database](https://incidentdatabase.ai/).
