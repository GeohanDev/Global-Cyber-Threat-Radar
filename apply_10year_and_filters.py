with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the badge <span class="badge-5y">5-YEAR & CONTINUOUS</span> from the header
old_h1 = """        <h1>
          GLOBAL AI CYBERATTACK RADAR
          <span class="badge-5y">5-YEAR & CONTINUOUS</span>
          <span class="badge-live" id="liveModeBadge">LIVE SYNC READY</span>
        </h1>
        <p>Worldwide Threat Intelligence · 5-Year Evolution (2022–2026+), Autonomous Agent Exploits & Future Ingestion</p>"""

new_h1 = """        <h1>
          GLOBAL AI CYBERATTACK RADAR
          <span class="badge-live" id="liveModeBadge">LIVE SYNC READY</span>
        </h1>
        <p>Worldwide Threat Intelligence · 10-Year Macro Horizon (2017–2026+), Autonomous Agent Exploits & Continuous Ingestion</p>"""

text = text.replace(old_h1, new_h1)

# 2. Update the Filter Panel HTML to include 10Y horizon, Target Sector, Attack Vector, and Specific Year filters
old_filter_panel = """      <div class="filter-group">
        <label for="filterHorizon">Time Horizon (5 Years / Continuous)</label>
        <select id="filterHorizon">
          <option value="5Y" selected>5-Year Dynamic View (2022 – 2026+)</option>
          <option value="ALL">All-Time Continuous (All Recorded)</option>
          <option value="12M">Rolling 12 Months (Recent Window)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterCategory">Scope / Category</label>
        <select id="filterCategory">
          <option value="ALL">All Categories (A, B, C)</option>
          <option value="A">Cat A: Attacks USING AI</option>
          <option value="B">Cat B: Attacks ON AI Systems</option>
          <option value="C">Cat C: Agentic Attacks Only</option>
          <option value="AB">Cat A & B</option>
          <option value="AC">Cat A & C</option>
          <option value="BC">Cat B & C</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterSeverity">Severity Level</label>
        <select id="filterSeverity">
          <option value="ALL">All Severities (1 - 5)</option>
          <option value="5">Severity 5: Systemic / Critical</option>
          <option value="4">Severity 4: Significant Loss</option>
          <option value="3">Severity 3: Confirmed Breach, Limited</option>
          <option value="2">Severity 2: Attempted, No Impact</option>
          <option value="1">Severity 1: Proof-of-Concept</option>
          <option value="4-5">Severity 4 & 5 (High/Critical)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterCountry">Geography / Country</label>
        <select id="filterCountry">
          <option value="ALL">Global (All Countries)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterTier">Source Registry Tier</label>
        <select id="filterTier">
          <option value="ALL">All Tiers (1, 2, 3)</option>
          <option value="1">Tier 1: Registries (ATLAS/CISA/AIID)</option>
          <option value="2">Tier 2: Vendor Intel (MSFT/Mandiant/CS)</option>
          <option value="3">Tier 3: Verified CTI News (Record/DarkReading)</option>
        </select>
      </div>"""

new_filter_panel = """      <div class="filter-group">
        <label for="filterHorizon">Time Horizon</label>
        <select id="filterHorizon">
          <option value="10Y" selected>10-Year Macro View (2017 – 2026+)</option>
          <option value="5Y">5-Year Trend View (2022 – 2026+)</option>
          <option value="12M">Rolling 12 Months (Recent Window)</option>
          <option value="ALL">All-Time Continuous (All Recorded)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterCategory">Scope / Category</label>
        <select id="filterCategory">
          <option value="ALL">All Categories (A, B, C)</option>
          <option value="A">Cat A: Attacks USING AI</option>
          <option value="B">Cat B: Attacks ON AI Systems</option>
          <option value="C">Cat C: Agentic Attacks Only</option>
          <option value="AB">Cat A & B</option>
          <option value="AC">Cat A & C</option>
          <option value="BC">Cat B & C</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterSeverity">Severity Level</label>
        <select id="filterSeverity">
          <option value="ALL">All Severities (1 - 5)</option>
          <option value="5">Severity 5: Systemic / Critical</option>
          <option value="4">Severity 4: Significant Loss</option>
          <option value="3">Severity 3: Confirmed Breach, Limited</option>
          <option value="2">Severity 2: Attempted, No Impact</option>
          <option value="1">Severity 1: Proof-of-Concept</option>
          <option value="4-5">Severity 4 & 5 (High/Critical)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterSector">Target Sector</label>
        <select id="filterSector">
          <option value="ALL">All Sectors</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterVector">Attack Vector</label>
        <select id="filterVector">
          <option value="ALL">All Vectors</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterYear">Specific Year</label>
        <select id="filterYear">
          <option value="ALL">All Years (2017–2026+)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterCountry">Geography / Country</label>
        <select id="filterCountry">
          <option value="ALL">Global (All Countries)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterTier">Source Registry Tier</label>
        <select id="filterTier">
          <option value="ALL">All Tiers (1, 2, 3)</option>
          <option value="1">Tier 1: Registries (ATLAS/CISA/AIID)</option>
          <option value="2">Tier 2: Vendor Intel (MSFT/Mandiant/CS)</option>
          <option value="3">Tier 3: Verified CTI News (Record/DarkReading)</option>
        </select>
      </div>"""

text = text.replace(old_filter_panel, new_filter_panel)

# 3. Update activeFilters initial state in JavaScript
old_active_filters = """      let activeFilters = {{
        horizon: '5Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        tier: 'ALL',
        sortCol: 'date',
        sortAsc: false,
        articleSearch: '',
        incidentSearch: ''
      }};"""

new_active_filters = """      let activeFilters = {{
        horizon: '10Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        sector: 'ALL',
        vector: 'ALL',
        year: 'ALL',
        tier: 'ALL',
        sortCol: 'date',
        sortAsc: false,
        articleSearch: '',
        incidentSearch: ''
      }};"""

text = text.replace(old_active_filters, new_active_filters)

# 4. Update populate dropdowns to include sector, vector, and year
old_populate_country = """      function populateCountryDropdown() {{
        const select = document.getElementById('filterCountry');
        select.innerHTML = '<option value="ALL">Global (All Countries)</option>';
        const countries = Array.from(new Set(allIncidents.map(i => i.country))).sort();
        countries.forEach(c => {{
          const opt = document.createElement('option');
          opt.value = c;
          opt.textContent = c;
          select.appendChild(opt);
        }});
      }}"""

new_populate_dropdowns = """      function populateCountryDropdown() {{
        const select = document.getElementById('filterCountry');
        select.innerHTML = '<option value="ALL">Global (All Countries)</option>';
        const countries = Array.from(new Set(allIncidents.map(i => i.country))).sort();
        countries.forEach(c => {{
          const opt = document.createElement('option');
          opt.value = c;
          opt.textContent = c;
          select.appendChild(opt);
        }});
      }}

      function populateSectorDropdown() {{
        const select = document.getElementById('filterSector');
        if (!select) return;
        select.innerHTML = '<option value="ALL">All Sectors</option>';
        const sectors = Array.from(new Set(allIncidents.map(i => i.target_sector).filter(Boolean))).sort();
        sectors.forEach(s => {{
          const opt = document.createElement('option');
          opt.value = s;
          opt.textContent = s;
          select.appendChild(opt);
        }});
      }}

      function populateVectorDropdown() {{
        const select = document.getElementById('filterVector');
        if (!select) return;
        select.innerHTML = '<option value="ALL">All Vectors</option>';
        const vectors = Array.from(new Set(allIncidents.map(i => i.attack_vector).filter(Boolean))).sort();
        vectors.forEach(v => {{
          const opt = document.createElement('option');
          opt.value = v;
          opt.textContent = v;
          select.appendChild(opt);
        }});
      }}

      function populateSpecificYearDropdown() {{
        const select = document.getElementById('filterYear');
        if (!select) return;
        select.innerHTML = `<option value="ALL">All Years (${{minDataYear}}–${{maxDataYear}}+)</option>`;
        for (let yr = maxDataYear; yr >= minDataYear; yr--) {{
          const opt = document.createElement('option');
          opt.value = String(yr);
          opt.textContent = `Year ${{yr}}`;
          select.appendChild(opt);
        }}
      }}"""

text = text.replace(old_populate_country, new_populate_dropdowns)

# 5. Update getFilteredIncidents to support 10Y, 5Y, sector, vector, and specific year
old_get_filtered_incidents = """      function getFilteredIncidents() {{
        return allIncidents.filter(inc => {{
          const incYear = parseInt(inc.date.substring(0, 4));
          
          if (activeFilters.horizon === '5Y') {{
            if (incYear < (maxDataYear - 4)) return false;
          }} else if (activeFilters.horizon === '12M') {{
            if (inc.date < '2025-12-01') return false;
          }} else if (activeFilters.horizon !== 'ALL') {{
            const chosenYear = parseInt(activeFilters.horizon);
            if (incYear !== chosenYear) return false;
          }}

          if (activeFilters.category !== 'ALL') {{"""

new_get_filtered_incidents = """      function getFilteredIncidents() {{
        return allIncidents.filter(inc => {{
          const incYear = parseInt(inc.date.substring(0, 4));
          
          if (activeFilters.horizon === '10Y') {{
            if (incYear < (maxDataYear - 9)) return false;
          }} else if (activeFilters.horizon === '5Y') {{
            if (incYear < (maxDataYear - 4)) return false;
          }} else if (activeFilters.horizon === '12M') {{
            if (inc.date < '2025-12-01') return false;
          }} else if (activeFilters.horizon !== 'ALL') {{
            const chosenYear = parseInt(activeFilters.horizon);
            if (incYear !== chosenYear) return false;
          }}

          if (activeFilters.year !== 'ALL' && incYear !== parseInt(activeFilters.year)) {{
            return false;
          }}

          if (activeFilters.sector !== 'ALL' && inc.target_sector !== activeFilters.sector) {{
            return false;
          }}

          if (activeFilters.vector !== 'ALL' && inc.attack_vector !== activeFilters.vector) {{
            return false;
          }}

          if (activeFilters.category !== 'ALL') {{"""

text = text.replace(old_get_filtered_incidents, new_get_filtered_incidents)

# 6. Update renderHeroSection for 10-year macro calculation
old_hero_start = """        if (heroChartMode === 'annual') {{
          titleEl.textContent = 'Annual AI Cyber Incident Frequency (5-Year Macro Horizon)';
          
          const startYear = Math.max(minDataYear, maxDataYear - 4);
          const years = [];
          for (let y = startYear; y <= maxDataYear; y++) {{
            years.push(String(y));
          }}"""

new_hero_start = """        if (heroChartMode === 'annual') {{
          const is10Y = (activeFilters.horizon === '10Y' || activeFilters.horizon === 'ALL');
          const startYear = is10Y 
            ? Math.max(minDataYear, maxDataYear - 9)
            : Math.max(minDataYear, maxDataYear - 4);

          titleEl.textContent = is10Y
            ? `Annual AI Cyber Incident Frequency (10-Year Macro Horizon, ${{startYear}}–${{maxDataYear}}+)`
            : `Annual AI Cyber Incident Frequency (5-Year Trend Horizon, ${{startYear}}–${{maxDataYear}}+)`;
          
          const years = [];
          for (let y = startYear; y <= maxDataYear; y++) {{
            years.push(String(y));
          }}"""

text = text.replace(old_hero_start, new_hero_start)

# 7. Update event listeners to handle new filters and reset
old_listeners = """      document.getElementById('filterHorizon').addEventListener('change', (e) => {{
        activeFilters.horizon = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterCategory').addEventListener('change', (e) => {{
        activeFilters.category = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterSeverity').addEventListener('change', (e) => {{
        activeFilters.severity = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterCountry').addEventListener('change', (e) => {{
        activeFilters.country = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterTier').addEventListener('change', (e) => {{
        activeFilters.tier = e.target.value;
        updateDashboard();
      }});

      document.getElementById('btnResetFilters').addEventListener('click', () => {{
        activeFilters = {{
          horizon: '5Y',
          category: 'ALL',
          severity: 'ALL',
          country: 'ALL',
          tier: 'ALL',
          sortCol: 'date',
          sortAsc: false,
          articleSearch: '',
          incidentSearch: ''
        }};
        document.getElementById('filterHorizon').value = '5Y';
        document.getElementById('filterCategory').value = 'ALL';
        document.getElementById('filterSeverity').value = 'ALL';
        document.getElementById('filterCountry').value = 'ALL';
        document.getElementById('filterTier').value = 'ALL';
        document.getElementById('searchArticles').value = '';
        document.getElementById('searchIncidents').value = '';
        updateDashboard();
      }});"""

new_listeners = """      document.getElementById('filterHorizon').addEventListener('change', (e) => {{
        activeFilters.horizon = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterCategory').addEventListener('change', (e) => {{
        activeFilters.category = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterSeverity').addEventListener('change', (e) => {{
        activeFilters.severity = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterSector').addEventListener('change', (e) => {{
        activeFilters.sector = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterVector').addEventListener('change', (e) => {{
        activeFilters.vector = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterYear').addEventListener('change', (e) => {{
        activeFilters.year = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterCountry').addEventListener('change', (e) => {{
        activeFilters.country = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterTier').addEventListener('change', (e) => {{
        activeFilters.tier = e.target.value;
        updateDashboard();
      }});

      document.getElementById('btnResetFilters').addEventListener('click', () => {{
        activeFilters = {{
          horizon: '10Y',
          category: 'ALL',
          severity: 'ALL',
          country: 'ALL',
          sector: 'ALL',
          vector: 'ALL',
          year: 'ALL',
          tier: 'ALL',
          sortCol: 'date',
          sortAsc: false,
          articleSearch: '',
          incidentSearch: ''
        }};
        document.getElementById('filterHorizon').value = '10Y';
        document.getElementById('filterCategory').value = 'ALL';
        document.getElementById('filterSeverity').value = 'ALL';
        document.getElementById('filterSector').value = 'ALL';
        document.getElementById('filterVector').value = 'ALL';
        document.getElementById('filterYear').value = 'ALL';
        document.getElementById('filterCountry').value = 'ALL';
        document.getElementById('filterTier').value = 'ALL';
        document.getElementById('searchArticles').value = '';
        document.getElementById('searchIncidents').value = '';
        updateDashboard();
      }});"""

text = text.replace(old_listeners, new_listeners)

# 8. Call populate functions during startup
old_startup = """      populateYearFilters();
      populateCountryDropdown();
      renderSourceTable();
      updateDashboard();"""

new_startup = """      populateYearFilters();
      populateCountryDropdown();
      populateSectorDropdown();
      populateVectorDropdown();
      populateSpecificYearDropdown();
      renderSourceTable();
      updateDashboard();"""

text = text.replace(old_startup, new_startup)

# 9. KPI label for 10-year
old_kpi_sub = """        const horizonLabel = activeFilters.horizon === '5Y' ? '5-Year Rolling (2022–' + maxDataYear + ')' :
          (activeFilters.horizon === '12M' ? 'Rolling 12 Months' : 'Active View (' + activeFilters.horizon + ')');
        document.getElementById('kpiHorizonSub').textContent = horizonLabel;"""

new_kpi_sub = """        const horizonLabel = activeFilters.horizon === '10Y' ? '10-Year Macro (2017–' + maxDataYear + '+)' :
          (activeFilters.horizon === '5Y' ? '5-Year Rolling (2022–' + maxDataYear + '+)' :
          (activeFilters.horizon === '12M' ? 'Rolling 12 Months' : 'Active View (' + activeFilters.horizon + ')'));
        document.getElementById('kpiHorizonSub').textContent = horizonLabel;"""

text = text.replace(old_kpi_sub, new_kpi_sub)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_dashboard.py updated with 10-year view and added filters!")
