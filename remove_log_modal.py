import re

with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove button from header
btn_markup = """        <button class="hud-btn" id="btnOpenLogModal" style="background: rgba(16, 185, 129, 0.15); color: #10b981; border-color: #10b981;" title="Log a new incident (continuous future ingestion)">
          <span>+ Log Incident</span>
        </button>"""

if btn_markup in content:
    content = content.replace(btn_markup, "")
    print("Removed btnOpenLogModal from header markup")
else:
    print("Warning: btn_markup not found exactly, trying regex...")
    content = re.sub(r'<button class="hud-btn" id="btnOpenLogModal"[^>]*>[\s\S]*?<\/button>', '', content)

# 2. Remove logIncidentModal markup
modal_regex = r'<!-- Incident Intake Modal \(For continuous logging of future incidents\) -->\s*<div class="modal-overlay" id="logIncidentModal">[\s\S]*?<\/div>\s*<\/div>'
if re.search(modal_regex, content):
    content = re.sub(modal_regex, '', content)
    print("Removed logIncidentModal HTML markup")
else:
    print("Warning: modal_regex not matched, searching for logIncidentModal...")
    pos = content.find('id="logIncidentModal"')
    if pos != -1:
        start = content.rfind('<div class="modal-overlay"', 0, pos)
        end = content.find('</div>\n  </div>', pos) + len('</div>\n  </div>')
        content = content[:start] + content[end:]
        print("Removed logIncidentModal via substring slice")

# 3. Update renderKeyConcerns bullet 5
old_li5 = "li5.innerHTML = `<strong>Forward Continuity:</strong> Ingestion engine automatically active for ${{maxDataYear + 1}}+ incidents via live feed sync or <a onclick=\"document.getElementById('logIncidentModal').style.display='flex'\">+ Log Incident</a> button.`;"
new_li5 = "li5.innerHTML = `<strong>Forward Continuity:</strong> Ingestion engine automatically active for ${{maxDataYear + 1}}+ incidents via automated multithreaded BeautifulSoup threat scraping and live telemetry sync.`;"

if old_li5 in content:
    content = content.replace(old_li5, new_li5)
    print("Updated li5 in renderKeyConcerns")

# 4. Remove JS listeners for logIncidentModal
js_block_regex = r'const modal = document\.getElementById\(\'logIncidentModal\'\);[\s\S]*?alert\(\'Incident successfully logged and persisted! Horizon statistics updated\.\'\);\s*\}\);'
if re.search(js_block_regex, content):
    content = re.sub(js_block_regex, '// Manual log modal removed in favor of automated live stream scraping daemon', content)
    print("Removed JS modal listeners")
else:
    print("Warning: js_block_regex not matched!")

# 5. Update methodology section text
content = content.replace(
    'live feed parsers and the <code>+ Log Incident</code> intake store them in browser <code>localStorage</code>, dynamically extending time horizons without code alteration.',
    'automated live feed parsers and multithreaded scraping daemons continuously ingest incoming zero-day events, dynamically extending time horizons without requiring manual entry.'
)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved generate_dashboard.py after removing log modal.")
