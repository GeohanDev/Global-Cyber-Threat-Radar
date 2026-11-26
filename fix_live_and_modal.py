with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Attach openArticleReaderModal to window
old_fn = """        modal.classList.add('active');
      }}"""

new_fn = """        modal.classList.add('active');
      }}
      window.openArticleReaderModal = openArticleReaderModal;"""

code = code.replace(old_fn, new_fn, 1)

# 2. Update getFilteredArticles so live articles are never excluded
old_filter = """      function getFilteredArticles() {{
        const validIncidentIds = new Set(getFilteredIncidents().map(i => i.incident_id));
        return allArticles.filter(art => {{
          if (!validIncidentIds.has(art.incident_id)) return false;"""

new_filter = """      function getFilteredArticles() {{
        const validIncidentIds = new Set(getFilteredIncidents().map(i => i.incident_id));
        return allArticles.filter(art => {{
          if (!art.isLive && !validIncidentIds.has(art.incident_id)) return false;"""

code = code.replace(old_filter, new_filter)

# 3. In attemptLiveSync, also add incident for live articles so all views stay in sync
old_sync_each = """              liveData.articles.forEach(art => {{
                if (!existingUrls.has(art.url)) {{
                  art.isLive = true;
                  art.live_time = '🟢 Live Stream';
                  allArticles.unshift(art);
                  existingUrls.add(art.url);
                  newArticlesCount++;
                }}
              }});"""

new_sync_each = """              liveData.articles.forEach(art => {{
                if (!existingUrls.has(art.url)) {{
                  art.isLive = true;
                  art.live_time = '🟢 Live Stream';
                  allArticles.unshift(art);
                  existingUrls.add(art.url);
                  newArticlesCount++;

                  allIncidents.unshift({{
                    incident_id: art.incident_id,
                    date: art.date ? art.date.slice(0, 10) : '2026-11-19',
                    headline: art.headline,
                    source_url: art.url,
                    source_tier: 3,
                    category: art.category || ['A'],
                    attack_vector: 'AI Threat Intelligence Live Feed',
                    target_sector: 'Enterprise & Technology',
                    country: art.country || 'Global',
                    severity: art.severity || 3,
                    confidence: 'high',
                    outlet: art.outlet
                  }});
                }}
              }});"""

code = code.replace(old_sync_each, new_sync_each)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("generate_dashboard.py updated with window.openArticleReaderModal and live incident ingestion.")
