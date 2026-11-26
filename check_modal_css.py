with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\.modal-overlay[^{]*\{[^}]*\}', text)
for m in matches:
    print(m)

matches2 = re.findall(r'\.modal-card[^{]*\{[^}]*\}', text)
for m in matches2:
    print(m)
