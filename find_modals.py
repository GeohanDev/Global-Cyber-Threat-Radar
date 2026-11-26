with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="modal' in l or 'id="incidentModal' in l or 'id="logIncidentModal' in l or 'class="modal' in l:
        print(f"{i+1}: {l.strip()[:80]}")
