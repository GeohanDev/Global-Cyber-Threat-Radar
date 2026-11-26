with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the single braces in the new_pipeline_listeners block
bad_code = """      const pipelineModal = document.getElementById('pipelineModal');
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

good_code = """      const pipelineModal = document.getElementById('pipelineModal');
      document.getElementById('btnOpenPipelineModal').addEventListener('click', () => {{
        pipelineModal.style.display = 'flex';
        pipelineModal.classList.add('active');
      }});
      document.getElementById('btnClosePipelineModal').addEventListener('click', () => {{
        pipelineModal.style.display = 'none';
        pipelineModal.classList.remove('active');
      }});
      document.getElementById('btnDismissPipelineModal').addEventListener('click', () => {{
        pipelineModal.style.display = 'none';
        pipelineModal.classList.remove('active');
      }});
      pipelineModal.addEventListener('click', (e) => {{
        if (e.target.id === 'pipelineModal') {{
          pipelineModal.style.display = 'none';
          pipelineModal.classList.remove('active');
        }}
      }});"""

text = text.replace(bad_code, good_code)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_dashboard.py braces fixed!")
