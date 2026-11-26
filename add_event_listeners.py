with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_listeners_block = """      document.getElementById('filterTier').addEventListener('change', e => {{
        activeFilters.tier = e.target.value;
        updateDashboard();
      }});"""

new_listeners_block = """      document.getElementById('filterTier').addEventListener('change', e => {{
        activeFilters.tier = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterSector').addEventListener('change', e => {{
        activeFilters.sector = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterVector').addEventListener('change', e => {{
        activeFilters.vector = e.target.value;
        updateDashboard();
      }});

      document.getElementById('filterYear').addEventListener('change', e => {{
        activeFilters.year = e.target.value;
        updateDashboard();
      }});"""

text = text.replace(old_listeners_block, new_listeners_block)

old_reset_block = """      document.getElementById('btnResetFilters').addEventListener('click', () => {{
        activeFilters = {{
          horizon: '5Y',
          category: 'ALL',
          severity: 'ALL',
          country: 'ALL',
          tier: 'ALL',
          articleSearch: '',
          incidentSearch: '',
          sortCol: 'date',
          sortAsc: false
        }};
        document.getElementById('filterHorizon').value = '5Y';
        document.getElementById('filterCategory').value = 'ALL';
        document.getElementById('filterSeverity').value = 'ALL';
        document.getElementById('filterCountry').value = 'ALL';
        document.getElementById('filterTier').value = 'ALL';
        document.getElementById('articleSearchInput').value = '';
        document.getElementById('incidentSearchInput').value = '';
        updateDashboard();
      }});"""

new_reset_block = """      document.getElementById('btnResetFilters').addEventListener('click', () => {{
        activeFilters = {{
          horizon: '10Y',
          category: 'ALL',
          severity: 'ALL',
          country: 'ALL',
          sector: 'ALL',
          vector: 'ALL',
          year: 'ALL',
          tier: 'ALL',
          articleSearch: '',
          incidentSearch: '',
          sortCol: 'date',
          sortAsc: false
        }};
        document.getElementById('filterHorizon').value = '10Y';
        document.getElementById('filterCategory').value = 'ALL';
        document.getElementById('filterSeverity').value = 'ALL';
        document.getElementById('filterSector').value = 'ALL';
        document.getElementById('filterVector').value = 'ALL';
        document.getElementById('filterYear').value = 'ALL';
        document.getElementById('filterCountry').value = 'ALL';
        document.getElementById('filterTier').value = 'ALL';
        document.getElementById('articleSearchInput').value = '';
        document.getElementById('incidentSearchInput').value = '';
        updateDashboard();
      }});"""

text = text.replace(old_reset_block, new_reset_block)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_dashboard.py event listeners added!")
