with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

target = """<div class="feed-controls">
          <input type="text" class="feed-search" id="incidentSearchInput" placeholder="Search incidents, CVEs, targets...">
        </div>
      </div>
      <div class="table-container">"""

replacement = """<div class="feed-controls">
          <input type="text" class="feed-search" id="incidentSearchInput" placeholder="Search incidents, CVEs, targets...">
        </div>
      </div>

      <!-- Famous AI Ecosystems Quick Filter Bar -->
      <div class="ecosystem-pills-bar" style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; padding: 8px 12px; background: var(--hud-box-bg); border: 1px solid var(--border-subtle); border-radius: 8px;">
        <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 4px;">Famous AI Ecosystems:</span>
        <button class="pill-btn active" onclick="window.filterByEcosystem('ALL')">All Cases</button>
        <button class="pill-btn" onclick="window.filterByEcosystem('Gemini')">✨ Google Gemini</button>
        <button class="pill-btn" onclick="window.filterByEcosystem('Anthropic')">🧠 Anthropic Claude</button>
        <button class="pill-btn" onclick="window.filterByEcosystem('Hugging Face')">🤗 Hugging Face</button>
        <button class="pill-btn" onclick="window.filterByEcosystem('OpenAI')">🤖 OpenAI / ChatGPT</button>
        <button class="pill-btn" onclick="window.filterByEcosystem('Copilot')">🪟 Microsoft Copilot</button>
        <button class="pill-btn" onclick="window.filterByEcosystem('NVIDIA')">⚡ NVIDIA</button>
        <button class="pill-btn" onclick="window.filterByEcosystem('Meta')">🦙 Meta Llama</button>
      </div>

      <div class="table-container">"""

if target in c:
    c = c.replace(target, replacement)
    print("Successfully inserted Famous AI Ecosystems Quick-Filter Bar!")
    with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(c)
else:
    print("Warning: Target string not found!")
