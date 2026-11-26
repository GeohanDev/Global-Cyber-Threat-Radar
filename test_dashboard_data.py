from bs4 import BeautifulSoup
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
data = json.loads(soup.find('script', {'id': 'embedded-data'}).string)

incidents = data['incidents']
print(f"Total embedded incidents: {len(incidents)}")

years = set(i['date'][:4] for i in incidents)
print(f"Years covered: {sorted(years)}")

sectors = set(i.get('target_sector') for i in incidents if i.get('target_sector'))
print(f"Total unique sectors: {len(sectors)}")

vectors = set(i.get('attack_vector') for i in incidents if i.get('attack_vector'))
print(f"Total unique vectors: {len(vectors)}")

# Verify 10-year filter logic
maxYear = 2026
tenYearIncidents = [i for i in incidents if int(i['date'][:4]) >= (maxYear - 9)]
print(f"Incidents in 10-year window (2017-2026): {len(tenYearIncidents)}")
