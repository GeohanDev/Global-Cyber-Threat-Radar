with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add .pill-btn CSS
old_hud_btn_css = """.hud-btn:hover {{
      border-color: var(--border-focus);
      color: var(--text-main);
    }}"""

new_pill_css = """.hud-btn:hover {{
      border-color: var(--border-focus);
      color: var(--text-main);
    }}

    .pill-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.72rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .pill-btn:hover {{
      border-color: var(--border-focus);
      color: var(--text-main);
    }}
    .pill-btn.active {{
      background: rgba(37, 99, 235, 0.15);
      border-color: #2563eb;
      color: #3b82f6;
    }}"""

if old_hud_btn_css in content:
    content = content.replace(old_hud_btn_css, new_pill_css)
    print("Added .pill-btn CSS")

# 2. Update the 3 visualization cards HTML to add descriptions below the titles
old_viz_deck = """    <!-- Multi-Dimensional Threat Intelligence Visualizations Deck -->
    <div class="grid-3col">
      <!-- 1. Scope Category Doughnut -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header">
          <div class="section-title">Scope Category Breakdown</div>
          <span style="font-size: 0.72rem; color: var(--text-dim);">Click slice to filter</span>
        </div>
        <div style="height: 230px; position: relative;">
          <canvas id="categoryDoughnutCanvas"></canvas>
        </div>
      </section>

      <!-- 2. MITRE ATLAS Vector Radar (Spider Chart) -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header">
          <div class="section-title">MITRE ATLAS Vector Radar</div>
          <span style="font-size: 0.72rem; color: var(--text-dim);">Threat density surface</span>
        </div>
        <div style="height: 230px; position: relative;">
          <canvas id="vectorRadarCanvas"></canvas>
        </div>
      </section>

      <!-- 3. Severity Impact Profile (Polar Area) -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header">
          <div class="section-title">Severity Impact Profile</div>
          <span style="font-size: 0.72rem; color: var(--text-dim);">Click petal to filter</span>
        </div>
        <div style="height: 230px; position: relative;">
          <canvas id="severityPolarCanvas"></canvas>
        </div>
      </section>
    </div>"""

new_viz_deck = """    <!-- Multi-Dimensional Threat Intelligence Visualizations Deck -->
    <div class="grid-3col">
      <!-- 1. Scope Category Doughnut -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header" style="flex-direction: column; align-items: flex-start; gap: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="section-title">Scope Category Breakdown</div>
            <span style="font-size: 0.72rem; color: var(--text-dim);">Click slice to filter</span>
          </div>
          <p style="font-size: 0.76rem; color: var(--text-muted); margin: 2px 0 0 0; line-height: 1.4;">
            Proportional distribution across core taxonomy: Cat A (Using AI), Cat B (Attacks On AI Systems), and Cat C (Agentic Attacks).
          </p>
        </div>
        <div style="height: 220px; position: relative; margin-top: 6px;">
          <canvas id="categoryDoughnutCanvas"></canvas>
        </div>
      </section>

      <!-- 2. MITRE ATLAS Vector Radar (Spider Chart) -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header" style="flex-direction: column; align-items: flex-start; gap: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="section-title">MITRE ATLAS Vector Radar</div>
            <span style="font-size: 0.72rem; color: var(--text-dim);">Threat density surface</span>
          </div>
          <p style="font-size: 0.76rem; color: var(--text-muted); margin: 2px 0 0 0; line-height: 1.4;">
            Multi-dimensional threat density mapping 6 core adversarial tactics from MITRE ATLAS (Prompt Injection, Rogue MCP, Supply Chain, Evasion, Deepfake, and Recon).
          </p>
        </div>
        <div style="height: 220px; position: relative; margin-top: 6px;">
          <canvas id="vectorRadarCanvas"></canvas>
        </div>
      </section>

      <!-- 3. Severity Impact Profile (Polar Area) -->
      <section class="section-card" style="margin-bottom: 0;">
        <div class="section-header" style="flex-direction: column; align-items: flex-start; gap: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="section-title">Severity Impact Profile</div>
            <span style="font-size: 0.72rem; color: var(--text-dim);">Click petal to filter</span>
          </div>
          <p style="font-size: 0.76rem; color: var(--text-muted); margin: 2px 0 0 0; line-height: 1.4;">
            Concentric radial spread across the 5 standard threat severity tiers, scaling from Sev 1 (Lab PoC) to Sev 5 (Systemic Infrastructure Breach).
          </p>
        </div>
        <div style="height: 220px; position: relative; margin-top: 6px;">
          <canvas id="severityPolarCanvas"></canvas>
        </div>
      </section>
    </div>"""

if old_viz_deck in content:
    content = content.replace(old_viz_deck, new_viz_deck)
    print("Updated 3 visualization cards with descriptions below the titles")
else:
    print("Warning: old_viz_deck not found exactly")

# 3. Add Famous AI Ecosystems Quick-Filter Bar above the Incident Table
old_table_header = """    <!-- 7. Incidents Table -->
    <section class="section-card">
      <div class="articles-feed-header">
        <div class="section-title">
          <span>De-duplicated Incident Registry (What Happened)</span>
          <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);" id="incidentCountBadge"></span>
        </div>
        <div class="feed-controls">
          <input type="text" class="feed-search" id="incidentSearchInput" placeholder="Search incidents, CVEs, targets...">
        </div>
      </div>
      <div class="table-container">"""

new_table_header = """    <!-- 7. Incidents Table -->
    <section class="section-card">
      <div class="articles-feed-header">
        <div class="section-title">
          <span>De-duplicated Incident Registry (What Happened)</span>
          <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);" id="incidentCountBadge"></span>
        </div>
        <div class="feed-controls">
          <input type="text" class="feed-search" id="incidentSearchInput" placeholder="Search incidents, CVEs, targets...">
        </div>
      </div>

      <!-- Famous AI Ecosystems Quick Filter Bar -->
      <div class="ecosystem-pills-bar" style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 12px; padding: 8px 12px; background: var(--hud-box-bg); border: 1px solid var(--border-subtle); border-radius: 8px;">
        <span style="font-size: 0.72rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 4px;">Famous Ecosystems:</span>
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

if old_table_header in content:
    content = content.replace(old_table_header, new_table_header)
    print("Added Famous AI Ecosystems Quick-Filter Bar")
else:
    print("Warning: old_table_header not found exactly")

# 4. Add window.filterByEcosystem in JavaScript
js_filter_function = """      window.filterByEcosystem = function(eco) {{
        const searchInput = document.getElementById('incidentSearchInput');
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
        
        if (eco === 'ALL') {{
          if (searchInput) searchInput.value = '';
          activeFilters.incidentSearch = '';
        }} else {{
          if (searchInput) searchInput.value = eco;
          activeFilters.incidentSearch = eco;
        }}
        
        // Highlight active pill button
        if (event && event.target && event.target.classList.contains('pill-btn')) {{
          event.target.classList.add('active');
        }}
        
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterByVector = function(vec) {{"""

content = content.replace("      window.filterByVector = function(vec) {{", js_filter_function)

# 5. Make incidentSearchInput input event call updateDashboard()
content = content.replace(
    "document.getElementById('incidentSearchInput').addEventListener('input', e => {\n        activeFilters.incidentSearch = e.target.value;\n        renderIncidentsTable(getFilteredIncidents());\n      });",
    "document.getElementById('incidentSearchInput').addEventListener('input', e => {\n        activeFilters.incidentSearch = e.target.value;\n        updateDashboard();\n      });"
)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved generate_dashboard.py with famous cases and card descriptions.")
