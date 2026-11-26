# patch_cyberattack_focus.py

with open("generate_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Section Title
old_title = '<span>Reported Articles Feed (What Was Reported)</span>'
new_title = '<span>Reported Articles Feed (Verified Cyberattack & Threat Dispatches)</span>'
assert old_title in code, "Failed to find old_title"
code = code.replace(old_title, new_title, 1)

# 2. Update pillsField labels to emphasize cyberattack & threat intelligence
old_pills = """      <!-- Tech Domain & Field Quick-Filter Bar -->
      <div class="card-pills-row" id="pillsField" style="margin-bottom: 8px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start; flex-wrap: wrap;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>🌐</span> Tech Field:
        </span>
        <button class="pill-btn active" data-field="ALL" onclick="window.filterByField('ALL')">All Fields (1,200+)</button>
        <button class="pill-btn" data-field="ai" onclick="window.filterByField('ai')">🤖 AI & Frontier LLMs</button>
        <button class="pill-btn" data-field="cyber" onclick="window.filterByField('cyber')">🛡️ Cybersecurity & CTI</button>
        <button class="pill-btn" data-field="hardware" onclick="window.filterByField('hardware')">💻 Computer Hardware & Chips</button>
        <button class="pill-btn" data-field="it" onclick="window.filterByField('it')">☁️ Enterprise IT & Cloud</button>
      </div>"""

new_pills = """      <!-- Threat Intelligence Vector & Domain Bar -->
      <div class="card-pills-row" id="pillsField" style="margin-bottom: 8px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start; flex-wrap: wrap;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>🛡️</span> Threat Vector:
        </span>
        <button class="pill-btn active" data-field="ALL" onclick="window.filterByField('ALL')">All Cyber Threats (550+)</button>
        <button class="pill-btn" data-field="cyber" onclick="window.filterByField('cyber')">🚨 Breaches, Ransomware & CTI</button>
        <button class="pill-btn" data-field="ai" onclick="window.filterByField('ai')">🤖 AI Cyberattacks & Jailbreaks</button>
        <button class="pill-btn" data-field="hardware" onclick="window.filterByField('hardware')">💻 Hardware & Chip Exploits</button>
        <button class="pill-btn" data-field="it" onclick="window.filterByField('it')">☁️ Cloud & Critical Infrastructure</button>
      </div>"""

assert old_pills in code, "Failed to find old_pills"
code = code.replace(old_pills, new_pills, 1)

# 3. Update field badges rendering in renderArticlesFeed
old_card_field = """          const fieldIcon = art.field === 'ai' ? '🤖 AI' :
                            art.field === 'cyber' ? '🛡️ Cyber' :
                            art.field === 'hardware' ? '💻 Hardware' :
                            art.field === 'it' ? '☁️ IT / Cloud' : '🌐 Tech';"""

new_card_field = """          const fieldIcon = art.field === 'ai' ? '🤖 AI Threat' :
                            art.field === 'cyber' ? '🚨 Breach/CTI' :
                            art.field === 'hardware' ? '💻 Chip Exploit' :
                            art.field === 'it' ? '☁️ Infra Outage' : '🛡️ Cyber';"""

assert old_card_field in code, "Failed to find old_card_field"
code = code.replace(old_card_field, new_card_field, 1)

with open("generate_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

print("generate_dashboard.py updated with cyberattack focus!")
