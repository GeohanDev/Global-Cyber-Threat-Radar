import http.server
import socketserver
import json
import urllib.parse
import os
import threading
import time
from datetime import datetime, timezone
import pdf_generator
import harvest_all_it_ai

PORT = 8080
DIRECTORY = "."

LATEST_FEED_LOCK = threading.Lock()
CACHED_LIVE_ARTICLES = []
LAST_HARVEST_TIME = None

def load_cached_from_disk():
    global CACHED_LIVE_ARTICLES, LAST_HARVEST_TIME
    if os.path.exists("bs4_extracted_feed.json"):
        try:
            with open("bs4_extracted_feed.json", "r", encoding="utf-8") as f:
                disk_data = json.load(f)
            items = []
            for idx, item in enumerate(disk_data, start=1):
                items.append({
                    "article_id": f"ART-LIVE-{idx:04d}",
                    "incident_id": f"INC-LIVE-{idx:04d}",
                    "headline": item.get("headline") or item.get("title", ""),
                    "title": item.get("title", ""),
                    "url": item.get("url", "#"),
                    "source_url": item.get("source_url") or item.get("url", "#"),
                    "archive_url": item.get("archive_url") or f"https://archive.is/newest/{item.get('url', '#')}",
                    "search_url": item.get("search_url") or f"https://www.google.com/search?q={urllib.parse.quote(item.get('headline') or item.get('title', ''))}",
                    "outlet": item.get("outlet", "Live Stream"),
                    "country": item.get("country", "Global"),
                    "field": item.get("field", "it"),
                    "threat_type": item.get("threat_type", "informational"),
                    "threat_label": item.get("threat_label", "🔵 Threat Intel Advisory"),
                    "category": item.get("category", ["A"]),
                    "severity": item.get("severity", 2),
                    "summary": item.get("description") or item.get("summary", ""),
                    "description": item.get("description") or item.get("summary", ""),
                    "pub_date": item.get("pub_date", ""),
                    "iso_time": item.get("iso_time", ""),
                    "epoch_time": item.get("epoch_time", 0),
                    "rel_time": item.get("rel_time", "Just now"),
                    "date": item.get("date", datetime.now().strftime("%Y-%m-%d %H:%M")),
                    "isLive": True
                })
            # Ensure newest first
            items.sort(key=lambda x: x.get("epoch_time", 0), reverse=True)
            with LATEST_FEED_LOCK:
                CACHED_LIVE_ARTICLES = items
                LAST_HARVEST_TIME = datetime.now()
            print(f"Loaded {len(items)} live tech dispatches from disk cache into memory.")
        except Exception as e:
            print("Error loading initial disk feed:", e)

def trigger_live_harvest():
    global CACHED_LIVE_ARTICLES, LAST_HARVEST_TIME
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Triggering full multi-domain 24-stream live sweep...")
    try:
        harvest_all_it_ai.run_harvest()
        load_cached_from_disk()
    except Exception as e:
        print("Error during live harvest:", e)

def continuous_harvester_thread():
    load_cached_from_disk()
    # Continuous live harvest every 90 seconds
    while True:
        time.sleep(90)
        try:
            trigger_live_harvest()
        except Exception as e:
            print("Background continuous sweep error:", e)

class ThreatRadarHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        # 1. API: Live Feed Stream
        if parsed.path == "/api/live-feed" or parsed.path == "/api/force-sweep":
            query = urllib.parse.parse_qs(parsed.query)
            if query.get("force") == ["true"] or parsed.path == "/api/force-sweep":
                # User clicked Force Live Sweep! Run harvest in background thread
                threading.Thread(target=trigger_live_harvest, daemon=True).start()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            with LATEST_FEED_LOCK:
                articles = list(CACHED_LIVE_ARTICLES)
                
            # If in-memory is empty, read from disk
            if not articles:
                load_cached_from_disk()
                with LATEST_FEED_LOCK:
                    articles = list(CACHED_LIVE_ARTICLES)
                    
            response_data = {
                "status": "success",
                "connected_sources": 24,
                "count": len(articles),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "last_sweep": LAST_HARVEST_TIME.isoformat() if LAST_HARVEST_TIME else datetime.now(timezone.utc).isoformat(),
                "articles": articles
            }
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        # 2. API: PDF Executive Export
        elif parsed.path == "/api/export-pdf":
            try:
                pdf_bytes = pdf_generator.generate_threat_radar_pdf()
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Disposition", 'attachment; filename="Global_AI_Cyberattack_Threat_Report.pdf"')
                self.send_header("Content-Length", str(len(pdf_bytes)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(pdf_bytes)
                return
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                return

        # Serve normal static files
        super().do_GET()

def run_server():
    # Start background live scraper daemon
    harvester_thread = threading.Thread(target=continuous_harvester_thread, daemon=True)
    harvester_thread.start()

    # Start HTTP server
    class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True

    with ThreadingHTTPServer(("", PORT), ThreatRadarHandler) as httpd:
        print(f"===============================================================")
        print(f"🚀 AI, Cyber, Hardware & IT Multi-Stream Live Server Running")
        print(f"👉 Local Access:      http://localhost:{PORT}")
        print(f"📡 API Live Feed:     http://localhost:{PORT}/api/live-feed")
        print(f"📥 PDF Generator:     http://localhost:{PORT}/api/export-pdf")
        print(f"🌐 Continuous Scraper: 24 Live Online RSS Feeds Active (90s cycle)")
        print(f"===============================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run_server()
