"""
Obsidian KPI Cards Component for Executive Threat & Impact Overview.
Strict adherence to Obsidian Design System:
- Pure dark surface #141922 with subtle amber top accent #E8A83E.
- Large numerical hero values in IBM Plex Mono.
- Explicit non-temporal comparison tags vs full dataset baseline.
- Micro sparkline visualizations computed directly from active dataset.
- Direct DOM rendering via st.html (zero markdown code-block artifacts).
"""
from typing import Optional, List
import pandas as pd
import streamlit as st
from utils.metrics import KPISuite, KPIMetric


def generate_sparkline_svg(values: List[float], color: str = "#E8A83E", width: int = 64, height: int = 20) -> str:
    """Generates a crisp inline SVG polyline sparkline from a numerical series."""
    if not values or len(values) < 2:
        return ""
    min_val, max_val = min(values), max(values)
    val_range = max_val - min_val if max_val != min_val else 1.0

    points = []
    step = width / (len(values) - 1)
    for i, v in enumerate(values):
        x = i * step
        y = (height - 4) - ((v - min_val) / val_range) * (height - 6) + 2
        points.append(f"{x:.1f},{y:.1f}")

    pts_str = " ".join(points)
    last_x, last_y = points[-1].split(",")
    return (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" style="overflow:visible;display:block;">'
        f'<polyline fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" points="{pts_str}"/>'
        f'<circle cx="{last_x}" cy="{last_y}" r="2" fill="{color}"/>'
        f'</svg>'
    )


def render_single_kpi_card(metric: KPIMetric, sparkline_vals: Optional[List[float]] = None):
    """Renders one styled Obsidian HTML KPI card."""
    sparkline_html = generate_sparkline_svg(sparkline_vals) if sparkline_vals else ""

    if metric.delta_display != "N/A":
        # Format delta status with directional arrow or baseline indicator
        prefix = ""
        if metric.delta_value is not None:
            if metric.delta_value > 0 and not metric.delta_display.startswith("+"):
                prefix = "▲ +"
            elif metric.delta_value < 0 and not metric.delta_display.startswith("-"):
                prefix = "▼ "
            elif metric.delta_value == 0:
                prefix = "● "

        delta_tag_html = (
            f'<div class="kpi-delta-wrapper">'
            f'<span class="kpi-delta-tag kpi-delta-neutral">{prefix}{metric.delta_display}</span>'
            f'<span class="kpi-delta-baseline-label">vs baseline ({metric.baseline_display})</span>'
            f'</div>'
        )
    else:
        delta_tag_html = (
            f'<div class="kpi-delta-wrapper">'
            f'<span class="kpi-delta-tag kpi-delta-neutral">N/A</span>'
            f'<span class="kpi-delta-baseline-label">No records in selection</span>'
            f'</div>'
        )

    card_html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-card-header">'
        f'<span class="kpi-title" title="{metric.description}">{metric.label}</span>'
        f'{sparkline_html}'
        f'</div>'
        f'<div class="kpi-value">{metric.current_display}</div>'
        f'{delta_tag_html}'
        f'</div>'
    )

    if hasattr(st, "html"):
        st.html(card_html)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


def extract_yearly_trends(df: Optional[pd.DataFrame]) -> dict:
    """Extracts yearly aggregated values for micro sparkline rendering."""
    trends = {
        "incidents": [],
        "total_loss": [],
        "avg_loss": [],
        "countries": [],
        "users": [],
        "resolution": [],
        "high_sev": [],
    }
    if df is None or df.empty or "Year" not in df.columns:
        return trends

    years = sorted(df["Year"].unique())
    if len(years) < 2:
        return trends

    try:
        yearly_grp = df.groupby("Year")
        trends["incidents"] = [float(yearly_grp.size().get(y, 0)) for y in years]
        trends["total_loss"] = [float(yearly_grp["Financial_Loss_Million_USD"].sum().get(y, 0.0)) for y in years]
        trends["avg_loss"] = [float(yearly_grp["Financial_Loss_Million_USD"].mean().get(y, 0.0)) for y in years]
        trends["countries"] = [float(yearly_grp["Country"].nunique().get(y, 0)) for y in years]
        trends["users"] = [float(yearly_grp["Affected_Users"].sum().get(y, 0)) for y in years]
        trends["resolution"] = [float(yearly_grp["Resolution_Time_Hours"].mean().get(y, 0.0)) for y in years]

        high_sev_series = []
        for y in years:
            sub = df[df["Year"] == y]
            share = (sub["Severity"] == "High").sum() / len(sub) * 100.0 if len(sub) > 0 else 0.0
            high_sev_series.append(float(share))
        trends["high_sev"] = high_sev_series
    except Exception:
        pass

    return trends


def render_kpi_row(suite: KPISuite, df: Optional[pd.DataFrame] = None):
    """Renders the top 7 KPI cards grid in Section 01."""
    trends = extract_yearly_trends(df)

    # Top row: 4 primary scale metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_single_kpi_card(suite.total_incidents, trends.get("incidents"))
    with col2:
        render_single_kpi_card(suite.total_loss, trends.get("total_loss"))
    with col3:
        render_single_kpi_card(suite.avg_loss, trends.get("avg_loss"))
    with col4:
        render_single_kpi_card(suite.countries_represented, trends.get("countries"))

    # Bottom row: 3 operational & severity metrics
    col5, col6, col7 = st.columns(3)
    with col5:
        render_single_kpi_card(suite.total_affected_users, trends.get("users"))
    with col6:
        render_single_kpi_card(suite.avg_resolution_time, trends.get("resolution"))
    with col7:
        render_single_kpi_card(suite.high_severity_share, trends.get("high_sev"))
