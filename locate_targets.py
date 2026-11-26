with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.article-card {' in l:
        print(f"CSS article-card at line {i+1}")
    if 'id="logIncidentModal"' in l:
        print(f"logIncidentModal at line {i+1}")
    if 'function renderArticlesFeed' in l:
        print(f"renderArticlesFeed at line {i+1}")
    if 'async function attemptLiveSync' in l:
        print(f"attemptLiveSync at line {i+1}")
