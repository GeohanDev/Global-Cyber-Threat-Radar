# patch_jpmorgan_cases.py

with open("generate_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Add JPMorgan to filterEntity select options
old_select = """          <option value="NVIDIA">⚡ NVIDIA</option>
          <option value="Meta">🦙 Meta Llama</option>
        </select>"""

new_select = """          <option value="NVIDIA">⚡ NVIDIA</option>
          <option value="Meta">🦙 Meta Llama</option>
          <option value="JPMorgan">🏦 JPMorgan Chase & Major Banks (Nov 19 Cyberattack)</option>
        </select>"""

if old_select in code:
    code = code.replace(old_select, new_select, 1)

# 2. Add JPMorgan pill to ecosystem-pills-bar
old_pills = """        <button class="pill-btn" data-eco="NVIDIA" onclick="window.filterByEcosystem('NVIDIA')">⚡ NVIDIA</button>
        <button class="pill-btn" data-eco="Meta" onclick="window.filterByEcosystem('Meta')">🦙 Meta Llama</button>
      </div>"""

new_pills = """        <button class="pill-btn" data-eco="NVIDIA" onclick="window.filterByEcosystem('NVIDIA')">⚡ NVIDIA</button>
        <button class="pill-btn" data-eco="Meta" onclick="window.filterByEcosystem('Meta')">🦙 Meta Llama</button>
        <button class="pill-btn" data-eco="JPMorgan" onclick="window.filterByEcosystem('JPMorgan')" style="border-color: rgba(234,179,8,0.4); color: #facc15;">🏦 JPMorgan Chase</button>
      </div>"""

if old_pills in code:
    code = code.replace(old_pills, new_pills, 1)

# 3. Add fuzzySearchMatch helper before getFilteredIncidents
old_before_filter = """      function getFilteredIncidents() {{" """.strip()

new_before_filter = """      function fuzzySearchMatch(text, query) {{
        if (!query) return true;
        const q = query.toLowerCase().trim();
        const t = text.toLowerCase();
        if (t.includes(q)) return true;
        // Normalize spaces (e.g. "jp morgan" -> "jpmorgan")
        const noSpaces = q.replace(/\\s+/g, '');
        if (t.includes(noSpaces)) return true;
        // Check JPMorgan / Chase banking aliases
        if (q.includes('jp morgan') || q.includes('jpmorgan') || q.includes('chase')) {{
          if (t.includes('jpmorgan') || t.includes('jp morgan') || t.includes('chase') || t.includes('mastercard') || t.includes('visa')) return true;
        }}
        // Check all words
        const words = q.split(/\\s+/).filter(w => w.length > 2);
        if (words.length > 1 && words.every(w => t.includes(w))) return true;
        return false;
      }}

      function getFilteredIncidents() {{"""

assert "function getFilteredIncidents() {{" in code, "Failed to find getFilteredIncidents"
code = code.replace("function getFilteredIncidents() {{", new_before_filter, 1)

# 4. Update activeFilters.entity in getFilteredIncidents
old_ent_match = """            }} else if (ent === 'nvidia') {{
              if (!text.includes('nvidia')) return false;
            }} else {{
              if (!text.includes(ent)) return false;
            }}"""

new_ent_match = """            }} else if (ent === 'nvidia') {{
              if (!text.includes('nvidia')) return false;
            }} else if (ent === 'jpmorgan' || ent === 'jp morgan') {{
              if (!text.includes('jpmorgan') && !text.includes('jp morgan') && !text.includes('chase') && !text.includes('mastercard') && !text.includes('visa')) return false;
            }} else {{
              if (!text.includes(ent)) return false;
            }}"""

assert old_ent_match in code, "Failed to find old_ent_match"
code = code.replace(old_ent_match, new_ent_match, 1)

# 5. Update activeFilters.incidentSearch in getFilteredIncidents
old_inc_search = """          if (activeFilters.incidentSearch) {{
            const q = activeFilters.incidentSearch.toLowerCase();
            const text = (inc.headline + ' ' + inc.incident_id + ' ' + inc.attack_vector + ' ' + inc.target_sector + ' ' + inc.country + ' ' + (inc.outlet || '')).toLowerCase();
            if (!text.includes(q)) return false;
          }}"""

new_inc_search = """          if (activeFilters.incidentSearch) {{
            const text = (inc.headline + ' ' + inc.incident_id + ' ' + inc.attack_vector + ' ' + inc.target_sector + ' ' + inc.country + ' ' + (inc.outlet || '')).toLowerCase();
            if (!fuzzySearchMatch(text, activeFilters.incidentSearch)) return false;
          }}"""

assert old_inc_search in code, "Failed to find old_inc_search"
code = code.replace(old_inc_search, new_inc_search, 1)

# 6. Update activeFilters.entity in getFilteredArticles
old_art_ent = """            else if (ent === 'nvidia') matches = text.includes('nvidia');
            else matches = text.includes(ent);
            if (!matches) return false;"""

new_art_ent = """            else if (ent === 'nvidia') matches = text.includes('nvidia');
            else if (ent === 'jpmorgan' || ent === 'jp morgan') matches = text.includes('jpmorgan') || text.includes('jp morgan') || text.includes('chase') || text.includes('mastercard') || text.includes('visa');
            else matches = text.includes(ent);
            if (!matches) return false;"""

assert old_art_ent in code, "Failed to find old_art_ent"
code = code.replace(old_art_ent, new_art_ent, 1)

# 7. Update activeFilters.articleSearch in getFilteredArticles
old_art_search = """          if (activeFilters.articleSearch) {{
            const q = activeFilters.articleSearch.toLowerCase();
            const text = (art.headline + ' ' + art.outlet + ' ' + art.country).toLowerCase();
            if (!text.includes(q)) return false;
          }}"""

new_art_search = """          if (activeFilters.articleSearch) {{
            const text = (art.headline + ' ' + art.outlet + ' ' + art.country + ' ' + (art.summary || '')).toLowerCase();
            if (!fuzzySearchMatch(text, activeFilters.articleSearch)) return false;
          }}"""

assert old_art_search in code, "Failed to find old_art_search"
code = code.replace(old_art_search, new_art_search, 1)

# 8. Update syncQuickPills for JPMorgan
old_sync_eco = """        // 5. Ecosystem Pills
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
          const eco = b.getAttribute('data-eco');
          b.classList.toggle('active', eco === activeFilters.entity);
        }});"""

new_sync_eco = """        // 5. Ecosystem Pills
        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
          const eco = b.getAttribute('data-eco');
          const isMatch = (eco === activeFilters.entity) ||
                          (eco === 'JPMorgan' && (activeFilters.entity === 'JPMorgan' || activeFilters.entity === 'jp morgan' || activeFilters.entity === 'jpmorgan'));
          b.classList.toggle('active', !!isMatch);
        }});"""

assert old_sync_eco in code, "Failed to find old_sync_eco"
code = code.replace(old_sync_eco, new_sync_eco, 1)

with open("generate_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

print("generate_dashboard.py patched successfully with JPMorgan & robust search!")
