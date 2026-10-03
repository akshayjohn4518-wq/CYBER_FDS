"""
Modern Dark Cybersecurity Intelligence Theme and CSS styling injection.
Complies with PRD Section 10 Design Tokens and Aesthetics.
"""

THEME_COLORS = {
    "background": "#080B12",
    "surface": "#111827",
    "elevated": "#182235",
    "primary_text": "#F3F4F6",
    "secondary_text": "#9CA3AF",
    "border": "#263244",
    "accent": "#38BDF8",
    "positive": "#34D399",
    "warning": "#FBBF24",
    "critical": "#F87171",
}

# Qualitative color palette for attack types (high contrast, color-blind accessible)
ATTACK_COLOR_MAP = {
    "Ransomware": "#F87171",        # Red / Rose
    "DDoS": "#FB923C",              # Orange
    "Phishing": "#FBBF24",          # Amber
    "Malware": "#38BDF8",           # Sky Cyan
    "SQL Injection": "#A78BFA",     # Purple / Violet
    "Man-in-the-Middle": "#34D399", # Emerald Mint
}

SEVERITY_COLOR_MAP = {
    "High": "#F87171",
    "Medium": "#FBBF24",
    "Low": "#34D399"
}

CUSTOM_CSS = """
<style>
/* Root font and global dark styling */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #F3F4F6;
}

/* Background overrides */
.stApp {
    background-color: #080B12 !important;
    background-image: 
        radial-gradient(at 15% 15%, rgba(56, 189, 248, 0.05) 0px, transparent 50%),
        radial-gradient(at 85% 85%, rgba(167, 139, 250, 0.04) 0px, transparent 50%);
    background-attachment: fixed;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0C121E !important;
    border-right: 1px solid #1F2A3C !important;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #F9FAFB !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* Nav anchor bar */
.nav-anchor-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    background: #111827;
    border: 1px solid #263244;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    position: sticky;
    top: 3.5rem;
    z-index: 99;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.nav-anchor-link {
    color: #9CA3AF !important;
    text-decoration: none !important;
    padding: 0.35rem 0.75rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

.nav-anchor-link:hover {
    color: #38BDF8 !important;
    background: rgba(56, 189, 248, 0.1);
    border-color: rgba(56, 189, 248, 0.25);
}

/* Section Containers */
.section-wrapper {
    background: #0E1626;
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1E293B;
    padding-bottom: 0.85rem;
    margin-bottom: 1.25rem;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #F3F4F6;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    background: rgba(56, 189, 248, 0.15);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.3);
}

/* KPI Card styling */
.kpi-card {
    background: linear-gradient(135deg, #111827 0%, #151F33 100%);
    border: 1px solid #223046;
    border-radius: 14px;
    padding: 1.2rem 1.1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    transition: transform 0.2s ease, border-color 0.2s ease;
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: #38BDF8;
    box-shadow: 0 8px 25px rgba(56, 189, 248, 0.12);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #38BDF8, #818CF8);
}

.kpi-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.4rem;
}

.kpi-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.85rem;
    font-weight: 800;
    color: #F9FAFB;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
    line-height: 1.1;
}

.kpi-delta-wrapper {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.75rem;
}

.kpi-delta-tag {
    font-family: 'JetBrains Mono', monospace;
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    font-weight: 600;
}

.kpi-delta-neutral {
    background: rgba(156, 163, 175, 0.15);
    color: #9CA3AF;
    border: 1px solid rgba(156, 163, 175, 0.25);
}

.kpi-delta-baseline-label {
    color: #6B7280;
    font-size: 0.72rem;
}

/* Badges and Filter Chips */
.filter-chip-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45rem;
    padding: 0.65rem 0.85rem;
    background: #0E1626;
    border: 1px solid #1E293B;
    border-radius: 10px;
    margin-bottom: 1.25rem;
}

.filter-chip {
    font-size: 0.75rem;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    background: #182235;
    color: #38BDF8;
    border: 1px solid #263244;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}

/* Warnings and Alerts */
.cyber-warning-banner {
    background: rgba(251, 191, 36, 0.08);
    border: 1px solid rgba(251, 191, 36, 0.3);
    border-left: 4px solid #FBBF24;
    padding: 0.85rem 1.1rem;
    border-radius: 8px;
    color: #FDE68A;
    font-size: 0.88rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.cyber-empty-card {
    background: #111827;
    border: 1px dashed #374151;
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 2rem 0;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(180deg, #1E293B 0%, #111827 100%) !important;
    border: 1px solid #334155 !important;
    color: #F3F4F6 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    border-color: #38BDF8 !important;
    color: #38BDF8 !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.25) !important;
}

/* Primary download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
    border: 1px solid #38BDF8 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #0369A1 0%, #075985 100%) !important;
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.4) !important;
}

/* Tooltip & expander styling */
.streamlit-expanderHeader {
    background-color: #111827 !important;
    border-radius: 8px !important;
    border: 1px solid #1F2A3C !important;
    font-size: 0.85rem !important;
    color: #9CA3AF !important;
}

/* Chart container card */
.chart-card {
    background: #111827;
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 1rem 1rem 0.5rem 1rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.4rem;
}

.chart-title {
    font-size: 1rem;
    font-weight: 700;
    color: #F3F4F6;
}

.chart-subtitle {
    font-size: 0.78rem;
    color: #9CA3AF;
    margin-bottom: 0.75rem;
}

.chart-sample-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #38BDF8;
    background: rgba(56, 189, 248, 0.1);
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    border: 1px solid rgba(56, 189, 248, 0.2);
}
</style>
"""


def apply_theme():
    """Returns CSS block for Streamlit."""
    return CUSTOM_CSS
