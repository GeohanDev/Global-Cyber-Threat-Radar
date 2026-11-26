with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update .digital-clock-box CSS
old_clock_box_css = """.digital-clock-box {{
      background: var(--hud-box-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 6px 12px;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      min-width: 170px;
    }}"""

new_clock_box_css = """.digital-clock-box {{
      background: var(--hud-box-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 6px 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      min-width: 180px;
    }}"""

if old_clock_box_css in content:
    content = content.replace(old_clock_box_css, new_clock_box_css)
    print("Updated .digital-clock-box CSS to center alignment")
else:
    print("Warning: old_clock_box_css not found")

# 2. Update .clock-time and .clock-sub CSS
old_clock_time_css = """.clock-time {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--border-focus);
      letter-spacing: 0.05em;
      line-height: 1.1;
    }}

    .clock-sub {{
      font-size: 0.68rem;
      color: var(--text-dim);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      margin-top: 3px;
    }}"""

new_clock_time_css = """.clock-time {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 1.12rem;
      font-weight: 700;
      color: var(--border-focus);
      letter-spacing: 0.05em;
      line-height: 1.1;
      text-align: center;
      width: 100%;
    }}

    .clock-sub {{
      font-size: 0.68rem;
      color: var(--text-dim);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      margin-top: 3px;
      text-align: center;
      width: 100%;
    }}"""

if old_clock_time_css in content:
    content = content.replace(old_clock_time_css, new_clock_time_css)
    print("Updated .clock-time and .clock-sub CSS to center text")
else:
    print("Warning: old_clock_time_css not found")

# 3. Update the sweep countdown box style
content = content.replace(
    '<div class="digital-clock-box" style="align-items: flex-start; min-width: 140px;">',
    '<div class="digital-clock-box" style="align-items: center; text-align: center; min-width: 140px;">'
)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved generate_dashboard.py with centered clock box.")
