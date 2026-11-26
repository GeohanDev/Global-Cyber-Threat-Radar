# update_docs_label.py
with open("DOCUMENTATION.md", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    "Live Telemetry Active (X Articles Ingested via BeautifulSoup)",
    "Live Telemetry Active (X Global Dispatches Ingested)"
)

with open("DOCUMENTATION.md", "w", encoding="utf-8") as f:
    f.write(text)

import subprocess
subprocess.run(["python", "convert_doc_to_word.py"], check=True)
print("Documentation regenerated.")
