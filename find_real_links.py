# find_real_links.py
import urllib.request
import re

req = urllib.request.Request('https://atlas.mitre.org/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode('utf-8')
        links = re.findall(r'href="([^"]+)"', html)
        for l in set(links):
            if any(k in l.lower() for k in ['case', 'study', 'matrices', 'navigator', 'mitre']):
                print(l)
except Exception as e:
    print('Error:', e)
