with open('generate_dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the toggle button markup in HTML
old_toggle_markup = """        <div class="chart-view-toggle">
          <button class="toggle-btn active" id="btnViewAnnual">10-Year View (By Year)</button>
          <button class="toggle-btn" id="btnViewMonthly">Monthly View (Rolling 12M)</button>
        </div>"""

new_toggle_markup = """        <div class="chart-view-toggle">
          <button class="toggle-btn active" id="btnViewAnnual">10-Year View (By Year)</button>
          <button class="toggle-btn" id="btnViewCumulative">Cumulative Surge (S-Curve)</button>
        </div>"""

if old_toggle_markup in content:
    content = content.replace(old_toggle_markup, new_toggle_markup)
    print("Updated toggle buttons markup in HTML")
else:
    print("Warning: old_toggle_markup not found, searching...")

# 2. Update the event listener
old_listeners = """      document.getElementById('btnViewAnnual').addEventListener('click', () => {{
        heroChartMode = 'annual';
        document.getElementById('btnViewAnnual').classList.add('active');
        document.getElementById('btnViewMonthly').classList.remove('active');
        renderHeroSection(getFilteredIncidents());
      }});

      document.getElementById('btnViewMonthly').addEventListener('click', () => {{
        heroChartMode = 'monthly';
        document.getElementById('btnViewMonthly').classList.add('active');
        document.getElementById('btnViewAnnual').classList.remove('active');
        renderHeroSection(getFilteredIncidents());
      }});"""

new_listeners = """      document.getElementById('btnViewAnnual').addEventListener('click', () => {{
        heroChartMode = 'annual';
        document.getElementById('btnViewAnnual').classList.add('active');
        const cumBtn = document.getElementById('btnViewCumulative');
        if (cumBtn) cumBtn.classList.remove('active');
        renderHeroSection(getFilteredIncidents());
      }});

      const btnCum = document.getElementById('btnViewCumulative');
      if (btnCum) {{
        btnCum.addEventListener('click', () => {{
          heroChartMode = 'cumulative';
          btnCum.classList.add('active');
          document.getElementById('btnViewAnnual').classList.remove('active');
          renderHeroSection(getFilteredIncidents());
        }});
      }}"""

if old_listeners in content:
    content = content.replace(old_listeners, new_listeners)
    print("Updated toggle buttons event listeners")
else:
    print("Warning: old_listeners not found")

# 3. Replace the else (monthly) block in renderHeroSection
old_monthly_code = """        }} else {{
          titleEl.textContent = 'Monthly Incident Trajectory (Rolling 12 Months)';
          const allMonths = ["2025-12","2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07","2026-08","2026-09","2026-10","2026-11"];
          const monthNames = ["Dec '25","Jan '26","Feb '26","Mar '26","Apr '26","May '26","Jun '26","Jul '26","Aug '26","Sep '26","Oct '26","Nov '26"];
          
          const countsA = Array(12).fill(0);
          const countsB = Array(12).fill(0);
          const countsC = Array(12).fill(0);
          const totals = Array(12).fill(0);

          filtered.forEach(inc => {{
            const ym = inc.date.substring(0, 7);
            const idx = allMonths.indexOf(ym);
            if (idx !== -1) {{
              totals[idx]++;
              if (inc.category.includes('A')) countsA[idx]++;
              if (inc.category.includes('B')) countsB[idx]++;
              if (inc.category.includes('C')) countsC[idx]++;
            }}
          }});

          const ma3 = [];
          for (let i = 0; i < 12; i++) {{
            const start = Math.max(0, i - 2);
            const sub = totals.slice(start, i + 1);
            const avg = sub.reduce((a, b) => a + b, 0) / sub.length;
            ma3.push(parseFloat(avg.toFixed(1)));
          }}

          let thead = '<thead><tr><th style="text-align:left; padding-left:12px;">Metric / Month</th>';
          allMonths.forEach((m, idx) => thead += `<th>${{monthNames[idx]}}</th>`);
          thead += '<th style="background:var(--table-th); color:var(--text-main);">12M Total</th></tr></thead>';

          let tbody = '<tbody>';
          tbody += '<tr class="total-row"><td style="text-align:left; padding-left:12px;">Reported Incidents</td>';
          totals.forEach(c => tbody += `<td><strong>${{c}}</strong></td>`);
          tbody += `<td><strong>${{totals.reduce((a,b)=>a+b, 0)}}</strong></td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-a);">Cat A: Using AI</td>';
          countsA.forEach(c => tbody += `<td>${{c}}</td>`);
          tbody += `<td>${{countsA.reduce((a,b)=>a+b, 0)}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-b);">Cat B: On AI Systems</td>';
          countsB.forEach(c => tbody += `<td>${{c}}</td>`);
          tbody += `<td>${{countsB.reduce((a,b)=>a+b, 0)}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-c);">Cat C: Agentic Attacks</td>';
          countsC.forEach(c => tbody += `<td>${{c}}</td>`);
          tbody += `<td>${{countsC.reduce((a,b)=>a+b, 0)}}</td></tr>`;

          tbody += '<tr style="color:#fbbf24;"><td style="text-align:left; padding-left:12px;">3-Month Moving Avg</td>';
          ma3.forEach(m => tbody += `<td>${{m}}</td>`);
          tbody += `<td>-</td></tr>`;

          tbody += '</tbody>';
          table.innerHTML = thead + tbody;

          if (heroChartInstance) heroChartInstance.destroy();
          if (typeof Chart !== 'undefined') {{
            const ctx = canvas.getContext('2d');
            heroChartInstance = new Chart(ctx, {{
              type: 'bar',
              data: {{
                labels: monthNames,
                datasets: [
                  {{
                    label: 'Cat A (Using AI)',
                    data: countsA,
                    backgroundColor: 'rgba(56, 189, 248, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 2
                  }},
                  {{
                    label: 'Cat B (On AI Systems)',
                    data: countsB,
                    backgroundColor: 'rgba(192, 132, 252, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 2
                  }},
                  {{
                    label: 'Cat C (Agentic Attacks)',
                    data: countsC,
                    backgroundColor: 'rgba(52, 211, 153, 0.85)',
                    stack: 'Stack 0',
                    borderRadius: 2
                  }},
                  {{
                    type: 'line',
                    label: '3-Month Moving Average',
                    data: ma3,
                    borderColor: '#f59e0b',
                    borderWidth: 3,
                    pointBackgroundColor: '#f59e0b',
                    pointRadius: 4,
                    tension: 0.25,
                    fill: false
                  }}
                ]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{
                    mode: 'index',
                    intersect: false,
                    backgroundColor: isLight ? '#ffffff' : '#111827',
                    titleColor: isLight ? '#0f172a' : '#ffffff',
                    bodyColor: isLight ? '#334155' : '#e2e8f0',
                    borderColor: isLight ? '#cbd5e1' : '#374151',
                    borderWidth: 1
                  }}
                }},
                scales: {{
                  x: {{
                    stacked: true,
                    grid: {{ color: gridColor }},
                    ticks: {{ color: textColor, font: {{ size: 11 }} }}
                  }},
                  y: {{
                    stacked: true,
                    beginAtZero: true,
                    grid: {{ color: gridColor }},
                    ticks: {{ color: textColor, font: {{ size: 11 }} }}
                  }}
                }}
              }}
            }});
          }}
        }}"""

new_cumulative_code = """        }} else {{
          titleEl.textContent = 'Cumulative Threat Surge Trajectory (10-Year Exponential S-Curve, 2017–2026+)';
          
          const is10Y = (activeFilters.horizon === '10Y' || activeFilters.horizon === 'ALL');
          const startYear = is10Y 
            ? Math.max(minDataYear, maxDataYear - 9)
            : Math.max(minDataYear, maxDataYear - 4);

          const years = [];
          for (let y = startYear; y <= maxDataYear; y++) {{
            years.push(String(y));
          }}

          const annualCountsA = Array(years.length).fill(0);
          const annualCountsB = Array(years.length).fill(0);
          const annualCountsC = Array(years.length).fill(0);
          const annualTotals = Array(years.length).fill(0);

          filtered.forEach(inc => {{
            const yr = inc.date.substring(0, 4);
            const idx = years.indexOf(yr);
            if (idx !== -1) {{
              annualTotals[idx]++;
              if (inc.category.includes('A')) annualCountsA[idx]++;
              if (inc.category.includes('B')) annualCountsB[idx]++;
              if (inc.category.includes('C')) annualCountsC[idx]++;
            }}
          }});

          // Compute cumulative running totals
          const cumTotals = [];
          const cumA = [];
          const cumB = [];
          const cumC = [];
          let runTot = 0, runA = 0, runB = 0, runC = 0;

          for (let i = 0; i < years.length; i++) {{
            runTot += annualTotals[i];
            runA += annualCountsA[i];
            runB += annualCountsB[i];
            runC += annualCountsC[i];
            cumTotals.push(runTot);
            cumA.push(runA);
            cumB.push(runB);
            cumC.push(runC);
          }}

          let thead = '<thead><tr><th style="text-align:left; padding-left:12px;">Cumulative Milestone / Year</th>';
          years.forEach(yr => thead += `<th>${{yr}}</th>`);
          thead += '<th style="background:var(--table-th); color:var(--text-main);">Current Total</th></tr></thead>';

          let tbody = '<tbody>';
          tbody += '<tr class="total-row"><td style="text-align:left; padding-left:12px;">Cumulative Incidents (Surge)</td>';
          cumTotals.forEach(c => tbody += `<td><strong>${{c}}</strong></td>`);
          tbody += `<td><strong style="color:var(--border-focus);">${{cumTotals[cumTotals.length - 1] || 0}}</strong></td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--text-dim);">New Additions in Year</td>';
          annualTotals.forEach(c => tbody += `<td>+${{c}}</td>`);
          tbody += `<td>+${{annualTotals.reduce((a,b)=>a+b, 0)}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-a);">Cat A Cumulative (Using AI)</td>';
          cumA.forEach(c => tbody += `<td>${{c}}</td>`);
          tbody += `<td>${{cumA[cumA.length - 1] || 0}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-b);">Cat B Cumulative (On AI Systems)</td>';
          cumB.forEach(c => tbody += `<td>${{c}}</td>`);
          tbody += `<td>${{cumB[cumB.length - 1] || 0}}</td></tr>`;

          tbody += '<tr><td style="text-align:left; padding-left:12px; color:var(--cat-c);">Cat C Cumulative (Agentic Attacks)</td>';
          cumC.forEach(c => tbody += `<td>${{c}}</td>`);
          tbody += `<td>${{cumC[cumC.length - 1] || 0}}</td></tr>`;

          tbody += '</tbody>';
          table.innerHTML = thead + tbody;

          if (heroChartInstance) heroChartInstance.destroy();
          if (typeof Chart !== 'undefined') {{
            const ctx = canvas.getContext('2d');
            heroChartInstance = new Chart(ctx, {{
              type: 'line',
              data: {{
                labels: years,
                datasets: [
                  {{
                    label: 'Cumulative Total (All Incidents)',
                    data: cumTotals,
                    borderColor: '#f59e0b',
                    backgroundColor: 'rgba(245, 158, 11, 0.15)',
                    borderWidth: 3.5,
                    pointBackgroundColor: '#f59e0b',
                    pointRadius: 5,
                    tension: 0.35,
                    fill: true
                  }},
                  {{
                    label: 'Cat A Cumulative (Using AI)',
                    data: cumA,
                    borderColor: 'rgba(56, 189, 248, 1)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 4],
                    pointRadius: 3,
                    tension: 0.3
                  }},
                  {{
                    label: 'Cat B Cumulative (On AI Systems)',
                    data: cumB,
                    borderColor: 'rgba(192, 132, 252, 1)',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 4],
                    pointRadius: 3,
                    tension: 0.3
                  }},
                  {{
                    label: 'Cat C Cumulative (Agentic Attacks)',
                    data: cumC,
                    borderColor: 'rgba(52, 211, 153, 1)',
                    backgroundColor: 'transparent',
                    borderWidth: 2.5,
                    pointRadius: 4,
                    tension: 0.3
                  }}
                ]
              }},
              options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                  legend: {{ display: false }},
                  tooltip: {{
                    mode: 'index',
                    intersect: false,
                    backgroundColor: isLight ? '#ffffff' : '#111827',
                    titleColor: isLight ? '#0f172a' : '#ffffff',
                    bodyColor: isLight ? '#334155' : '#e2e8f0',
                    borderColor: isLight ? '#cbd5e1' : '#374151',
                    borderWidth: 1
                  }}
                }},
                scales: {{
                  x: {{
                    grid: {{ color: gridColor }},
                    ticks: {{ color: textColor, font: {{ size: 12 }} }}
                  }},
                  y: {{
                    beginAtZero: true,
                    grid: {{ color: gridColor }},
                    ticks: {{ color: textColor, font: {{ size: 11 }} }}
                  }}
                }}
              }}
            }});
          }}
        }}"""

if old_monthly_code in content:
    content = content.replace(old_monthly_code, new_cumulative_code)
    print("Replaced monthly rolling code with Cumulative Surge (S-Curve) trajectory")
else:
    print("Warning: old_monthly_code not matched exactly!")

with open('generate_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved generate_dashboard.py.")
