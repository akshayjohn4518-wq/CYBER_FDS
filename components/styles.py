"""
Obsidian Threat Intelligence Design System.
Benchmark: Enterprise intelligence platforms (Palantir, Bloomberg, modern SOC).
Design Language: Quiet intelligence. High signal. Zero visual noise.
"""

THEME_COLORS = {
    "background": "#080A0D",
    "secondary_bg": "#0E1116",
    "surface": "#141922",
    "elevated": "#1A202B",
    "primary_text": "#F2F0EA",
    "secondary_text": "#9299A5",
    "muted_text": "#626A76",
    "border": "#252C36",
    "subtle_border": "#1C222B",
    "accent": "#E8A83E",       # Signal Amber
    "info": "#6D8FB8",         # Steel Blue
    "success": "#55B88A",      # Controlled Green
    "critical": "#D95C5C",     # Critical Red
}

# Qualitative semantic color palette for attack vectors
ATTACK_COLOR_MAP = {
    "Ransomware": "#D95C5C",        # Critical Red
    "DDoS": "#E8A83E",              # Signal Amber
    "Phishing": "#D4883A",          # Warm Amber
    "Malware": "#6D8FB8",           # Steel Blue
    "SQL Injection": "#8E82A6",     # Muted Violet / Slate
    "Man-in-the-Middle": "#55B88A", # Controlled Green
}

# Semantic severity palette
SEVERITY_COLOR_MAP = {
    "High": "#D95C5C",
    "Medium": "#E8A83E",
    "Low": "#55B88A"
}

CUSTOM_CSS = """
<style>
/* Root font and global dark styling: Obsidian Foundation */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #F2F0EA;
    background-color: #080A0D;
}

/* Background overrides - pure graphite, zero neon glow */
.stApp {
    background-color: #080A0D !important;
    background-image: none !important;
    color: #F2F0EA !important;
}

/* Sidebar styling - persistent dark intelligence rail */
[data-testid="stSidebar"] {
    background-color: #0E1116 !important;
    border-right: 1px solid #1C222B !important;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.25rem;
    padding-bottom: 2rem;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    color: #F2F0EA !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* Section Containers - 8px radius, clean graphite surface */
.section-wrapper {
    background: #0E1116;
    border: 1px solid #252C36;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.75rem;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid #1C222B;
    padding-bottom: 0.85rem;
    margin-bottom: 1.25rem;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #F2F0EA;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    letter-spacing: -0.01em;
}

.section-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.18rem 0.5rem;
    border-radius: 4px;
    background: rgba(232, 168, 62, 0.1);
    color: #E8A83E;
    border: 1px solid rgba(232, 168, 62, 0.25);
    letter-spacing: 0.04em;
}

/* Top Global Header */
.obsidian-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.85rem 1.25rem;
    background: #0E1116;
    border: 1px solid #252C36;
    border-radius: 8px;
    margin-bottom: 1.25rem;
    gap: 1rem;
    flex-wrap: wrap;
}

.obsidian-brand-lockup {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.obsidian-mark {
    width: 26px;
    height: 26px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #141922;
    border: 1px solid #E8A83E;
    border-radius: 4px;
    color: #E8A83E;
    font-size: 0.82rem;
    font-weight: 800;
    font-family: 'IBM Plex Mono', monospace;
}

.obsidian-brand-title {
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #F2F0EA;
    margin: 0;
    line-height: 1.1;
}

.obsidian-brand-sub {
    font-size: 0.7rem;
    color: #9299A5;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
}

.obsidian-telemetry-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.76rem;
    color: #9299A5;
}

.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #55B88A;
    background: rgba(85, 184, 138, 0.1);
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    border: 1px solid rgba(85, 184, 138, 0.25);
    font-weight: 600;
}

.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #55B88A;
    display: inline-block;
}

/* Nav anchor rail */
.nav-anchor-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    padding: 0.5rem 0.85rem;
    background: #0E1116;
    border: 1px solid #252C36;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    position: sticky;
    top: 3.5rem;
    z-index: 99;
}

.nav-anchor-link {
    color: #9299A5 !important;
    text-decoration: none !important;
    padding: 0.3rem 0.65rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 600;
    transition: all 0.15s ease;
    border: 1px solid transparent;
}

.nav-anchor-link:hover {
    color: #E8A83E !important;
    background: rgba(232, 168, 62, 0.08);
    border-color: rgba(232, 168, 62, 0.25);
}

/* KPI Card styling: Obsidian Specification */
.kpi-card {
    background: #141922;
    border: 1px solid #252C36;
    border-top: 2px solid #E8A83E;
    border-radius: 8px;
    padding: 1.1rem 1rem 0.95rem 1rem;
    margin-bottom: 0.85rem;
    position: relative;
    transition: border-color 0.15s ease, background-color 0.15s ease;
    min-height: 122px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.kpi-card:hover {
    border-color: #E8A83E;
    background: #171D28;
}

.kpi-card-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.35rem;
}

.kpi-title {
    font-size: 0.72rem;
    font-weight: 600;
    color: #9299A5;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.kpi-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.75rem;
    font-weight: 700;
    color: #F2F0EA;
    letter-spacing: -0.03em;
    margin-bottom: 0.45rem;
    line-height: 1.1;
}

.kpi-delta-wrapper {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.72rem;
    flex-wrap: wrap;
}

.kpi-delta-tag {
    font-family: 'IBM Plex Mono', monospace;
    padding: 0.15rem 0.45rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.7rem;
    line-height: 1;
}

.kpi-delta-neutral {
    background: rgba(232, 168, 62, 0.1);
    color: #E8A83E;
    border: 1px solid rgba(232, 168, 62, 0.25);
}

.kpi-delta-baseline-label {
    color: #626A76;
    font-size: 0.7rem;
    font-family: 'IBM Plex Mono', monospace;
}

/* Badges and Filter Chips */
.filter-chip-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45rem;
    padding: 0.65rem 0.85rem;
    background: #0E1116;
    border: 1px solid #252C36;
    border-radius: 8px;
    margin-bottom: 1.25rem;
}

.filter-chip {
    font-size: 0.73rem;
    font-family: 'IBM Plex Mono', monospace;
    padding: 0.18rem 0.5rem;
    border-radius: 4px;
    background: #141922;
    color: #E8A83E;
    border: 1px solid #252C36;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
}

/* Warnings and Alerts */
.cyber-warning-banner {
    background: #141922;
    border: 1px solid #252C36;
    border-left: 3px solid #E8A83E;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    color: #F2F0EA;
    font-size: 0.85rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.cyber-empty-card {
    background: #0E1116;
    border: 1px solid #252C36;
    border-radius: 8px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 2rem 0;
}

/* Chart container card */
.chart-card {
    background: #141922;
    border: 1px solid #252C36;
    border-radius: 8px;
    padding: 1rem 1rem 0.5rem 1rem;
    margin-bottom: 1.25rem;
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.35rem;
}

.chart-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #F2F0EA;
    letter-spacing: -0.01em;
}

.chart-subtitle {
    font-size: 0.76rem;
    color: #9299A5;
    margin-bottom: 0.65rem;
}

.chart-sample-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #E8A83E;
    background: rgba(232, 168, 62, 0.08);
    padding: 0.15rem 0.45rem;
    border-radius: 4px;
    border: 1px solid rgba(232, 168, 62, 0.2);
}

/* Key Insights Panel */
.insights-panel {
    background: #0E1116;
    border: 1px solid #252C36;
    border-radius: 8px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
}

.insights-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1C222B;
    padding-bottom: 0.65rem;
    margin-bottom: 1rem;
}

.insights-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 0.85rem;
}

.insight-item {
    background: #141922;
    border: 1px solid #1C222B;
    border-left: 3px solid #E8A83E;
    border-radius: 6px;
    padding: 0.85rem 1rem;
}

.insight-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #9299A5;
    margin-bottom: 0.25rem;
}

.insight-text {
    font-size: 0.82rem;
    color: #F2F0EA;
    line-height: 1.4;
}

/* Buttons - 6px radius, neutral dark surface with amber hover */
.stButton > button {
    background: #141922 !important;
    border: 1px solid #252C36 !important;
    color: #F2F0EA !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 0.85rem !important;
    transition: border-color 0.15s ease, color 0.15s ease !important;
}

.stButton > button:hover {
    border-color: #E8A83E !important;
    color: #E8A83E !important;
    background: #1A202B !important;
    box-shadow: none !important;
}

/* Primary download button */
.stDownloadButton > button {
    background: #141922 !important;
    border: 1px solid #E8A83E !important;
    color: #E8A83E !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 0.85rem !important;
    transition: all 0.15s ease !important;
}

.stDownloadButton > button:hover {
    background: rgba(232, 168, 62, 0.15) !important;
    color: #F2F0EA !important;
    border-color: #E8A83E !important;
    box-shadow: none !important;
}

/* Streamlit Expander header */
.streamlit-expanderHeader {
    background-color: #0E1116 !important;
    border-radius: 6px !important;
    border: 1px solid #1C222B !important;
    font-size: 0.82rem !important;
    color: #9299A5 !important;
}

/* Streamlit Inputs & Sliders styling */
[data-baseweb="input"] {
    background-color: #141922 !important;
    border-color: #252C36 !important;
    border-radius: 6px !important;
}

[data-baseweb="select"] {
    border-radius: 6px !important;
}

[data-baseweb="select"] > div {
    background-color: #141922 !important;
    border-color: #252C36 !important;
    border-radius: 6px !important;
    color: #F2F0EA !important;
}

[data-baseweb="tag"] {
    background-color: #1A202B !important;
    border: 1px solid #252C36 !important;
    color: #E8A83E !important;
    border-radius: 4px !important;
}

/* Streamlit Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #252C36 !important;
    border-radius: 8px !important;
    background-color: #141922 !important;
}

/* Streamlit Sliders */
.stSlider [data-baseweb="slider"] {
    margin-top: 0.25rem;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #080A0D;
}
::-webkit-scrollbar-thumb {
    background: #252C36;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3B4555;
}
</style>
"""


def apply_theme():
    """Returns CSS block for Streamlit."""
    return CUSTOM_CSS
