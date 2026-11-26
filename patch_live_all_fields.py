# patch_live_all_fields.py
import re

with open("generate_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update pre-embedding of bs4_extracted_feed.json to include field, rel_time, and pub_date
old_embed = """                data.setdefault("articles", []).insert(0, {
                    "article_id": art_id,
                    "incident_id": inc_id,
                    "date": item.get("date", "2026-11-20")[:10],
                    "headline": title,
                    "outlet": outlet,
                    "url": url,
                    "country": country,
                    "category": list(set(cat)),
                    "severity": sev,
                    "summary": desc,
                    "isLive": True,
                    "live_time": "🟢 Live Stream"
                })"""

new_embed = """                data.setdefault("articles", []).insert(0, {
                    "article_id": art_id,
                    "incident_id": inc_id,
                    "date": item.get("date", "2026-11-20")[:10],
                    "headline": title,
                    "outlet": outlet,
                    "url": url,
                    "country": country,
                    "field": item.get("field", "it"),
                    "category": item.get("category", list(set(cat))),
                    "severity": item.get("severity", sev),
                    "summary": desc,
                    "isLive": True,
                    "pub_date": item.get("pub_date", ""),
                    "rel_time": item.get("rel_time", "Just now"),
                    "live_time": item.get("rel_time", "Just now")
                })"""

assert old_embed in code, "Failed to find old_embed"
code = code.replace(old_embed, new_embed, 1)

# 2. Update Reported Articles Feed header to add Tech Domain Pills and Live Sweep controls
old_feed_header = """    <!-- 6. Reported Articles Feed -->
    <section class="section-card">
      <div class="articles-feed-header">
        <div class="section-title">
          <span>Reported Articles Feed (What Was Reported)</span>
          <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);" id="articlesCountBadge">(50 most recent)</span>
        </div>
        <div class="feed-controls">
          <input type="text" class="feed-search" id="articleSearchInput" placeholder="Filter articles by text...">
        </div>
      </div>
      <!-- Broadcaster & News Source Quick-Filter Bar -->
      <div class="card-pills-row" id="pillsBroadcast" style="margin-bottom: 14px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>📡</span> News Broadcast:
        </span>
        <button class="pill-btn active" data-broadcast="ALL" onclick="window.filterByBroadcast('ALL')">All Sources</button>
        <button class="pill-btn" data-broadcast="BBC" onclick="window.filterByBroadcast('BBC')">📺 BBC News</button>
        <button class="pill-btn" data-broadcast="CNN" onclick="window.filterByBroadcast('CNN')">📺 CNN</button>
        <button class="pill-btn" data-broadcast="Reuters" onclick="window.filterByBroadcast('Reuters')">🌐 Reuters</button>
        <button class="pill-btn" data-broadcast="Bloomberg" onclick="window.filterByBroadcast('Bloomberg')">📊 Bloomberg</button>
        <button class="pill-btn" data-broadcast="Guardian" onclick="window.filterByBroadcast('Guardian')">📰 The Guardian</button>
        <button class="pill-btn" data-broadcast="CNBC" onclick="window.filterByBroadcast('CNBC')">📈 CNBC</button>
        <button class="pill-btn" data-broadcast="TechCrunch" onclick="window.filterByBroadcast('TechCrunch')">⚡ TechCrunch</button>
        <button class="pill-btn" data-broadcast="Wired" onclick="window.filterByBroadcast('Wired')">🔌 Wired</button>
        <button class="pill-btn" data-broadcast="CTI" onclick="window.filterByBroadcast('CTI')">🛡️ CTI Registries</button>
      </div>"""

new_feed_header = """    <!-- 6. Reported Articles Feed -->
    <section class="section-card">
      <div class="articles-feed-header" style="flex-wrap: wrap; gap: 10px;">
        <div class="section-title">
          <span>Reported Articles Feed (What Was Reported)</span>
          <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);" id="articlesCountBadge">(50 most recent)</span>
        </div>
        <div class="feed-controls" style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
          <div style="display: flex; align-items: center; gap: 6px; font-size: 0.75rem; color: #10b981; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); padding: 4px 10px; border-radius: 20px; font-weight: 600;">
            <span class="live-dot" style="display: inline-block; width: 7px; height: 7px; background: #10b981; border-radius: 50%; box-shadow: 0 0 6px #10b981;"></span>
            <span>Next Live Sweep: <span id="sweepCountdown">90s</span></span>
          </div>
          <button id="forceSweepBtn" onclick="window.forceLiveSweep()" class="pill-btn" style="background: rgba(56,189,248,0.12); color: #38bdf8; border: 1px solid #38bdf8; font-weight: 600; cursor: pointer; padding: 4px 12px; border-radius: 6px;">
            ⚡ Force Live Sweep
          </button>
          <input type="text" class="feed-search" id="articleSearchInput" placeholder="Filter articles by text...">
        </div>
      </div>

      <!-- Tech Domain & Field Quick-Filter Bar -->
      <div class="card-pills-row" id="pillsField" style="margin-bottom: 8px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start; flex-wrap: wrap;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>🌐</span> Tech Field:
        </span>
        <button class="pill-btn active" data-field="ALL" onclick="window.filterByField('ALL')">All Fields (660+)</button>
        <button class="pill-btn" data-field="ai" onclick="window.filterByField('ai')">🤖 AI & Frontier LLMs</button>
        <button class="pill-btn" data-field="cyber" onclick="window.filterByField('cyber')">🛡️ Cybersecurity & CTI</button>
        <button class="pill-btn" data-field="hardware" onclick="window.filterByField('hardware')">💻 Computer Hardware & Chips</button>
        <button class="pill-btn" data-field="it" onclick="window.filterByField('it')">☁️ Enterprise IT & Cloud</button>
      </div>

      <!-- Broadcaster & News Source Quick-Filter Bar -->
      <div class="card-pills-row" id="pillsBroadcast" style="margin-bottom: 14px; margin-top: 0; padding-top: 0; border-top: none; justify-content: flex-start; flex-wrap: wrap;">
        <span style="font-size: 0.72rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 6px; display: inline-flex; align-items: center; gap: 4px;">
          <span>📡</span> News Broadcast:
        </span>
        <button class="pill-btn active" data-broadcast="ALL" onclick="window.filterByBroadcast('ALL')">All Sources</button>
        <button class="pill-btn" data-broadcast="BBC" onclick="window.filterByBroadcast('BBC')">📺 BBC News</button>
        <button class="pill-btn" data-broadcast="CNN" onclick="window.filterByBroadcast('CNN')">📺 CNN</button>
        <button class="pill-btn" data-broadcast="Reuters" onclick="window.filterByBroadcast('Reuters')">🌐 Reuters</button>
        <button class="pill-btn" data-broadcast="Bloomberg" onclick="window.filterByBroadcast('Bloomberg')">📊 Bloomberg</button>
        <button class="pill-btn" data-broadcast="Guardian" onclick="window.filterByBroadcast('Guardian')">📰 The Guardian</button>
        <button class="pill-btn" data-broadcast="CNBC" onclick="window.filterByBroadcast('CNBC')">📈 CNBC</button>
        <button class="pill-btn" data-broadcast="TechCrunch" onclick="window.filterByBroadcast('TechCrunch')">⚡ TechCrunch</button>
        <button class="pill-btn" data-broadcast="Wired" onclick="window.filterByBroadcast('Wired')">🔌 Wired</button>
        <button class="pill-btn" data-broadcast="Ars Technica" onclick="window.filterByBroadcast('arstechnica')">💻 Ars Technica</button>
        <button class="pill-btn" data-broadcast="Tom's Hardware" onclick="window.filterByBroadcast('tomshardware')">⚙️ Tom's Hardware</button>
        <button class="pill-btn" data-broadcast="CTI" onclick="window.filterByBroadcast('CTI')">🛡️ CTI Registries</button>
      </div>"""

assert old_feed_header in code, "Failed to find old_feed_header"
code = code.replace(old_feed_header, new_feed_header, 1)

# 3. Add field: 'ALL' to activeFilters
old_filters = """      let activeFilters = {{
        horizon: '10Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        sector: 'ALL',
        vector: 'ALL',
        year: 'ALL',
        tier: 'ALL',
        entity: 'ALL',
        broadcast: 'ALL',"""

new_filters = """      let activeFilters = {{
        horizon: '10Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        sector: 'ALL',
        vector: 'ALL',
        year: 'ALL',
        tier: 'ALL',
        entity: 'ALL',
        broadcast: 'ALL',
        field: 'ALL',"""

assert old_filters in code, "Failed to find old_filters"
code = code.replace(old_filters, new_filters, 1)

# 4. Update getFilteredArticles to filter by activeFilters.field and expanded broadcast
old_art_filter = """          if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
            const bc = activeFilters.broadcast.toLowerCase();
            const outlet = (art.outlet || '').toLowerCase();
            if (bc === 'cti') {{
              if (!outlet.includes('record') && !outlet.includes('dark reading') && !outlet.includes('securityweek') && !outlet.includes('hacker news') && !outlet.includes('krebs') && !outlet.includes('ncsc') && !outlet.includes('mitre') && !outlet.includes('atlas') && !outlet.includes('cso') && !outlet.includes('affairs')) return false;
            }} else if (bc === 'guardian') {{
              if (!outlet.includes('guardian')) return false;
            }} else if (bc === 'bbc') {{
              if (!outlet.includes('bbc')) return false;
            }} else if (bc === 'cnn') {{
              if (!outlet.includes('cnn')) return false;
            }} else if (bc === 'reuters') {{
              if (!outlet.includes('reuters')) return false;
            }} else if (bc === 'bloomberg') {{
              if (!outlet.includes('bloomberg')) return false;
            }} else if (bc === 'cnbc') {{
              if (!outlet.includes('cnbc')) return false;
            }} else if (bc === 'techcrunch') {{
              if (!outlet.includes('techcrunch')) return false;
            }} else if (bc === 'wired') {{
              if (!outlet.includes('wired')) return false;
            }} else {{
              if (!outlet.includes(bc)) return false;
            }}
          }}"""

new_art_filter = """          if (activeFilters.field && activeFilters.field !== 'ALL') {{
            if (art.field !== activeFilters.field) return false;
          }}
          if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
            const bc = activeFilters.broadcast.toLowerCase();
            const outlet = (art.outlet || '').toLowerCase();
            if (bc === 'cti') {{
              if (!outlet.includes('record') && !outlet.includes('dark reading') && !outlet.includes('securityweek') && !outlet.includes('hacker news') && !outlet.includes('krebs') && !outlet.includes('ncsc') && !outlet.includes('mitre') && !outlet.includes('atlas') && !outlet.includes('cso') && !outlet.includes('affairs')) return false;
            }} else if (bc === 'guardian') {{
              if (!outlet.includes('guardian')) return false;
            }} else if (bc === 'bbc') {{
              if (!outlet.includes('bbc')) return false;
            }} else if (bc === 'cnn') {{
              if (!outlet.includes('cnn')) return false;
            }} else if (bc === 'reuters') {{
              if (!outlet.includes('reuters')) return false;
            }} else if (bc === 'bloomberg') {{
              if (!outlet.includes('bloomberg')) return false;
            }} else if (bc === 'cnbc') {{
              if (!outlet.includes('cnbc')) return false;
            }} else if (bc === 'techcrunch') {{
              if (!outlet.includes('techcrunch')) return false;
            }} else if (bc === 'wired') {{
              if (!outlet.includes('wired')) return false;
            }} else if (bc === 'arstechnica') {{
              if (!outlet.includes('ars')) return false;
            }} else if (bc === 'tomshardware') {{
              if (!outlet.includes('tom')) return false;
            }} else {{
              if (!outlet.includes(bc)) return false;
            }}
          }}"""

assert old_art_filter in code, "Failed to find old_art_filter"
code = code.replace(old_art_filter, new_art_filter, 1)

# 5. Update renderArticlesFeed to display relative time badges and domain badges
old_render_card = """          const isLiveNow = art.isLive || art.live_time;
          const liveBadgeHtml = isLiveNow 
            ? `<span class="badge" style="background:rgba(16,185,129,0.18); color:#10b981; border:1px solid #10b981; font-weight:700;">🟢 LIVE</span> `
            : '';
          const timeText = art.live_time ? art.live_time : art.date;

          card.innerHTML = `
            <div class="article-meta">
              <span class="article-outlet">${{art.outlet}}</span>
              <div style="display:flex; align-items:center; gap:6px;">
                ${{liveBadgeHtml}}
                <span>${{timeText}} · ${{art.country}}</span>
              </div>
            </div>"""

new_render_card = """          const isLiveNow = art.isLive || art.live_time || art.rel_time;
          const relTime = art.rel_time || (art.live_time && art.live_time !== '🟢 Live Stream' ? art.live_time : 'Just now');
          const liveBadgeHtml = isLiveNow 
            ? `<span class="badge" style="background:rgba(16,185,129,0.18); color:#10b981; border:1px solid #10b981; font-weight:700;">🟢 LIVE · ${{relTime}}</span> `
            : `<span class="badge" style="background:rgba(148,163,184,0.15); color:#94a3b8; border:1px solid #64748b;">${{art.date}}</span> `;

          const fieldIcon = art.field === 'ai' ? '🤖 AI' :
                            art.field === 'cyber' ? '🛡️ Cyber' :
                            art.field === 'hardware' ? '💻 Hardware' :
                            art.field === 'it' ? '☁️ IT / Cloud' : '🌐 Tech';
          const fieldBadge = `<span class="badge" style="background:rgba(59,130,246,0.12); color:#60a5fa; border:1px solid rgba(59,130,246,0.25); text-transform:uppercase; font-size:10px; font-weight:700;">${{fieldIcon}}</span>`;

          card.innerHTML = `
            <div class="article-meta">
              <div style="display:flex; align-items:center; gap:6px;">
                <span class="article-outlet">${{art.outlet}}</span>
                ${{fieldBadge}}
              </div>
              <div style="display:flex; align-items:center; gap:6px;">
                ${{liveBadgeHtml}}
                <span style="color:var(--text-dim); font-size:0.75rem;">${{art.country}}</span>
              </div>
            </div>"""

assert old_render_card in code, "Failed to find old_render_card"
code = code.replace(old_render_card, new_render_card, 1)

# 6. Add window.filterByField function
old_filter_bc = """      // --- Explicit Quick-Filter Handlers (Clear visual buttons instead of graph clicks) ---
      window.filterByBroadcast = function(outlet) {{"""

new_filter_bc = """      // --- Explicit Quick-Filter Handlers (Clear visual buttons instead of graph clicks) ---
      window.filterByField = function(field) {{
        activeFilters.field = field;
        if (field === 'ALL') {{
          document.getElementById('articleSearchInput').value = '';
          activeFilters.articleSearch = '';
        }}
        syncQuickPills();
        updateDashboard();
        const feed = document.getElementById('articlesGrid');
        if (feed) feed.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};

      window.filterByBroadcast = function(outlet) {{"""

assert old_filter_bc in code, "Failed to find old_filter_bc"
code = code.replace(old_filter_bc, new_filter_bc, 1)

# 7. Update syncQuickPills to sync #pillsField
old_sync_pills = """        // 6. Broadcast Pills
        document.querySelectorAll('#pillsBroadcast .pill-btn').forEach(b => {{
          const bc = b.getAttribute('data-broadcast');
          b.classList.toggle('active', bc === activeFilters.broadcast);
        }});"""

new_sync_pills = """        // 6. Broadcast Pills
        document.querySelectorAll('#pillsBroadcast .pill-btn').forEach(b => {{
          const bc = b.getAttribute('data-broadcast');
          b.classList.toggle('active', bc === activeFilters.broadcast);
        }});

        // 7. Tech Domain / Field Pills
        document.querySelectorAll('#pillsField .pill-btn').forEach(b => {{
          const f = b.getAttribute('data-field');
          b.classList.toggle('active', f === activeFilters.field);
        }});"""

assert old_sync_pills in code, "Failed to find old_sync_pills"
code = code.replace(old_sync_pills, new_sync_pills, 1)

# 8. Update renderActiveFiltersRibbon to show Field badge and window.removeActiveFilter
old_ribbon_bc = """        if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
          const bcLabels = {{ 'BBC': 'BBC News', 'CNN': 'CNN', 'Reuters': 'Reuters', 'Bloomberg': 'Bloomberg', 'Guardian': 'The Guardian', 'CNBC': 'CNBC', 'TechCrunch': 'TechCrunch', 'Wired': 'Wired', 'CTI': 'CTI Registries' }};
          badges.push({{ key: 'broadcast', label: `Broadcast: ${{bcLabels[activeFilters.broadcast] || activeFilters.broadcast}}` }});
        }}"""

new_ribbon_bc = """        if (activeFilters.broadcast && activeFilters.broadcast !== 'ALL') {{
          const bcLabels = {{ 'BBC': 'BBC News', 'CNN': 'CNN', 'Reuters': 'Reuters', 'Bloomberg': 'Bloomberg', 'Guardian': 'The Guardian', 'CNBC': 'CNBC', 'TechCrunch': 'TechCrunch', 'Wired': 'Wired', 'arstechnica': 'Ars Technica', 'tomshardware': "Tom's Hardware", 'CTI': 'CTI Registries' }};
          badges.push({{ key: 'broadcast', label: `Broadcast: ${{bcLabels[activeFilters.broadcast] || activeFilters.broadcast}}` }});
        }}
        if (activeFilters.field && activeFilters.field !== 'ALL') {{
          const fLabels = {{ 'ai': 'AI & Models', 'cyber': 'Cybersecurity', 'hardware': 'Hardware & Chips', 'it': 'Enterprise IT' }};
          badges.push({{ key: 'field', label: `Field: ${{fLabels[activeFilters.field] || activeFilters.field}}` }});
        }}"""

assert old_ribbon_bc in code, "Failed to find old_ribbon_bc"
code = code.replace(old_ribbon_bc, new_ribbon_bc, 1)

old_remove_bc = """        }} else if (key === 'broadcast') {{
          window.filterByBroadcast('ALL');
        }}"""

new_remove_bc = """        }} else if (key === 'broadcast') {{
          window.filterByBroadcast('ALL');
        }} else if (key === 'field') {{
          window.filterByField('ALL');
        }}"""

assert old_remove_bc in code, "Failed to find old_remove_bc"
code = code.replace(old_remove_bc, new_remove_bc, 1)

# 9. Add Countdown Timer and Force Sweep at end of script
old_init = """      populateYearFilters();
      populateCountryDropdown();
      populateSectorDropdown();
      populateVectorDropdown();
      populateSpecificYearDropdown();
      updateDashboard();
      attemptLiveSync();"""

new_init = """      populateYearFilters();
      populateCountryDropdown();
      populateSectorDropdown();
      populateVectorDropdown();
      populateSpecificYearDropdown();
      updateDashboard();
      attemptLiveSync();

      // 90-second continuous countdown for live telemetry sweep
      let sweepSecondsLeft = 90;
      const countdownEl = document.getElementById('sweepCountdown');
      setInterval(() => {{
        sweepSecondsLeft--;
        if (sweepSecondsLeft <= 0) {{
          sweepSecondsLeft = 90;
          attemptLiveSync();
        }}
        if (countdownEl) {{
          countdownEl.textContent = sweepSecondsLeft + 's';
        }}
      }}, 1000);

      window.forceLiveSweep = async function() {{
        const btn = document.getElementById('forceSweepBtn');
        if (btn) {{
          btn.innerHTML = '<span>⚡ Sweeping...</span>';
          btn.disabled = true;
        }}
        sweepSecondsLeft = 90;
        await attemptLiveSync(true);
        if (btn) {{
          btn.innerHTML = '<span>⚡ Force Live Sweep</span>';
          btn.disabled = false;
        }}
      }};"""

assert old_init in code, "Failed to find old_init"
code = code.replace(old_init, new_init, 1)

with open("generate_dashboard.py", "w", encoding="utf-8") as f:
    f.write(code)

print("generate_dashboard.py patched successfully!")
