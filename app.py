"""
Global Cybersecurity Threats Analytics Dashboard (2015–2024)
Course: Fundamentals of Data Science
Owner: REDDY — CSE-QE-2A
Version: 1.1 — Vibe Coding Ready
"""
import streamlit as st

# Configure page metadata must be the very first Streamlit command
st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard | 2015-2024",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components.styles import apply_theme
from components.header import render_header
from components.filters import render_sidebar_filters, render_active_filter_chips, reset_filters
from components.kpi_cards import render_kpi_row
from components.charts import (
    render_chart_01, render_chart_02, render_chart_03, render_chart_04,
    render_chart_05, render_chart_06, render_chart_07, render_chart_08,
    render_chart_09, render_chart_10, render_chart_11
)
from components.incident_table import render_incident_explorer
from utils.data_loader import load_dataset
from utils.metrics import calculate_kpis

# Inject custom cyber dark CSS design system
st.markdown(apply_theme(), unsafe_allow_html=True)


def main():
    # 1. Ingest, clean and validate dataset
    full_df, validation_report = load_dataset()

    if not validation_report.is_valid or full_df.empty:
        st.error("🚨 Critical Error Loading Dataset:")
        for err in validation_report.errors:
            st.error(f"- {err}")
        st.stop()

    # 2. Render Global Sidebar Filters (F1 - F11)
    filtered_df, filter_state = render_sidebar_filters(full_df)

    # 3. Calculate KPIs and baseline differences (vs full dataset)
    kpi_suite = calculate_kpis(filtered_df, full_df)

    # 4. Render Application Header, Metadata & Caveats
    render_header(validation_report, total_records=len(full_df))

    # 5. Render Active Filter Chips & Status Bar
    render_active_filter_chips(filter_state, total_matched=len(filtered_df), total_full=len(full_df))

    # 6. Small Sample Warning (< 30 records)
    if kpi_suite.is_small_sample:
        st.markdown(
            f"""
            <div class="cyber-warning-banner">
                <span style="font-size: 1.2rem;">⚠️</span>
                <div>
                    <b>Limited sample size (n = {len(filtered_df):,}):</b>
                    Interpret aggregate statistics and distributions with caution when viewing small cohorts.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 7. Empty State Handling (0 matching records)
    if kpi_suite.is_empty:
        st.markdown(
            """
            <div class="cyber-empty-card">
                <div style="font-size: 3rem; margin-bottom: 0.75rem;">🛡️</div>
                <h2 style="margin: 0 0 0.5rem 0; font-size: 1.6rem; color: #F3F4F6;">
                    No incidents match your current filters.
                </h2>
                <p style="color: #9CA3AF; max-width: 500px; margin: 0 auto 1.5rem auto; font-size: 0.92rem;">
                    Your filter combinations returned zero matching threat events. Reset your filters to restore the full 1,000 incident dataset.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col_c1, col_c2, col_c3 = st.columns([2, 1, 2])
        with col_c2:
            if st.button("🔄 Reset All Filters Now", use_container_width=True):
                reset_filters(full_df)
                st.rerun()
        st.stop()

    # =========================================================================
    # SECTION 01 — EXECUTIVE OVERVIEW
    # =========================================================================
    st.markdown("<div id='section-01-executive-overview'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">SECTION 01</span>
                    Executive Threat & Impact Overview
                </div>
                <span style="font-size: 0.8rem; color: #9CA3AF;">Core Performance Indicators</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    # Render 6 KPI cards + countries represented
    render_kpi_row(kpi_suite)

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

    # 2-Column Grid: Country Financial Impact + Yearly Dual Axis Trend
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_01(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    with row1_c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_02(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 02 — GLOBAL THREAT LANDSCAPE
    # =========================================================================
    st.markdown("<div id='section-02-global-threat-landscape'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">SECTION 02</span>
                    Global Threat Landscape & Geography
                </div>
                <span style="font-size: 0.8rem; color: #9CA3AF;">Sovereign Exposure & Attack Distribution</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    # Full-width Choropleth Map
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    render_chart_11(filtered_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Attack Distribution
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    render_chart_04(filtered_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 03 — ATTACK INTELLIGENCE
    # =========================================================================
    st.markdown("<div id='section-03-attack-intelligence'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">SECTION 03</span>
                    Threat Vector & Actor Intelligence
                </div>
                <span style="font-size: 0.8rem; color: #9CA3AF;">Cross-Tabulation & Threat Attribution</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_07(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    with row3_c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_08(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Scatter Plot: Affected Users vs Financial Loss
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    render_chart_05(filtered_df)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 04 — FINANCIAL & OPERATIONAL IMPACT
    # =========================================================================
    st.markdown("<div id='section-04-financial-operational-impact'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">SECTION 04</span>
                    Financial & Operational Impact Distributions
                </div>
                <span style="font-size: 0.8rem; color: #9CA3AF;">Parametric Spreads & Industry Vulnerability</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    row4_c1, row4_c2 = st.columns(2)
    with row4_c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_03(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    with row4_c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_06(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 05 — DEFENSE & RESPONSE DYNAMICS
    # =========================================================================
    st.markdown("<div id='section-05-defense-response-dynamics'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">SECTION 05</span>
                    Defense Architecture & Incident Trajectory
                </div>
                <span style="font-size: 0.8rem; color: #9CA3AF;">Security Countermeasures & Attack Evolution</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    row5_c1, row5_c2 = st.columns(2)
    with row5_c1:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_09(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    with row5_c2:
        st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
        render_chart_10(filtered_df)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 06 — INCIDENT EXPLORER & DATA EXPORT
    # =========================================================================
    st.markdown("<div id='section-06-incident-explorer'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">SECTION 06</span>
                    Incident Explorer & Telemetry Export
                </div>
                <span style="font-size: 0.8rem; color: #9CA3AF;">Granular Record Auditing</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    render_incident_explorer(filtered_df)

    st.markdown("</div>", unsafe_allow_html=True)

    # Application Footer
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 1rem 0; color: #64748B; font-size: 0.8rem; border-top: 1px solid #1E293B;">
            <b>Global Cybersecurity Threats Analytics Dashboard</b> &bull; Fundamentals of Data Science Coursework<br>
            Developed by REDDY (CSE-QE-2A) &bull; Built with Streamlit, Plotly & Pandas &bull; October 2026
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
