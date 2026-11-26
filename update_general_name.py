# update_general_name.py
import re

# 1. Update generate_dashboard.py
with open("generate_dashboard.py", "r", encoding="utf-8") as f:
    dash_text = f.read()

# Replace BeautifulSoup in statusWidget
old_status = "statusWidget.textContent = `Live Telemetry Active (${{allArticles.length}} Articles Ingested via BeautifulSoup)`;"
new_status = "statusWidget.textContent = `Live Telemetry Active (${{allArticles.length}} Global Dispatches Ingested)`;"

if old_status in dash_text:
    dash_text = dash_text.replace(old_status, new_status)
    print("Updated statusWidget in generate_dashboard.py")
else:
    print("Could not find exact old_status, checking with regex...")
    dash_text = re.sub(
        r"statusWidget\.textContent\s*=\s*`Live Telemetry Active \(\$\{\{allArticles\.length\}\} Articles Ingested via BeautifulSoup\)`",
        "statusWidget.textContent = `Live Telemetry Active (${{allArticles.length}} Global Dispatches Ingested)`",
        dash_text
    )

# Replace initial loading state
dash_text = dash_text.replace(
    '<span id="sourceStatusText">Testing Live CORS Feeds...</span>',
    '<span id="sourceStatusText">Connecting to Live Threat Intelligence Feed...</span>'
)

# Replace pipeline modal technical references
dash_text = dash_text.replace(
    "Architectural schematic of raw threat ingestion, BeautifulSoup parsing, classification, live telemetry proxying, and reactive dashboard rendering.",
    "Architectural schematic of raw threat ingestion, automated stream parsing, classification, live telemetry proxying, and reactive dashboard rendering."
)

dash_text = dash_text.replace(
    '<strong style="color:#c084fc; font-size:0.9rem;">2. BeautifulSoup4 & lxml Parsing Engine</strong>',
    '<strong style="color:#c084fc; font-size:0.9rem;">2. Automated Intelligence Ingestion Engine</strong>'
)

dash_text = dash_text.replace(
    "<code>soup_harvester.py</code> parses incoming XML/HTML feeds via <code>BeautifulSoup(content, 'xml')</code>. Strips CDATA tags, normalizes publication timestamps, decodes HTML entities, and maps telemetry into structured threat registries.",
    "Automated syndication parser ingests incoming XML/HTML threat intelligence feeds. Strips CDATA tags, normalizes publication timestamps, decodes HTML entities, and maps telemetry into structured threat registries."
)

# Replace summary bullet point
dash_text = dash_text.replace(
    "incidents via automated multithreaded BeautifulSoup threat scraping and live telemetry sync.",
    "incidents via automated multithreaded global threat intelligence harvesting and live telemetry sync."
)

with open("generate_dashboard.py", "w", encoding="utf-8") as f:
    f.write(dash_text)
print("generate_dashboard.py updated.")

# 2. Update pdf_generator.py
with open("pdf_generator.py", "r", encoding="utf-8") as f:
    pdf_text = f.read()

pdf_text = pdf_text.replace(
    "Engine: BeautifulSoup4 CTI Stream",
    "Engine: Automated Global CTI Stream"
)

pdf_text = pdf_text.replace(
    "The radar integrates live polling from BeautifulSoup4 scrapers over The Record, Dark Reading, SecurityWeek, and MITRE ATLAS",
    "The radar integrates live polling from automated global threat intelligence feeds over The Record, Dark Reading, SecurityWeek, and MITRE ATLAS"
)

pdf_text = pdf_text.replace(
    "Harvested via Python BeautifulSoup4 and lxml from Tier-1 registries",
    "Harvested via automated continuous syndication harvesting from Tier-1 registries"
)

with open("pdf_generator.py", "w", encoding="utf-8") as f:
    f.write(pdf_text)
print("pdf_generator.py updated.")
