with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Target Entity dropdown in HTML Universal Filter Bar right before the Reset button
filter_tier_block = """      <div class="filter-group">
        <label for="filterTier">Source Registry Tier</label>
        <select id="filterTier">
          <option value="ALL">All Tiers (1, 2, 3)</option>
          <option value="1">Tier 1: Registries (ATLAS/CISA/AIID)</option>
          <option value="2">Tier 2: Vendor Intel (MSFT/Mandiant/CS)</option>
          <option value="3">Tier 3: Verified CTI News (Record/DarkReading)</option>
        </select>
      </div>"""

filter_entity_block = """      <div class="filter-group">
        <label for="filterTier">Source Registry Tier</label>
        <select id="filterTier">
          <option value="ALL">All Tiers (1, 2, 3)</option>
          <option value="1">Tier 1: Registries (ATLAS/CISA/AIID)</option>
          <option value="2">Tier 2: Vendor Intel (MSFT/Mandiant/CS)</option>
          <option value="3">Tier 3: Verified CTI News (Record/DarkReading)</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="filterEntity" style="color: #38bdf8; font-weight: 700;">Famous Company / Ecosystem</label>
        <select id="filterEntity" style="border-color: rgba(56, 189, 248, 0.5);">
          <option value="ALL" selected>All Companies (Global Threat)</option>
          <option value="Gemini">✨ Google Gemini</option>
          <option value="Anthropic">🧠 Anthropic Claude</option>
          <option value="Hugging Face">🤗 Hugging Face</option>
          <option value="OpenAI">🤖 OpenAI / ChatGPT</option>
          <option value="Microsoft">🪟 Microsoft / Copilot</option>
          <option value="NVIDIA">⚡ NVIDIA</option>
          <option value="Meta">🦙 Meta Llama</option>
        </select>
      </div>"""

if filter_tier_block in content:
    content = content.replace(filter_tier_block, filter_entity_block)
    print("Added #filterEntity dropdown to Universal Filter Bar HTML")
else:
    print("Warning: filter_tier_block not found exactly!")

# 2. Update activeFilters initialization
old_init = """let activeFilters = {{
        horizon: '10Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        sector: 'ALL',
        vector: 'ALL',
        year: 'ALL',
        tier: 'ALL',"""

new_init = """let activeFilters = {{
        horizon: '10Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        sector: 'ALL',
        vector: 'ALL',
        year: 'ALL',
        tier: 'ALL',
        entity: 'ALL',"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("Updated activeFilters initialization with entity: 'ALL'")

# 3. Add entity check in getFilteredIncidents
incident_filter_target = """if (activeFilters.tier !== 'ALL' && inc.source_tier !== parseInt(activeFilters.tier)) {{
            return false;
          }}"""

incident_filter_repl = """if (activeFilters.tier !== 'ALL' && inc.source_tier !== parseInt(activeFilters.tier)) {{
            return false;
          }}

          if (activeFilters.entity && activeFilters.entity !== 'ALL') {{
            const ent = activeFilters.entity.toLowerCase();
            const text = (inc.headline + ' ' + inc.incident_id + ' ' + inc.attack_vector + ' ' + inc.target_sector + ' ' + inc.country + ' ' + (inc.outlet || '')).toLowerCase();
            if (ent === 'microsoft') {{
              if (!text.includes('microsoft') && !text.includes('copilot')) return false;
            }} else if (ent === 'openai') {{
              if (!text.includes('openai') && !text.includes('chatgpt') && !text.includes('gpt')) return false;
            }} else if (ent === 'anthropic') {{
              if (!text.includes('anthropic') && !text.includes('claude')) return false;
            }} else if (ent === 'gemini') {{
              if (!text.includes('gemini') && !text.includes('google')) return false;
            }} else if (ent === 'meta') {{
              if (!text.includes('meta') && !text.includes('llama')) return false;
            }} else if (ent === 'hugging face') {{
              if (!text.includes('hugging face') && !text.includes('huggingface')) return false;
            }} else if (ent === 'nvidia') {{
              if (!text.includes('nvidia')) return false;
            }} else {{
              if (!text.includes(ent)) return false;
            }}
          }}"""

if incident_filter_target in content:
    content = content.replace(incident_filter_target, incident_filter_repl)
    print("Added entity filtering logic to getFilteredIncidents")

# 4. Add entity check in getFilteredArticles
article_filter_target = """function getFilteredArticles() {{
        const validIncidentIds = new Set(getFilteredIncidents().map(i => i.incident_id));
        return allArticles.filter(art => {{
          if (!art.isLive && !validIncidentIds.has(art.incident_id)) return false;"""

article_filter_repl = """function getFilteredArticles() {{
        const validIncidentIds = new Set(getFilteredIncidents().map(i => i.incident_id));
        return allArticles.filter(art => {{
          if (!art.isLive && !validIncidentIds.has(art.incident_id)) return false;
          
          if (art.isLive && activeFilters.entity && activeFilters.entity !== 'ALL') {{
            const ent = activeFilters.entity.toLowerCase();
            const text = (art.headline + ' ' + art.outlet + ' ' + (art.summary || '')).toLowerCase();
            let matches = false;
            if (ent === 'microsoft') matches = text.includes('microsoft') || text.includes('copilot');
            else if (ent === 'openai') matches = text.includes('openai') || text.includes('chatgpt') || text.includes('gpt');
            else if (ent === 'anthropic') matches = text.includes('anthropic') || text.includes('claude');
            else if (ent === 'gemini') matches = text.includes('gemini') || text.includes('google');
            else if (ent === 'meta') matches = text.includes('meta') || text.includes('llama');
            else if (ent === 'hugging face') matches = text.includes('hugging face') || text.includes('huggingface');
            else if (ent === 'nvidia') matches = text.includes('nvidia');
            else matches = text.includes(ent);
            if (!matches) return false;
          }}"""

if article_filter_target in content:
    content = content.replace(article_filter_target, article_filter_repl)
    print("Added entity filtering logic to getFilteredArticles")

# 5. Update window.filterByEcosystem to sync with filterEntity dropdown
old_filter_eco = """      window.filterByEcosystem = function(eco) {{
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
      }};"""

new_filter_eco = """      window.filterByEcosystem = function(eco) {{
        activeFilters.entity = eco;
        const entDropdown = document.getElementById('filterEntity');
        if (entDropdown) entDropdown.value = eco;

        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
        if (event && event.target && event.target.classList.contains('pill-btn')) {{
          event.target.classList.add('active');
        }} else {{
          document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
            if ((eco === 'ALL' && b.textContent.includes('All Cases')) ||
                (eco !== 'ALL' && b.textContent.includes(eco))) {{
              b.classList.add('active');
            }}
          }});
        }}
        
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};"""

if old_filter_eco in content:
    content = content.replace(old_filter_eco, new_filter_eco)
    print("Updated window.filterByEcosystem function")

# 6. Add event listener for filterEntity dropdown
listener_target = "document.getElementById('filterTier').addEventListener('change', e => {{"
listener_code = """document.getElementById('filterEntity').addEventListener('change', e => {{
        activeFilters.entity = e.target.value;
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
          if ((e.target.value === 'ALL' && b.textContent.includes('All Cases')) ||
              (e.target.value !== 'ALL' && b.textContent.includes(e.target.value))) {{
            b.classList.add('active');
          }} else {{
            b.classList.remove('active');
          }}
        }});
        updateDashboard();
      }});

      document.getElementById('filterTier').addEventListener('change', e => {{"""

if listener_target in content:
    content = content.replace(listener_target, listener_code)
    print("Added change event listener for filterEntity dropdown")

# 7. Update btnResetFilters to reset filterEntity
reset_target = "document.getElementById('filterTier').value = 'ALL';"
reset_repl = """document.getElementById('filterTier').value = 'ALL';
        const entSelect = document.getElementById('filterEntity');
        if (entSelect) entSelect.value = 'ALL';
        activeFilters.entity = 'ALL';
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
        const allBtn = document.querySelector('.ecosystem-pills-bar .pill-btn');
        if (allBtn) allBtn.classList.add('active');"""

if reset_target in content:
    content = content.replace(reset_target, reset_repl)
    print("Updated btnResetFilters to reset entity filter")

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved generate_dashboard.py with official Target Entity filter dropdown.")
