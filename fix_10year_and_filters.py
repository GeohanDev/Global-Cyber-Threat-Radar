with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix activeFilters initial state in generate_dashboard.py
old_af = """      let heroChartMode = 'annual';
      let activeFilters = {{
        horizon: '5Y',
        category: 'ALL',
        severity: 'ALL',
        country: 'ALL',
        tier: 'ALL',
        articleSearch: '',
        incidentSearch: '',
        sortCol: 'date',
        sortAsc: false
      }};"""

new_af = """      let heroChartMode = 'annual';
      let activeFilters = {{
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
      }};"""

text = text.replace(old_af, new_af)

# 2. Fix populateYearFilters so it keeps the 4 base options (10Y, 5Y, 12M, ALL)
old_pyf = """      function populateYearFilters() {{
        const select = document.getElementById('filterHorizon');
        while (select.options.length > 3) {{
          select.remove(3);
        }}"""

new_pyf = """      function populateYearFilters() {{
        const select = document.getElementById('filterHorizon');
        while (select.options.length > 4) {{
          select.remove(4);
        }}"""

text = text.replace(old_pyf, new_pyf)

# 3. Call all dropdown population functions at initialization and form submit
old_init = """      populateYearFilters();
      populateCountryDropdown();
      updateDashboard();
      attemptLiveSync();"""

new_init = """      populateYearFilters();
      populateCountryDropdown();
      populateSectorDropdown();
      populateVectorDropdown();
      populateSpecificYearDropdown();
      updateDashboard();
      attemptLiveSync();"""

text = text.replace(old_init, new_init)

old_form_init = """        populateYearFilters();
        populateCountryDropdown();
        updateDashboard();
        modal.style.display = 'none';"""

new_form_init = """        populateYearFilters();
        populateCountryDropdown();
        populateSectorDropdown();
        populateVectorDropdown();
        populateSpecificYearDropdown();
        updateDashboard();
        modal.style.display = 'none';"""

text = text.replace(old_form_init, new_form_init)

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("generate_dashboard.py fixed successfully!")
