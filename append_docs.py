# append_docs.py
with open("DOCUMENTATION.md", "r", encoding="utf-8") as f:
    text = f.read()

appendix = """
---

## 10. Famous AI Ecosystems & Quick-Pill Telemetry Filter

### 10.1 High-Profile AI Ecosystem Incident Registry
The incident database now includes verified threat telemetry cases targeting major global AI enterprises and open-source ecosystems:
* **Google Gemini:** Prompt injection vulnerabilities in Gemini Advanced & Workspace integrations, rogue API tool manipulation.
* **Anthropic Claude:** Indirect prompt injection via system artifact parsing and jailbreak bypass vectors.
* **Hugging Face:** Malicious pickled model checkpoints, backdoored weights, and safetensors deserialization exploits.
* **OpenAI / ChatGPT:** Custom GPT actions SSRF, data exfiltration via rogue plugin endpoints, and account takeover vectors.
* **Microsoft Copilot:** Prompt injection across Microsoft 365 tenant boundary, cross-tenant file extraction via autonomous search indexing.
* **NVIDIA:** Vulnerabilities in Triton Inference Server, NeMo framework memory corruption, and GPU container privilege escalation.
* **Meta Llama:** Direct weights tampering, untrusted fine-tuning dataset poisoning, and distributed parameter inversion attacks.

### 10.2 Sleek SOC Quick-Pill Design & Architecture
* **Visual Styling:** Rounded pill elements (`border-radius: 20px`, `padding: 6px 14px`) with soft drop shadows and clean borders replacing unstyled HTML browser buttons.
* **Reactive Active State:** Glowing electric blue fill (`#2563eb`) with elevated contrast (`#ffffff` text) and soft shadow glow (`box-shadow: 0 2px 10px rgba(37, 99, 235, 0.35)`).
* **Branded Dynamic Accents:** Per-ecosystem hover color accents (Gemini Blue, Anthropic Amber, Hugging Face Orange, OpenAI Teal, Copilot Azure, NVIDIA Lime, Meta Violet).
* **Dual-Filter Synchronization:** Two-way sync between the Universal Filter Bar dropdown (`#filterEntity`) and the quick-pill button deck (`.ecosystem-pills-bar`).
"""

if "## 10. Famous AI Ecosystems" not in text:
    with open("DOCUMENTATION.md", "w", encoding="utf-8") as f:
        f.write(text + appendix)
    print("DOCUMENTATION.md updated.")
else:
    print("Already in DOCUMENTATION.md")
