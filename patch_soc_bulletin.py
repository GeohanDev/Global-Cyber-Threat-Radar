import re

with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update title
content = content.replace(
    '<title>Global AI Cyberattack Threat Radar (5-Year & Continuous)</title>',
    '<title>Global AI Cyberattack Threat Radar (10-Year Macro & Continuous)</title>'
)

# 2. Update ticker-track CSS min-width: 0
content = content.replace(
    """.ticker-track {{
      flex: 1;
      overflow: hidden;
      position: relative;
      white-space: nowrap;
      mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
      -webkit-mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
    }}""",
    """.ticker-track {{
      flex: 1;
      min-width: 0;
      overflow: hidden;
      position: relative;
      white-space: nowrap;
      mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
      -webkit-mask-image: linear-gradient(to right, transparent, black 16px, black calc(100% - 16px), transparent);
    }}"""
)

# 3. Update KPI subtext
content = content.replace(
    '<span class="kpi-subtext" id="kpiHorizonSub">5-Year baseline volume</span>',
    '<span class="kpi-subtext" id="kpiHorizonSub">10-Year Macro baseline volume</span>'
)

# 4. Update SOC Bulletin Header in HTML
content = content.replace(
    '<h2 class="concerns-title">5-Year Threat Evolution & Current Findings</h2>',
    '<h2 class="concerns-title" id="socBulletinTitle">10-Year Threat Evolution & Current Findings</h2>'
)

# 5. Update Annual Button initial text
content = content.replace(
    '<button class="toggle-btn active" id="btnViewAnnual">5-Year View (By Year)</button>',
    '<button class="toggle-btn active" id="btnViewAnnual">10-Year View (By Year)</button>'
)

# 6. Update Methodology Footer
content = content.replace(
    '<h3>5-Year Architecture, Forward-Continuity & Source Observability</h3>',
    '<h3>10-Year Macro Architecture, Forward-Continuity & Source Observability</h3>'
)
content = content.replace(
    '<p style="margin-top: 6px;"><strong>5-Year Macro Evolutionary Shifts:</strong> 2022 Proof-of-concept injection → 2023 Darknet LLMs & Jailbreaks → 2024 Deepfake wire fraud & GenAI worms → 2025/2026 Autonomous agent loop hijacking, rogue MCP servers & SCADA bridge disruption.</p>',
    '<p style="margin-top: 6px;"><strong>10-Year Macro Evolutionary Shifts:</strong> 2017 Deepfake PoCs & AV Evasion → 2022 LLM Prompt Injections → 2023 Darknet LLMs & Jailbreaks → 2024 Deepfake wire fraud & GenAI worms → 2025/2026 Autonomous agent loop hijacking, rogue MCP servers & SCADA bridge disruption.</p>'
)

# 7. Update renderKeyConcerns in JS
old_concerns_fn = """      function renderKeyConcerns(filtered) {{
        const list = document.getElementById('concernsList');
        list.innerHTML = '';

        if (filtered.length === 0) {{
          list.innerHTML = '<li class="concern-item">No incidents match current filter selection.</li>';
          return;
        }}

        const yearCounts = {{}};
        filtered.forEach(i => {{
          const yr = i.date.substring(0, 4);
          yearCounts[yr] = (yearCounts[yr] || 0) + 1;
        }});
        const yearsPresent = Object.keys(yearCounts).sort();
        const firstYr = yearsPresent[0];
        const lastYr = yearsPresent[yearsPresent.length - 1];
        const firstCnt = yearCounts[firstYr] || 1;
        const lastCnt = yearCounts[lastYr] || 1;
        const growthMultiple = (lastCnt / firstCnt).toFixed(1);

        const li1 = document.createElement('li');
        li1.className = 'concern-item';
        li1.innerHTML = `<strong>5-Year Threat Escalation:</strong> AI-related cyberattacks have increased <strong>${{growthMultiple}}x</strong> from ${{firstYr}} (${{firstCnt}} incidents) to ${{lastYr}} (${{lastCnt}} incidents), driven by autonomous agents and multimodal generative tools.`;
        list.appendChild(li1);

        const maxSev = Math.max(...filtered.map(i => i.severity));
        const topInc = filtered.find(i => i.severity === maxSev);
        if (topInc) {{
          const li2 = document.createElement('li');
          li2.className = 'concern-item';
          li2.innerHTML = `<strong>Peak Severity Breach:</strong> <a onclick="window.highlightIncident('${{topInc.incident_id}}')">[${{topInc.incident_id}}] ${{topInc.headline}}</a> (Severity ${{topInc.severity}} - ${{topInc.target_sector}}, ${{topInc.country}}).`;
          list.appendChild(li2);
        }}

        const sectorCounts = {{}};
        filtered.forEach(i => sectorCounts[i.target_sector] = (sectorCounts[i.target_sector] || 0) + 1);
        let topSector = 'Financial Services';
        let topSecCount = 0;
        for (const [s, c] of Object.entries(sectorCounts)) {{
          if (c > topSecCount) {{
            topSecCount = c;
            topSector = s;
          }}
        }}

        const li3 = document.createElement('li');
        li3.className = 'concern-item';
        li3.innerHTML = `<strong>Dominant 5-Year Target Sector:</strong> <a onclick="window.filterBySector('${{topSector}}')">${{topSector}}</a> (${{topSecCount}} incidents), suffering systemic wire transfers, deepfake CFO impersonation, and trading-agent exploitation.`;
        list.appendChild(li3);

        const agenticIncs = filtered.filter(i => i.category.includes('C'));
        const li4 = document.createElement('li');
        li4.className = 'concern-item';
        li4.innerHTML = `<strong>Autonomous Agent Exploits (Cat C):</strong> Surged from 0 cases in 2022 to ${{agenticIncs.length}} total cases, led by <a onclick="window.filterByVector('Rogue MCP Server / Tool Poisoning')">Rogue MCP tool injection</a> and cross-agent context worms.`;
        list.appendChild(li4);

        const li5 = document.createElement('li');
        li5.className = 'concern-item';
        li5.innerHTML = `<strong>Forward Continuity:</strong> Ingestion engine automatically active for ${{maxDataYear + 1}}+ incidents via live feed sync or <a onclick="document.getElementById('logIncidentModal').style.display='flex'">+ Log Incident</a> button.`;
        list.appendChild(li5);
      }}"""

new_concerns_fn = """      function renderKeyConcerns(filtered) {{
        const list = document.getElementById('concernsList');
        list.innerHTML = '';

        // Dynamic Horizon Label for SOC Bulletin
        let horizonPrefix = '10-Year';
        if (activeFilters.horizon === '5Y') {{
          horizonPrefix = '5-Year';
        }} else if (activeFilters.horizon === '12M') {{
          horizonPrefix = '12-Month';
        }} else if (activeFilters.horizon === 'ALL') {{
          horizonPrefix = 'All-Time Continuous';
        }} else if (activeFilters.horizon === '10Y') {{
          horizonPrefix = '10-Year';
        }} else {{
          horizonPrefix = `Year ${{activeFilters.horizon}}`;
        }}

        const bulletinTitle = document.getElementById('socBulletinTitle');
        if (bulletinTitle) {{
          bulletinTitle.textContent = `${{horizonPrefix}} Threat Evolution & Current Findings`;
        }}

        if (filtered.length === 0) {{
          list.innerHTML = '<li class="concern-item">No incidents match current filter selection.</li>';
          return;
        }}

        const yearCounts = {{}};
        filtered.forEach(i => {{
          const yr = i.date.substring(0, 4);
          yearCounts[yr] = (yearCounts[yr] || 0) + 1;
        }});
        const yearsPresent = Object.keys(yearCounts).sort();
        const firstYr = yearsPresent[0];
        const lastYr = yearsPresent[yearsPresent.length - 1];
        const firstCnt = yearCounts[firstYr] || 1;
        const lastCnt = yearCounts[lastYr] || 1;
        const growthMultiple = (lastCnt / firstCnt).toFixed(1);

        const li1 = document.createElement('li');
        li1.className = 'concern-item';
        li1.innerHTML = `<strong>${{horizonPrefix}} Threat Escalation:</strong> AI-related cyberattacks have increased <strong>${{growthMultiple}}x</strong> from ${{firstYr}} (${{firstCnt}} incidents) to ${{lastYr}} (${{lastCnt}} incidents), driven by autonomous agents and multimodal generative tools.`;
        list.appendChild(li1);

        const maxSev = Math.max(...filtered.map(i => i.severity));
        const topInc = filtered.find(i => i.severity === maxSev);
        if (topInc) {{
          const li2 = document.createElement('li');
          li2.className = 'concern-item';
          li2.innerHTML = `<strong>Peak Severity Breach:</strong> <a onclick="window.highlightIncident('${{topInc.incident_id}}')">[${{topInc.incident_id}}] ${{topInc.headline}}</a> (Severity ${{topInc.severity}} - ${{topInc.target_sector}}, ${{topInc.country}}).`;
          list.appendChild(li2);
        }}

        const sectorCounts = {{}};
        filtered.forEach(i => sectorCounts[i.target_sector] = (sectorCounts[i.target_sector] || 0) + 1);
        let topSector = 'Financial Services';
        let topSecCount = 0;
        for (const [s, c] of Object.entries(sectorCounts)) {{
          if (c > topSecCount) {{
            topSecCount = c;
            topSector = s;
          }}
        }}

        const li3 = document.createElement('li');
        li3.className = 'concern-item';
        li3.innerHTML = `<strong>Dominant ${{horizonPrefix}} Target Sector:</strong> <a onclick="window.filterBySector('${{topSector}}')">${{topSector}}</a> (${{topSecCount}} incidents), suffering systemic wire transfers, deepfake CFO impersonation, and trading-agent exploitation.`;
        list.appendChild(li3);

        const agenticIncs = filtered.filter(i => i.category.includes('C'));
        const li4 = document.createElement('li');
        li4.className = 'concern-item';
        const startYrBaseline = firstYr || 2017;
        li4.innerHTML = `<strong>Autonomous Agent Exploits (Cat C):</strong> Surged from ${{yearCounts[startYrBaseline] || 0}} baseline cases in ${{startYrBaseline}} to ${{agenticIncs.length}} total cases in this window, led by <a onclick="window.filterByVector('Rogue MCP Server / Tool Poisoning')">Rogue MCP tool injection</a> and cross-agent context worms.`;
        list.appendChild(li4);

        const li5 = document.createElement('li');
        li5.className = 'concern-item';
        li5.innerHTML = `<strong>Forward Continuity:</strong> Ingestion engine automatically active for ${{maxDataYear + 1}}+ incidents via live feed sync or <a onclick="document.getElementById('logIncidentModal').style.display='flex'">+ Log Incident</a> button.`;
        list.appendChild(li5);
      }}"""

if old_concerns_fn in content:
    content = content.replace(old_concerns_fn, new_concerns_fn)
    print("Successfully replaced renderKeyConcerns in generate_dashboard.py")
else:
    print("Warning: old_concerns_fn exact string not found! Trying regex or substring replacement...")

# 8. Update renderHeroSection annual button text update
old_hero_start = """      function renderHeroSection(filtered) {{
        const canvas = document.getElementById('heroChartCanvas');"""

new_hero_start = """      function renderHeroSection(filtered) {{
        const canvas = document.getElementById('heroChartCanvas');
        const btnAnnual = document.getElementById('btnViewAnnual');
        if (btnAnnual) {{
          if (activeFilters.horizon === '5Y') {{
            btnAnnual.textContent = '5-Year View (2022–' + maxDataYear + '+)';
          }} else if (activeFilters.horizon === '12M') {{
            btnAnnual.textContent = 'Annual View';
          }} else if (activeFilters.horizon === 'ALL') {{
            btnAnnual.textContent = 'Continuous All-Time View';
          }} else {{
            btnAnnual.textContent = '10-Year View (2017–' + maxDataYear + '+)';
          }}
        }}"""

if old_hero_start in content:
    content = content.replace(old_hero_start, new_hero_start)
    print("Successfully added dynamic btnAnnual text to renderHeroSection")
else:
    print("Warning: old_hero_start not found!")

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved patched generate_dashboard.py.")
