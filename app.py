"""
Global Cybersecurity Threats Analytics Dashboard (2015–2024)
Obsidian Threat Intelligence Platform.
Design System: Obsidian — Threat Intelligence (Enterprise Benchmark)
"""
from datetime import datetime
import streamlit as st

# Configure page metadata must be the very first Streamlit command
st.set_page_config(
    page_title="Obsidian // Cyber Threat Intelligence",
    page_icon="⬡",
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

# Inject Obsidian Threat Intelligence CSS stylesheet
st.markdown(apply_theme(), unsafe_allow_html=True)


def render_key_insights(filtered_df, full_df):
    """Dynamically generates analytical intelligence observations from active dataset."""
    if filtered_df.empty:
        return

    n = len(filtered_df)
    top_attack = filtered_df["Attack_Type"].value_counts().index[0]
    top_attack_pct = (filtered_df["Attack_Type"] == top_attack).sum() / n * 100
    top_attack_loss = filtered_df[filtered_df["Attack_Type"] == top_attack]["Financial_Loss_Million_USD"].sum()

    top_country_series = filtered_df.groupby("Country")["Financial_Loss_Million_USD"].sum()
    top_country = top_country_series.idxmax()
    top_country_loss = top_country_series.max()
    country_share = top_country_loss / filtered_df["Financial_Loss_Million_USD"].sum() * 100 if filtered_df["Financial_Loss_Million_USD"].sum() > 0 else 0

    top_vuln = filtered_df["Vulnerability_Type"].value_counts().index[0]
    top_defense = filtered_df["Defense_Mechanism"].value_counts().index[0]

    avg_res = filtered_df["Resolution_Time_Hours"].mean()
    base_res = full_df["Resolution_Time_Hours"].mean()
    res_diff = avg_res - base_res

    st.markdown(
        f"""
        <div class="insights-panel">
            <div class="insights-header">
                <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #E8A83E; letter-spacing: 0.08em; text-transform: uppercase;">
                    KEY INTELLIGENCE FINDINGS // ACTIVE COHORT (n = {n:,})
                </span>
                <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #626A76;">
                    COMPUTED FROM ACTIVE FILTERS
                </span>
            </div>
            <div class="insights-grid">
                <div class="insight-item">
                    <div class="insight-label">Primary Threat Vector</div>
                    <div class="insight-text">
                        <b>{top_attack}</b> represents the leading attack modality, driving <b>{top_attack_pct:.1f}%</b> of cohort incidents and <b>${top_attack_loss:,.1f}M</b> in cumulative exposure.
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-label">Exposure Concentration</div>
                    <div class="insight-text">
                        Sovereign financial loss peaks in <b>{top_country}</b> with <b>${top_country_loss:,.1f}M</b>, representing <b>{country_share:.1f}%</b> of total cohort financial damage.
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-label">Exploitation & Defense</div>
                    <div class="insight-text">
                        Primary initial access vector is <b>{top_vuln}</b>. The predominant countermeasure architecture deployed is <b>{top_defense}</b>.
                    </div>
                </div>
                <div class="insight-item">
                    <div class="insight-label">Mean Operational Latency</div>
                    <div class="insight-text">
                        Cohort recovery duration averages <b>{avg_res:.1f} hours</b> ({'+' if res_diff >= 0 else ''}{res_diff:.1f} hrs vs full dataset 37.2 hrs baseline).
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    # 1. Ingest, clean and validate dataset
    full_df, validation_report = load_dataset()

    if not validation_report.is_valid or full_df.empty:
        st.error("🚨 Critical Error Loading Dataset:")
        for err in validation_report.errors:
            st.error(f"- {err}")
        st.stop()

    # 2. Render Global Sidebar Navigation & Analytical Filters (F1 - F11)
    filtered_df, filter_state = render_sidebar_filters(full_df)

    # 3. Calculate KPIs and baseline differences (vs full dataset)
    kpi_suite = calculate_kpis(filtered_df, full_df)

    # 4. Render Obsidian Enterprise Header & Global Telemetry
    render_header(validation_report, total_records=len(full_df))

    # 5. Render Active Filter Telemetry Chips
    render_active_filter_chips(filter_state, total_matched=len(filtered_df), total_full=len(full_df))

    # 6. Small Sample Warning (< 30 records)
    if kpi_suite.is_small_sample:
        st.markdown(
            f"""
            <div class="cyber-warning-banner">
                <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.74rem; font-weight: 700; color: #E8A83E;">WARNING //</span>
                <span style="font-size: 0.82rem;">
                    Limited cohort sample (n = {len(filtered_df):,}). Interpret statistical distributions and parametric averages with caution.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 7. Empty State Handling (0 matching records)
    if kpi_suite.is_empty:
        st.markdown(
            """
            <div class="cyber-empty-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem; color: #626A76;">⬡</div>
                <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; color: #F2F0EA;">
                    Zero incidents match active filter criteria.
                </h3>
                <p style="color: #9299A5; max-width: 500px; margin: 0 auto 1.5rem auto; font-size: 0.85rem;">
                    Your filter combinations returned zero matching threat events. Reset filters to restore the full 1,000 incident dataset.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col_c1, col_c2, col_c3 = st.columns([2, 1, 2])
        with col_c2:
            if st.button("↺ Reset All Filters Now", width="stretch"):
                reset_filters(full_df)
                st.rerun()
        st.stop()

    current_timestamp = datetime.now().strftime("%d %b %Y · %H:%M") + " IST"

    # =========================================================================
    # SECTION 01 — EXECUTIVE THREAT & IMPACT OVERVIEW
    # =========================================================================
    st.markdown("<div id='section-01-executive-overview'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">01</span>
                    EXECUTIVE THREAT & IMPACT OVERVIEW
                </div>
                <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #9299A5;">
                    LAST UPDATED: <b style="color: #F2F0EA;">{current_timestamp}</b>
                </div>
            </div>
            <div style="font-size: 0.8rem; color: #9299A5; margin-bottom: 1.15rem;">
                Global cyber threat landscape at a glance
            </div>
        """,
        unsafe_allow_html=True
    )

    # Render 7 Obsidian KPI cards with micro sparklines
    render_kpi_row(kpi_suite, filtered_df)

    # Render Dynamically Computed Key Insights
    render_key_insights(filtered_df, full_df)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # 2-Column Grid: Country Financial Impact + Yearly Dual Axis Trend
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        render_chart_01(filtered_df)

    with row1_c2:
        render_chart_02(filtered_df)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 02 — GLOBAL THREAT LANDSCAPE & GEOGRAPHY
    # =========================================================================
    st.markdown("<div id='section-02-global-threat-landscape'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">02</span>
                    GLOBAL THREAT LANDSCAPE & GEOGRAPHY
                </div>
                <span style="font-size: 0.72rem; color: #9299A5; font-family: 'IBM Plex Mono', monospace;">SOVEREIGN EXPOSURE</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    # Full-width Choropleth Map
    render_chart_11(filtered_df)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Attack Distribution
    render_chart_04(filtered_df)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 03 — THREAT VECTOR & ACTOR INTELLIGENCE
    # =========================================================================
    st.markdown("<div id='section-03-attack-intelligence'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">03</span>
                    THREAT VECTOR & ACTOR INTELLIGENCE
                </div>
                <span style="font-size: 0.72rem; color: #9299A5; font-family: 'IBM Plex Mono', monospace;">CROSS-TABULATION & ATTRIBUTION</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    row3_c1, row3_c2 = st.columns(2)
    with row3_c1:
        render_chart_07(filtered_df)

    with row3_c2:
        render_chart_08(filtered_df)

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Scatter Plot: Affected Users vs Financial Loss
    render_chart_05(filtered_df)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 04 — FINANCIAL & OPERATIONAL IMPACT DISTRIBUTIONS
    # =========================================================================
    st.markdown("<div id='section-04-financial-operational-impact'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">04</span>
                    FINANCIAL & OPERATIONAL IMPACT DISTRIBUTIONS
                </div>
                <span style="font-size: 0.72rem; color: #9299A5; font-family: 'IBM Plex Mono', monospace;">SPREADS & SECTOR EXPOSURE</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    row4_c1, row4_c2 = st.columns(2)
    with row4_c1:
        render_chart_03(filtered_df)

    with row4_c2:
        render_chart_06(filtered_df)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 05 — DEFENSE ARCHITECTURE & INCIDENT TRAJECTORY
    # =========================================================================
    st.markdown("<div id='section-05-defense-response-dynamics'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">05</span>
                    DEFENSE ARCHITECTURE & INCIDENT TRAJECTORY
                </div>
                <span style="font-size: 0.72rem; color: #9299A5; font-family: 'IBM Plex Mono', monospace;">COUNTERMEASURES & LONGITUDINAL DYNAMICS</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    row5_c1, row5_c2 = st.columns(2)
    with row5_c1:
        render_chart_09(filtered_df)

    with row5_c2:
        render_chart_10(filtered_df)

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================================================================
    # SECTION 06 — INCIDENT EXPLORER & TELEMETRY AUDIT
    # =========================================================================
    st.markdown("<div id='section-06-incident-explorer'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-wrapper">
            <div class="section-header">
                <div class="section-title">
                    <span class="section-num">06</span>
                    INCIDENT EXPLORER & TELEMETRY AUDIT
                </div>
                <span style="font-size: 0.72rem; color: #9299A5; font-family: 'IBM Plex Mono', monospace;">GRANULAR RECORD AUDITING</span>
            </div>
        """,
        unsafe_allow_html=True
    )

    render_incident_explorer(filtered_df)

    st.markdown("</div>", unsafe_allow_html=True)

    # Application Footer
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 1rem 0; color: #626A76; font-size: 0.76rem; border-top: 1px solid #1C222B; font-family: 'IBM Plex Mono', monospace;">
            <b>OBSIDIAN // THREAT INTELLIGENCE WORKSPACE</b> &bull; Fundamentals of Data Science<br>
            Production Analytics Engine &bull; Streamlit / Plotly / Pandas
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
