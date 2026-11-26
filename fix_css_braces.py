with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any single { or } in media_print_css with {{ and }}
bad_css = """    /* Print Optimization (for browser Save as PDF) */
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
    }"""

good_css = """    /* Print Optimization (for browser Save as PDF) */
    @media print {{
      .live-top-ticker, .livetime-hud, .filter-panel, .chart-view-toggle, .btn-reset, .modal-overlay {{
        display: none !important;
      }}
      body {{
        background: #ffffff !important;
        color: #0f172a !important;
      }}
      .dashboard-container {{
        max-width: 100% !important;
        padding: 0 !important;
      }}
      .section-card, .kpi-card, .concerns-panel {{
        box-shadow: none !important;
        border: 1px solid #cbd5e1 !important;
        page-break-inside: avoid;
        background: #ffffff !important;
      }}
      .incidents-table {{
        font-size: 8pt !important;
      }}
    }}"""

if bad_css in content:
    content = content.replace(bad_css, good_css)
    print("Fixed CSS braces in generate_dashboard.py")
else:
    print("bad_css not found")

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)
