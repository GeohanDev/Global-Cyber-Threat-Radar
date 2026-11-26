# patch_pill_design.py
import re

with open("generate_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add CSS rules for .ecosystem-pills-bar and .pill-btn before </style>
css_to_add = """
    /* Famous AI Ecosystems Quick-Pill Bar */
    .ecosystem-pills-bar {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 14px;
      padding: 10px 16px;
      background: var(--hud-box-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    }}
    .ecosystem-pills-label {{
      font-size: 0.74rem;
      font-weight: 800;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-right: 6px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      flex-shrink: 0;
    }}
    .ecosystem-live-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #3b82f6;
      display: inline-block;
      box-shadow: 0 0 6px #3b82f6;
      animation: pulseDot 2s infinite;
    }}
    .pill-btn {{
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      outline: none;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      user-select: none;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }}
    .pill-btn:hover {{
      border-color: #3b82f6;
      color: #3b82f6;
      background: rgba(59, 130, 246, 0.08);
      transform: translateY(-1px);
      box-shadow: 0 4px 10px rgba(59, 130, 246, 0.15);
    }}
    .pill-btn.active {{
      background: #2563eb !important;
      color: #ffffff !important;
      border-color: #2563eb !important;
      font-weight: 700;
      box-shadow: 0 2px 10px rgba(37, 99, 235, 0.35);
      transform: translateY(-1px);
    }}
    .pill-btn:active {{
      transform: translateY(0);
    }}
    .pill-btn[data-eco="Gemini"]:hover {{
      border-color: #4285f4;
      color: #4285f4;
      background: rgba(66, 133, 244, 0.1);
    }}
    .pill-btn[data-eco="Anthropic"]:hover {{
      border-color: #d97706;
      color: #d97706;
      background: rgba(217, 119, 6, 0.1);
    }}
    .pill-btn[data-eco="Hugging Face"]:hover {{
      border-color: #f59e0b;
      color: #f59e0b;
      background: rgba(245, 158, 11, 0.1);
    }}
    .pill-btn[data-eco="OpenAI"]:hover {{
      border-color: #10a37f;
      color: #10a37f;
      background: rgba(16, 163, 127, 0.1);
    }}
    .pill-btn[data-eco="Copilot"]:hover {{
      border-color: #0078d4;
      color: #0078d4;
      background: rgba(0, 120, 212, 0.1);
    }}
    .pill-btn[data-eco="NVIDIA"]:hover {{
      border-color: #76b900;
      color: #76b900;
      background: rgba(118, 185, 0, 0.1);
    }}
    .pill-btn[data-eco="Meta"]:hover {{
      border-color: #8b5cf6;
      color: #8b5cf6;
      background: rgba(139, 92, 246, 0.1);
    }}
"""

if ".pill-btn {{" not in content:
    # insert before </style>
    style_end = content.find("  </style>")
    if style_end != -1:
        content = content[:style_end] + css_to_add + content[style_end:]
        print("CSS inserted before </style>")
    else:
        print("Could not find </style>")

# 2. Update HTML markup for .ecosystem-pills-bar
old_html_regex = r'<div class="ecosystem-pills-bar"[^>]*>[\s\S]*?</div>\s*<!-- \/Famous AI Ecosystems Quick Filter Bar -->|<div class="ecosystem-pills-bar"[^>]*>[\s\S]*?</div>'

new_html = """<div class="ecosystem-pills-bar">
        <span class="ecosystem-pills-label">
          <span class="ecosystem-live-dot"></span>
          Famous AI Ecosystems:
        </span>
        <button class="pill-btn active" data-eco="ALL" onclick="window.filterByEcosystem('ALL')">All Cases</button>
        <button class="pill-btn" data-eco="Gemini" onclick="window.filterByEcosystem('Gemini')">✨ Google Gemini</button>
        <button class="pill-btn" data-eco="Anthropic" onclick="window.filterByEcosystem('Anthropic')">🧠 Anthropic Claude</button>
        <button class="pill-btn" data-eco="Hugging Face" onclick="window.filterByEcosystem('Hugging Face')">🤗 Hugging Face</button>
        <button class="pill-btn" data-eco="OpenAI" onclick="window.filterByEcosystem('OpenAI')">🤖 OpenAI / ChatGPT</button>
        <button class="pill-btn" data-eco="Copilot" onclick="window.filterByEcosystem('Copilot')">🪟 Microsoft Copilot</button>
        <button class="pill-btn" data-eco="NVIDIA" onclick="window.filterByEcosystem('NVIDIA')">⚡ NVIDIA</button>
        <button class="pill-btn" data-eco="Meta" onclick="window.filterByEcosystem('Meta')">🦙 Meta Llama</button>
      </div>"""

# Find the ecosystem-pills-bar div
bar_pos = content.find('<div class="ecosystem-pills-bar"')
if bar_pos != -1:
    bar_end = content.find('</div>', bar_pos) + 6
    content = content[:bar_pos] + new_html + content[bar_end:]
    print("HTML markup for ecosystem pills updated.")

# 3. Enhance window.filterByEcosystem to use data-eco selector
old_filter_fn = """      window.filterByEcosystem = function(eco) {{
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

new_filter_fn = """      window.filterByEcosystem = function(eco) {{
        activeFilters.entity = eco;
        const entDropdown = document.getElementById('filterEntity');
        if (entDropdown) entDropdown.value = eco;

        document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => b.classList.remove('active'));
        const matched = document.querySelector(`.ecosystem-pills-bar .pill-btn[data-eco="${{eco}}"]`);
        if (matched) {{
          matched.classList.add('active');
        }} else {{
          document.querySelectorAll('.ecosystem-pills-bar .pill-btn').forEach(b => {{
            if ((eco === 'ALL' && (b.getAttribute('data-eco') === 'ALL' || b.textContent.includes('All Cases'))) ||
                (eco !== 'ALL' && (b.getAttribute('data-eco') === eco || b.textContent.includes(eco)))) {{
              b.classList.add('active');
            }}
          }});
        }}
        
        updateDashboard();
        const table = document.getElementById('incidentsTable');
        if (table) table.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }};"""

if old_filter_fn in content:
    content = content.replace(old_filter_fn, new_filter_fn)
    print("filterByEcosystem function enhanced.")
else:
    print("old_filter_fn exact match not found, checking...")

with open("generate_dashboard.py", "w", encoding="utf-8") as f:
    f.write(content)

print("generate_dashboard.py patched successfully.")
