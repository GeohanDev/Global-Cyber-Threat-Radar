with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the button markup
content = content.replace(
    '<button class="hud-btn" id="btnExportData" title="Export current registry dataset (JSON)">\n          <span>📥 Export</span>\n        </button>',
    '<button class="hud-btn" id="btnExportData" style="background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);" title="Download Official Threat Intelligence Report (PDF)">\n          <span>📥 Export PDF</span>\n        </button>'
)

# 2. Add @media print styles
media_print_css = """
    /* Print Optimization (for browser Save as PDF) */
    @media print {
      .live-top-ticker, .livetime-hud, .filter-panel, .chart-view-toggle, .btn-reset, .modal-overlay {
        display: none !important;
      }
      body {
        background: #ffffff !important;
        color: #0f172a !important;
      }
      .dashboard-container {
        max-width: 100% !important;
        padding: 0 !important;
      }
      .section-card, .kpi-card, .concerns-panel {
        box-shadow: none !important;
        border: 1px solid #cbd5e1 !important;
        page-break-inside: avoid;
        background: #ffffff !important;
      }
      .incidents-table {
        font-size: 8pt !important;
      }
    }
  </style>"""

content = content.replace("  </style>", media_print_css)

# 3. Update the event listener
old_listener = """      document.getElementById('btnExportData').addEventListener('click', () => {{
        const exportObj = {{
          exported_at: new Date().toISOString(),
          incidents: allIncidents,
          articles: allArticles
        }};
        const blob = new Blob([JSON.stringify(exportObj, null, 2)], {{ type: 'application/json' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ai_threat_radar_dataset_${{new Date().toISOString().substring(0, 10)}}.json`;
        a.click();
        URL.revokeObjectURL(url);
      }});"""

new_listener = """      document.getElementById('btnExportData').addEventListener('click', async () => {{
        const btn = document.getElementById('btnExportData');
        const originalHtml = btn.innerHTML;
        btn.innerHTML = '<span>⏳ Generating PDF...</span>';
        btn.disabled = true;

        try {{
          const horizon = (typeof activeFilters !== 'undefined' && activeFilters.horizon) ? activeFilters.horizon : '10Y';
          const url = `/api/export-pdf?horizon=${{encodeURIComponent(horizon)}}`;
          const resp = await fetch(url);
          if (!resp.ok) throw new Error('PDF Generation endpoint returned ' + resp.status);

          const blob = await resp.blob();
          const blobUrl = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = blobUrl;
          a.download = `Global_AI_Cyberattack_Threat_Report_${{horizon}}_${{new Date().toISOString().substring(0, 10)}}.pdf`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(blobUrl);
        }} catch (err) {{
          console.warn('Backend PDF endpoint error, falling back to print dialog:', err);
          window.print();
        }} finally {{
          btn.innerHTML = originalHtml;
          btn.disabled = false;
        }}
      }});"""

if old_listener in content:
    content = content.replace(old_listener, new_listener)
    print("Successfully replaced btnExportData listener")
else:
    print("Warning: old_listener not matched exactly, looking for substring...")
    pos = content.find("btnExportData').addEventListener")
    print("Found pos:", pos)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved generate_dashboard.py with PDF export support.")
