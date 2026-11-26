with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for id_name in ['filterSector', 'filterVector', 'filterYear', 'filterCountry', 'filterHorizon']:
    target = f"document.getElementById('{id_name}').addEventListener"
    print(f"{id_name} listener present:", target in text)
