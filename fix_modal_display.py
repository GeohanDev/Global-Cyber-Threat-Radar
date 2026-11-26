with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add .modal-overlay.active CSS rule
old_overlay_css = """.modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }}"""

new_overlay_css = """.modal-overlay {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }}
    .modal-overlay.active {{
      display: flex !important;
    }}"""

text = text.replace(old_overlay_css, new_overlay_css)

# 2. Update openArticleReaderModal and close handlers
old_open_modal = """        modal.classList.add('active');
      }}
      window.openArticleReaderModal = openArticleReaderModal;

      document.getElementById('btnCloseArticleModal').addEventListener('click', () => {{
        document.getElementById('articleReaderModal').classList.remove('active');
      }});
      document.getElementById('articleReaderModal').addEventListener('click', (e) => {{
        if (e.target.id === 'articleReaderModal') {{
          document.getElementById('articleReaderModal').classList.remove('active');
        }}
      }});"""

new_open_modal = """        modal.style.display = 'flex';
        modal.classList.add('active');
      }}

      function closeArticleReaderModal() {{
        const modal = document.getElementById('articleReaderModal');
        if (modal) {{
          modal.style.display = 'none';
          modal.classList.remove('active');
        }}
      }}

      window.openArticleReaderModal = openArticleReaderModal;
      window.closeArticleReaderModal = closeArticleReaderModal;

      document.getElementById('btnCloseArticleModal').addEventListener('click', closeArticleReaderModal);
      document.getElementById('articleReaderModal').addEventListener('click', (e) => {{
        if (e.target.id === 'articleReaderModal') {{
          closeArticleReaderModal();
        }}
      }});"""

text = text.replace(old_open_modal, new_open_modal)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_dashboard.py updated with modal display flex and active class.")
