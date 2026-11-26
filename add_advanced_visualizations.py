with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add .grid-3col CSS
old_grid_css = """.grid-2col {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }}
    
    @media (min-width: 1024px) {{
      .grid-2col {{
        grid-template-columns: 1.15fr 0.85fr;
      }}
    }}"""

new_grid_css = """.grid-2col {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }}
    
    @media (min-width: 1024px) {{
      .grid-2col {{
        grid-template-columns: 1.15fr 0.85fr;
      }}
    }}

    .grid-3col {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
      margin-top: 20px;
    }}

    @media (min-width: 900px) {{
      .grid-3col {{
        grid-template-columns: repeat(3, 1fr);
      }}
    }}"""

if old_grid_css in content:
    content = content.replace(old_grid_css, new_grid_css)
    print("Added .grid-3col CSS")
else:
    print("Warning: old_grid_css not found")

# 2. Add the 3 visualization cards HTML right after the Hero Chart section
hero_section_end = """      <div class="monthly-table-wrapper">
        <table class="monthly-table" id="timelineDataTable">
        </table>
      </div>
    </section>"""

viz_deck_html = """      <div class="monthly-table-wrapper">
        <table class="monthly-table" id="timelineDataTable">
        </table>
      </div>
    </section>

    <!-- Multi-Dimensional Threat Intelligence Visualizations Deck -->
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

if hero_section_end in content:
    content = content.replace(hero_section_end, viz_deck_html)
    print("Added 3 visualization cards HTML deck")
else:
    print("Warning: hero_section_end not found")

# 3. Add renderAdvancedVisualizations JS function and update updateDashboard
update_dash_target = """function updateDashboard() {{
        const filteredIncidents = getFilteredIncidents();
        const filteredArticles = getFilteredArticles();

        renderKPIs(filteredIncidents);
        renderKeyConcerns(filteredIncidents);
        renderHeroSection(filteredIncidents);
        renderCountries(filteredIncidents);"""

update_dash_repl = """function updateDashboard() {{
        const filteredIncidents = getFilteredIncidents();
        const filteredArticles = getFilteredArticles();

        renderKPIs(filteredIncidents);
        renderKeyConcerns(filteredIncidents);
        renderHeroSection(filteredIncidents);
        renderAdvancedVisualizations(filteredIncidents);
        renderCountries(filteredIncidents);"""

if update_dash_target in content:
    content = content.replace(update_dash_target, update_dash_repl)
    print("Added renderAdvancedVisualizations call inside updateDashboard")
else:
    print("Warning: update_dash_target not found")

# 4. Insert the JavaScript implementation of renderAdvancedVisualizations
js_insert_marker = "      function renderCountries(filtered) {{"

js_viz_code = """      let categoryDoughnutInstance = null;
      let vectorRadarInstance = null;
      let severityPolarInstance = null;

      function renderAdvancedVisualizations(filtered) {{
        const isLight = document.body.classList.contains('light');
        const textColor = isLight ? '#475569' : '#94a3b8';
        const gridColor = isLight ? 'rgba(0, 0, 0, 0.08)' : 'rgba(255, 255, 255, 0.08)';

        // 1. Category Doughnut Chart
        const catCanvas = document.getElementById('categoryDoughnutCanvas');
        if (catCanvas && typeof Chart !== 'undefined') {{
          let countA = 0, countB = 0, countC = 0;
          filtered.forEach(i => {{
            if (i.category.includes('A')) countA++;
            if (i.category.includes('B')) countB++;
            if (i.category.includes('C')) countC++;
          }});
          const totalCats = countA + countB + countC || 1;

          if (categoryDoughnutInstance) categoryDoughnutInstance.destroy();
          categoryDoughnutInstance = new Chart(catCanvas.getContext('2d'), {{
            type: 'doughnut',
            data: {{
              labels: ['Cat A: Using AI', 'Cat B: On AI Systems', 'Cat C: Agentic Attacks'],
              datasets: [{{
                data: [countA, countB, countC],
                backgroundColor: [
                  'rgba(56, 189, 248, 0.85)',
                  'rgba(192, 132, 252, 0.85)',
                  'rgba(52, 211, 153, 0.85)'
                ],
                borderColor: isLight ? '#ffffff' : '#0b1120',
                borderWidth: 2,
                hoverOffset: 6
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              cutout: '66%',
              plugins: {{
                legend: {{
                  position: 'bottom',
                  labels: {{ color: textColor, font: {{ size: 10 }}, boxWidth: 10, padding: 8 }}
                }},
                tooltip: {{
                  callbacks: {{
                    label: function(ctx) {{
                      const val = ctx.raw || 0;
                      const pct = Math.round((val / totalCats) * 100);
                      return ` ${{ctx.label}}: ${{val}} (${{pct}}%)`;
                    }}
                  }}
                }}
              }},
              onClick: (evt, elements) => {{
                if (elements.length > 0) {{
                  const idx = elements[0].index;
                  const targetCat = idx === 0 ? 'A' : (idx === 1 ? 'B' : 'C');
                  const select = document.getElementById('filterCategory');
                  if (select) {{
                    select.value = targetCat;
                    activeFilters.category = targetCat;
                    updateDashboard();
                  }}
                }}
              }}
            }}
          }});
        }}

        // 2. MITRE ATLAS Vector Radar Chart
        const radarCanvas = document.getElementById('vectorRadarCanvas');
        if (radarCanvas && typeof Chart !== 'undefined') {{
          const vectorMap = {{
            'Agent / MCP': 0,
            'Supply Chain': 0,
            'Prompt Injection': 0,
            'Deepfake Fraud': 0,
            'Evasion / PoC': 0,
            'Recon / Phishing': 0
          }};

          filtered.forEach(i => {{
            const v = (i.attack_vector || '').toLowerCase();
            const h = (i.headline || '').toLowerCase();
            const combo = v + ' ' + h;

            if (combo.includes('agent') || combo.includes('mcp') || combo.includes('loop')) {{
              vectorMap['Agent / MCP']++;
            }} else if (combo.includes('supply') || combo.includes('poison') || combo.includes('hugging')) {{
              vectorMap['Supply Chain']++;
            }} else if (combo.includes('prompt') || combo.includes('jailbreak') || combo.includes('direct')) {{
              vectorMap['Prompt Injection']++;
            }} else if (combo.includes('deepfake') || combo.includes('voice') || combo.includes('cfo') || combo.includes('video')) {{
              vectorMap['Deepfake Fraud']++;
            }} else if (combo.includes('evasion') || combo.includes('adversarial') || combo.includes('perturbation')) {{
              vectorMap['Evasion / PoC']++;
            }} else {{
              vectorMap['Recon / Phishing']++;
            }}
          }});

          const radarLabels = Object.keys(vectorMap);
          const radarValues = Object.values(vectorMap);

          if (vectorRadarInstance) vectorRadarInstance.destroy();
          vectorRadarInstance = new Chart(radarCanvas.getContext('2d'), {{
            type: 'radar',
            data: {{
              labels: radarLabels,
              datasets: [{{
                label: 'Threat Density',
                data: radarValues,
                backgroundColor: 'rgba(56, 189, 248, 0.2)',
                borderColor: '#38bdf8',
                borderWidth: 2,
                pointBackgroundColor: '#38bdf8',
                pointBorderColor: '#ffffff',
                pointRadius: 3.5
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{ display: false }}
              }},
              scales: {{
                r: {{
                  angleLines: {{ color: gridColor }},
                  grid: {{ color: gridColor }},
                  pointLabels: {{ color: textColor, font: {{ size: 9.5 }} }},
                  ticks: {{ display: false, backdropColor: 'transparent' }},
                  beginAtZero: true
                }}
              }}
            }}
          }});
        }}

        // 3. Severity Polar Area Chart
        const polarCanvas = document.getElementById('severityPolarCanvas');
        if (polarCanvas && typeof Chart !== 'undefined') {{
          const sevCounts = [0, 0, 0, 0, 0];
          filtered.forEach(i => {{
            const s = parseInt(i.severity);
            if (s >= 1 && s <= 5) sevCounts[s - 1]++;
          }});

          if (severityPolarInstance) severityPolarInstance.destroy();
          severityPolarInstance = new Chart(polarCanvas.getContext('2d'), {{
            type: 'polarArea',
            data: {{
              labels: ['Sev 1: PoC', 'Sev 2: Attempted', 'Sev 3: Limited', 'Sev 4: Significant', 'Sev 5: Critical'],
              datasets: [{{
                data: sevCounts,
                backgroundColor: [
                  'rgba(100, 116, 139, 0.75)',
                  'rgba(2, 132, 199, 0.75)',
                  'rgba(234, 179, 8, 0.75)',
                  'rgba(249, 115, 22, 0.75)',
                  'rgba(239, 68, 68, 0.85)'
                ],
                borderColor: isLight ? '#ffffff' : '#0b1120',
                borderWidth: 1.5
              }}]
            }},
            options: {{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {{
                legend: {{
                  position: 'bottom',
                  labels: {{ color: textColor, font: {{ size: 9 }}, boxWidth: 8, padding: 6 }}
                }}
              }},
              scales: {{
                r: {{
                  grid: {{ color: gridColor }},
                  ticks: {{ display: false, backdropColor: 'transparent' }}
                }}
              }},
              onClick: (evt, elements) => {{
                if (elements.length > 0) {{
                  const idx = elements[0].index;
                  const targetSev = String(idx + 1);
                  const select = document.getElementById('filterSeverity');
                  if (select) {{
                    select.value = targetSev;
                    activeFilters.severity = targetSev;
                    updateDashboard();
                  }}
                }}
              }}
            }}
          }});
        }}
      }}

      function renderCountries(filtered) {{"""

if js_insert_marker in content:
    content = content.replace(js_insert_marker, js_viz_code)
    print("Added renderAdvancedVisualizations function implementation")
else:
    print("Warning: js_insert_marker not found")

# 5. Update theme toggle to call updateDashboard()
content = content.replace(
    "renderHeroSection(getFilteredIncidents());\n      }});\n\n      // Dynam",
    "updateDashboard();\n      }});\n\n      // Dynam"
)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved generate_dashboard.py with advanced visualizations deck.")
