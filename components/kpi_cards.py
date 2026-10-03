"""
KPI Cards Component for Executive Overview.
Displays the 6 core metrics + countries represented with explicit non-temporal
comparisons against the full unfiltered dataset baseline (PRD Section 7).
"""
import streamlit as st
from utils.metrics import KPISuite, KPIMetric


def render_single_kpi_card(metric: KPIMetric):
    """Renders one styled HTML KPI card."""
    delta_tag_html = ""
    if metric.delta_display != "N/A":
        delta_tag_html = f"""
        <div class="kpi-delta-wrapper">
            <span class="kpi-delta-tag kpi-delta-neutral">{metric.delta_display}</span>
            <span class="kpi-delta-baseline-label">vs full dataset ({metric.baseline_display})</span>
        </div>
        """
    else:
        delta_tag_html = """
        <div class="kpi-delta-wrapper">
            <span class="kpi-delta-tag kpi-delta-neutral">N/A</span>
            <span class="kpi-delta-baseline-label">No records in selection</span>
        </div>
        """

    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-title" title="{metric.description}">{metric.label}</div>
        <div class="kpi-value">{metric.current_display}</div>
        {delta_tag_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_kpi_row(suite: KPISuite):
    """Renders the top KPI cards grid in Section 01."""
    # Top row: 3 primary scale metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_single_kpi_card(suite.total_incidents)
    with col2:
        render_single_kpi_card(suite.total_loss)
    with col3:
        render_single_kpi_card(suite.avg_loss)
    with col4:
        render_single_kpi_card(suite.countries_represented)

    # Bottom row: 3 operational & severity metrics
    col5, col6, col7 = st.columns(3)
    with col5:
        render_single_kpi_card(suite.total_affected_users)
    with col6:
        render_single_kpi_card(suite.avg_resolution_time)
    with col7:
        render_single_kpi_card(suite.high_severity_share)
