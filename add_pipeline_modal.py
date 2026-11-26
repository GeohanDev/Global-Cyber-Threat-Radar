with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add Pipeline button in header controls
old_export_btn = """        <button class="hud-btn" id="btnExportData" title="Export current registry dataset (JSON)">
          <span>📥 Export</span>
        </button>"""

new_pipeline_btn = """        <button class="hud-btn" id="btnOpenPipelineModal" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4);" title="View End-to-End System Data Pipeline">
          <span>📊 Pipeline</span>
        </button>

        <button class="hud-btn" id="btnExportData" title="Export current registry dataset (JSON)">
          <span>📥 Export</span>
        </button>"""

text = text.replace(old_export_btn, new_pipeline_btn)

# 2. Add Pipeline Modal HTML
pipeline_modal_html = """  <!-- System Architecture & Data Pipeline Modal -->
  <div class="modal-overlay" id="pipelineModal">
    <div class="modal-card" style="max-width: 820px; width: 94%; max-height: 88vh; overflow-y: auto;">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span class="badge" style="background:#2563eb; color:#fff;">Architecture</span>
          <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981;">End-to-End Pipeline</span>
        </div>
        <button class="modal-close" id="btnClosePipelineModal">&times;</button>
      </div>

      <div style="padding: 10px 0 15px 0;">
        <h2 style="font-size:1.3rem; font-weight:700; color:var(--text-main); margin-bottom:6px;">
          Global AI Cyberattack Threat Radar — Data & Processing Pipeline
        </h2>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:18px;">
          Architectural schematic of raw threat ingestion, BeautifulSoup parsing, classification, live telemetry proxying, and reactive dashboard rendering.
        </p>

        <!-- Pipeline Stage 1 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#38bdf8; font-size:0.9rem;">1. Raw Threat Ingestion Layer (Tier 1 / 2 / 3 Sources)</strong>
            <span class="badge" style="background:rgba(56,189,248,0.15); color:#38bdf8;">Multi-Source Feed</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Continuous polling of authoritative public feeds: <strong>MITRE ATLAS</strong> (case studies & raw data), <strong>CyberSecurity Malaysia (CSM)</strong> & NACSA advisories, <strong>AI Incident Database (AIID)</strong>, <strong>OWASP GenAI Top 10</strong>, <strong>Microsoft Threat Intelligence (MSTIC)</strong>, <strong>Dark Reading</strong> XML, <strong>The Record</strong> RSS, and <strong>KrebsOnSecurity</strong>.
          </p>
        </div>

        <!-- Pipeline Stage 2 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#c084fc; font-size:0.9rem;">2. BeautifulSoup4 & lxml Parsing Engine</strong>
            <span class="badge" style="background:rgba(192,132,252,0.15); color:#c084fc;">python-bs4 + lxml</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            <code>soup_harvester.py</code> parses incoming XML/HTML feeds via <code>BeautifulSoup(content, 'xml')</code>. Strips CDATA tags, normalizes publication timestamps, decodes HTML entities, and applies regex word-boundary filtering on AI threat indicators (<code>\b(ai|llm|deepfake|prompt injection|mcp|agent)\b</code>).
          </p>
        </div>

        <!-- Pipeline Stage 3 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#facc15; font-size:0.9rem;">3. Taxonomy Classification & De-duplication Router</strong>
            <span class="badge" style="background:rgba(250,204,21,0.15); color:#facc15;">Atomic Incident Mapping</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Maps events to the three foundational scope categories: <strong>Cat A (Attacks USING AI)</strong>, <strong>Cat B (Attacks ON AI Systems)</strong>, and <strong>Cat C (Agentic Attacks)</strong>. Applies 1–5 Severity Rubric and de-duplicates multiple media reports into unified atomic incident IDs (<code>INC-YYYY-MM-XX</code>).
          </p>
        </div>

        <!-- Pipeline Stage 4 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#34d399; font-size:0.9rem;">4. Local Telemetry Daemon & CORS Proxy (server.py)</strong>
            <span class="badge" style="background:rgba(52,211,153,0.15); color:#34d399;">HTTP Daemon :8080</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Local daemon running outside sandbox boundaries provides <code>Access-Control-Allow-Origin: *</code>. Exposes <code>/api/live-feed</code> to serve sanitized JSON articles with live timestamps, and handles <code>/api/status</code> health checks.
          </p>
        </div>

        <!-- Pipeline Stage 5 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#60a5fa; font-size:0.9rem;">5. Browser Client Reactive Engine (index.html)</strong>
            <span class="badge" style="background:rgba(96,165,250,0.15); color:#60a5fa;">State Hydration & Filters</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Merges bundled 10-year baseline (2017–2026+), live streaming feed from <code>/api/live-feed</code>, and local continuous intake records (<code>localStorage</code>). Routes data through the 8-dimension filter matrix (Horizon, Category, Severity, Sector, Vector, Year, Country, Tier).
          </p>
        </div>

        <!-- Pipeline Stage 6 -->
        <div style="background:var(--hud-box-bg); border:1px solid var(--border-subtle); border-radius:8px; padding:14px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <strong style="color:#f43f5e; font-size:0.9rem;">6. Analytical Presentation & Interactive Delivery</strong>
            <span class="badge" style="background:rgba(244,63,94,0.15); color:#f43f5e;">UI / SOC Console</span>
          </div>
          <p style="font-size:0.82rem; color:var(--text-main); line-height:1.5;">
            Renders dynamic Chart.js hero stacked bars, 10-year milestone tables, Country exposure rankings, live reported articles feed with <strong>In-App Intel Reader Modal</strong> (100% accessible briefings), and searchable de-duplicated incident registry.
          </p>
        </div>

        <div style="display:flex; justify-content:flex-end; margin-top:16px;">
          <button class="hud-btn" id="btnDismissPipelineModal" style="background:var(--border-focus); color:#fff; padding:6px 16px;">Close Pipeline Overview</button>
        </div>
      </div>
    </div>
  </div>
"""

target_modal_anchor = '  <!-- In-App Article Intel Reader Modal (Guaranteed 100% Access) -->'
text = text.replace(target_modal_anchor, pipeline_modal_html + "\n" + target_modal_anchor)

# 3. Add JS event listeners for Pipeline Modal
old_close_readers = """      window.openArticleReaderModal = openArticleReaderModal;
      window.closeArticleReaderModal = closeArticleReaderModal;"""

new_pipeline_listeners = """      window.openArticleReaderModal = openArticleReaderModal;
      window.closeArticleReaderModal = closeArticleReaderModal;

      const pipelineModal = document.getElementById('pipelineModal');
      document.getElementById('btnOpenPipelineModal').addEventListener('click', () => {
        pipelineModal.style.display = 'flex';
        pipelineModal.classList.add('active');
      });
      document.getElementById('btnClosePipelineModal').addEventListener('click', () => {
        pipelineModal.style.display = 'none';
        pipelineModal.classList.remove('active');
      });
      document.getElementById('btnDismissPipelineModal').addEventListener('click', () => {
        pipelineModal.style.display = 'none';
        pipelineModal.classList.remove('active');
      });
      pipelineModal.addEventListener('click', (e) => {
        if (e.target.id === 'pipelineModal') {
          pipelineModal.style.display = 'none';
          pipelineModal.classList.remove('active');
        }
      });"""

text = text.replace(old_close_readers, new_pipeline_listeners)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_dashboard.py updated with Pipeline button and modal!")
