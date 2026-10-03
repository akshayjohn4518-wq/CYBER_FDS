# Global Cybersecurity Threats Analytics Dashboard (2015–2024)
### Course: Fundamentals of Data Science | Owner: REDDY — CSE-QE-2A | Version 1.1

An interactive, dark-mode cybersecurity visual intelligence platform built with **Python**, **Streamlit**, **Pandas**, and **Plotly**. Transforms longitudinal threat data (1,000 incidents from 2015 to 2024 across 10 sovereign nations) into actionable analytical intelligence.

---

## 🚀 Key Features

### 1. Centralized Global Filtering System (F1–F11)
- **Shared Filter Engine:** Single source of truth. Every KPI, chart, and data table responds synchronously to the shared filter state.
- **AND/OR Filter Logic:** OR logic within multi-select dimensions; AND logic across dimensions.
- **11 Filtering Controls:**
  - `F1`: Country (Multi-select across 10 sovereign nations)
  - `F2`: Year Range (Slider: 2015 – 2024)
  - `F3`: Attack Type (Multi-select: Ransomware, DDoS, Malware, Phishing, SQL Injection, MitM)
  - `F4`: Target Industry (Multi-select: Banking, IT, Healthcare, Government, Retail, etc.)
  - `F5`: Attack Source (Multi-select: Nation-state, Hacker Group, Insider, Unknown)
  - `F6`: Security Vulnerability (Multi-select: Zero-day, Unpatched Software, Weak Passwords, Social Engineering)
  - `F7`: Defense Mechanism (Multi-select: Firewall, Encryption, VPN, Antivirus, AI-based Detection)
  - `F8`: Severity Rating (Multi-select: Low, Medium, High)
  - `F9`: Financial Loss (Range slider: $0.5M – $100.0M)
  - `F10`: Incident Resolution Time (Range slider: 1 – 72 Hours)
  - `F11`: Recorded Affected Users (Range slider: 400 – 1,000,000 users)
- **Active Filter Chips & Reset:** Visual badges display currently active filter parameters, with a one-click reset to restore the full baseline.
- **Graceful State Handling:**
  - **Small Sample Warning:** Automatically notifies users when sample size is below 30 incidents (`n < 30`).
  - **Zero-Result State:** Clean, non-crashing empty screen with a prominent "Reset All Filters" action button.

---

### 2. Executive Overview & Baseline KPIs
Displays 6 core performance metrics + sovereign countries represented, with **explicit non-temporal comparisons** against the full 1,000-incident baseline dataset (PRD Section 7):
1. **Total Incidents:** Filtered record count vs full baseline (1,000).
2. **Total Financial Loss:** Cumulative economic damage ($M) vs full baseline ($50,380.7M).
3. **Average Loss / Incident:** Mean loss ($M) per incident vs full baseline ($50.38M).
4. **Recorded Affected Users:** Cumulative recorded incident footprint vs full baseline (499.7M).
5. **Average Resolution Time:** Mean response hours vs full baseline (37.2 hrs).
6. **High-Severity Share:** Percentage of incidents in top loss tertile vs full baseline (33.3%).
7. **Countries Represented:** Distinct sovereign nations present in filtered cohort.

---

### 3. Complete Visualization Suite (All 11 Modules)
All visualizations feature hover tooltips, sample size indicators (`n = ...`), clear units, responsive layouts, and an expandable **"View Underlying Data"** table:

| Chart ID | Visualization Title | Type | Description |
|---|---|---|---|
| **Chart 01** | Total Financial Loss by Country | Horizontal Bar Chart | Cumulative loss in $M per country, sorted descending. |
| **Chart 02** | Yearly Incident & Loss Trend | Dual-Axis Line Chart | Longitudinal frequency (left) vs cumulative loss (right). |
| **Chart 03** | Distribution Analysis | Histogram + Marginal Boxplot | Frequency spreads with mean/median lines; toggle between Loss ($M) and Resolution Time (hrs). |
| **Chart 04** | Attack Type Distribution | Donut Chart | Proportional breakdown across 6 attack modalities with high-contrast palette. |
| **Chart 05** | Affected Users vs Financial Loss | Scatter Plot | Correlation inspection with optional Log-scale toggle and attack-type coloring. |
| **Chart 06** | Financial Loss by Target Industry | Box Plot | Industry dispersion sorted descending by median loss. |
| **Chart 07** | Attack Type × Country Matrix | Heatmap | Cross-tabulated mean financial loss ($M) with preserved missing cells. |
| **Chart 08** | Industry Loss by Threat Actor Source | Grouped Bar Chart | Sector vulnerability segmented by Nation-state, Hacker Group, Insider, and Unknown. |
| **Chart 09** | Defense Mechanism Frequency | Donut Chart | Deployment share across defensive countermeasures with center incident count. |
| **Chart 10** | Yearly Attack Vector Trajectory | Stacked Area Chart | 10-year longitudinal evolution of cyber threat types. |
| **Chart 11** | Geographic Financial Impact | Choropleth Map | Sovereign nation loss heat map with Natural Earth projection. |

---

### 4. Incident Explorer & Telemetry Export
- **Multi-Field Text Search:** Real-time search across Country, Attack Type, Industry, Actor, Vulnerability, and Defense.
- **Flexible Sorting:** Sort by any metric (Country, Year, Loss, Users, Resolution Time, Severity).
- **Interactive Pagination:** Configure display density (10, 25, 50, or 100 rows per page) with page jump and navigation buttons.
- **Full Filtered CSV Export:** Download the entire filtered record set (all rows, not just the active page) with a single click.
- **Country Summary Export:** Download aggregated country-level metrics (incidents, mean loss, primary attack vectors).
- **Highest-Impact Callout:** Identifies peak financial exposure events strictly within the active filter scope.

---

## 🛠️ Project Structure

```text
FDS/
│
├── .streamlit/
│   └── config.toml          # Dark theme tokens, port & server configs
├── app.py                   # Main Streamlit dashboard application
├── requirements.txt         # Project dependencies (streamlit, pandas, plotly, numpy)
├── README.md                # Documentation and architecture guide
│
├── data/
│   ├── Global_Cybersecurity_Threats_2015-2024_1000_records.csv  # Primary source
│   └── Cybersecurity_Final_Countrywise.csv                       # Cleaned standardized CSV
│
├── components/
│   ├── __init__.py
│   ├── styles.py            # Modern Dark Cyber design system & CSS injection
│   ├── header.py            # Header, metadata, badges & methodology modal
│   ├── filters.py           # Centralized global filtering controls (F1–F11)
│   ├── kpi_cards.py         # 6 core KPI cards + non-temporal baseline deltas
│   ├── charts.py            # All 11 Plotly visualization modules
│   └── incident_table.py    # Searchable, sortable, paginated explorer & CSV export
│
└── utils/
    ├── __init__.py
    ├── data_loader.py       # Data ingestion, ISO-3 mapping, derived columns & caching
    ├── validation.py        # Schema validation, bounds checking & integrity reporting
    ├── metrics.py           # KPI engine & full baseline comparison calculations
    └── export.py            # CSV preparation and country summary generator
```

---

## 💻 Installation & Local Execution

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- `pip` package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard
```bash
streamlit run app.py
```
Or with explicit port configuration:
```bash
python -m streamlit run app.py --server.port 8501
```

Once running, navigate to:
```
http://localhost:8501
```

---

## 🛡️ Analytical Caveats & Methodology (PRD §3.5)

1. **Coursework Exploration:** This platform is designed for academic analysis and visual exploration. It does not represent live security operations center (SOC) telemetry.
2. **Recorded Affected Users:** Reflects the dataset's recorded impact measure per incident; the sum represents cumulative incident exposure, not unique de-duplicated individuals.
3. **Statistical Uniformity:** Record distributions exhibit near-uniform synthetic benchmark characteristics with minimal cross-country divergence.
4. **Non-Temporal Baseline Comparisons:** KPI deltas compare current filtered selections against the complete 1,000-incident dataset baseline, avoiding misleading temporal growth claims.

---

## 📋 Acceptance Criteria Verification (AC01 – AC18)

- **AC01 (Loads CSV):** Loads `Global_Cybersecurity_Threats_2015-2024_1000_records.csv` on startup.
- **AC02 (Validation):** Automated validation checks schema, types, bounds, missing cells, and duplicates.
- **AC03 (KPI Calculations):** All 6 KPIs calculate with explicit delta against the full 1,000-incident baseline.
- **AC04 (11 Charts):** All 11 charts render correctly with hover, units, and custom styling.
- **AC05 (Unified Filtering):** Every filter updates all KPIs, charts, and tables simultaneously.
- **AC06 & AC07 (Boolean Logic):** AND logic between dimensions, OR logic within multi-selects.
- **AC08 (Reset Action):** "Reset All Filters" immediately restores the full dataset.
- **AC09 (Empty State):** Zero-result filters display a friendly empty state without crashing.
- **AC10 (Small Sample Warning):** Cohorts with `n < 30` display a visible caution banner.
- **AC11 (CSV Export):** Exports all filtered records with timestamped naming.
- **AC12 (Table Features):** Search, column sorting, and pagination (10/25/50/100) verified.
- **AC13 (Filter Consistency):** Shared state guarantees synchronization across all visual modules.
- **AC14 (Non-Temporal Delta):** Delta badges explicitly state "vs full dataset".
- **AC15 (Responsive Layout):** Responsive column grids prevent horizontal viewport overflow.
- **AC16 (Visible Missing Data):** Heatmaps preserve missing combinations as distinct cells.
- **AC17 (Units & Sample Size):** Every chart specifies metric units and sample size (`n = ...`).
- **AC18 (Reproducibility):** Application runs directly with standard `streamlit run app.py`.
