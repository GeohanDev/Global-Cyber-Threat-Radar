with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- LINES 1620 TO 1720 ---")
for i in range(1620, min(1720, len(lines))):
    if any(k in lines[i] for k in ['populate', 'minDataYear', 'maxDataYear', 'activeFilters']):
        print(f"{i+1}: {lines[i].strip()}")

print("\n--- LINES 1830 TO 1920 ---")
for i in range(1830, min(1920, len(lines))):
    if any(k in lines[i] for k in ['populate', 'getFilteredIncidents', 'activeFilters', 'horizon']):
        print(f"{i+1}: {lines[i].strip()}")
