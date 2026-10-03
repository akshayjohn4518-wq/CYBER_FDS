"""
Centralized Global Filtering System (F1 - F11).
Implements PRD Section 6:
- Single shared filter engine powering all KPIs, charts, tables, and exports.
- Multi-select OR logic within dimension; AND logic across dimensions.
- Reset restores the full baseline dataset.
- Exposes active filter chips and badges.
"""
from dataclasses import dataclass
from typing import List, Tuple
import pandas as pd
import streamlit as st


@dataclass
class FilterState:
    countries: List[str]
    year_range: Tuple[int, int]
    attack_types: List[str]
    target_industries: List[str]
    attack_sources: List[str]
    vulnerabilities: List[str]
    defense_mechanisms: List[str]
    severities: List[str]
    loss_range: Tuple[float, float]
    resolution_range: Tuple[int, int]
    users_range: Tuple[int, int]


def init_session_state(df: pd.DataFrame):
    """Initializes filter values in st.session_state if not already present."""
    if "filter_reset_trigger" not in st.session_state:
        st.session_state.filter_reset_trigger = 0

    defaults = {
        "f_countries": [],
        "f_year_range": (int(df["Year"].min()), int(df["Year"].max())),
        "f_attack_types": [],
        "f_industries": [],
        "f_attack_sources": [],
        "f_vulnerabilities": [],
        "f_defense": [],
        "f_severities": [],
        "f_loss_range": (float(df["Financial_Loss_Million_USD"].min()), float(df["Financial_Loss_Million_USD"].max())),
        "f_res_range": (int(df["Resolution_Time_Hours"].min()), int(df["Resolution_Time_Hours"].max())),
        "f_users_range": (int(df["Affected_Users"].min()), int(df["Affected_Users"].max())),
    }

    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_filters(df: pd.DataFrame):
    """Resets all filters back to default full-range states."""
    st.session_state.f_countries = []
    st.session_state.f_year_range = (int(df["Year"].min()), int(df["Year"].max()))
    st.session_state.f_attack_types = []
    st.session_state.f_industries = []
    st.session_state.f_attack_sources = []
    st.session_state.f_vulnerabilities = []
    st.session_state.f_defense = []
    st.session_state.f_severities = []
    st.session_state.f_loss_range = (float(df["Financial_Loss_Million_USD"].min()), float(df["Financial_Loss_Million_USD"].max()))
    st.session_state.f_res_range = (int(df["Resolution_Time_Hours"].min()), int(df["Resolution_Time_Hours"].max()))
    st.session_state.f_users_range = (int(df["Affected_Users"].min()), int(df["Affected_Users"].max()))
    st.session_state.filter_reset_trigger += 1


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[pd.DataFrame, FilterState]:
    """
    Renders the persistent left sidebar with all 11 global filters.
    Applies unified filtering logic and returns (filtered_df, filter_state).
    """
    init_session_state(df)

    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
            <div style="font-size: 1.05rem; font-weight: 800; color: #F3F4F6; letter-spacing: -0.02em;">
                GLOBAL FILTERS
            </div>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #38BDF8; background: rgba(56, 189, 248, 0.1); padding: 0.15rem 0.4rem; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.25);">
                F1 – F11
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True, help="Restores full 1,000 incident dataset"):
        reset_filters(df)
        st.rerun()

    st.sidebar.markdown("<hr style='border: none; border-top: 1px solid #1E293B; margin: 0.75rem 0;'>", unsafe_allow_html=True)

    # 1. Geographic & Temporal
    with st.sidebar.expander("🌍 Geography & Time (F1, F2)", expanded=True):
        all_countries = sorted(df["Country"].unique().tolist())
        countries = st.multiselect(
            "F1. Country",
            options=all_countries,
            key="f_countries",
            placeholder="All 10 Countries"
        )

        min_year = int(df["Year"].min())
        max_year = int(df["Year"].max())
        year_range = st.slider(
            "F2. Year Range",
            min_value=min_year,
            max_value=max_year,
            key="f_year_range"
        )

    # 2. Threat Vector & Target
    with st.sidebar.expander("🛡️ Attack & Industry (F3, F4, F5)", expanded=True):
        all_attacks = sorted(df["Attack_Type"].unique().tolist())
        attack_types = st.multiselect(
            "F3. Attack Type",
            options=all_attacks,
            key="f_attack_types",
            placeholder="All 6 Attack Types"
        )

        all_industries = sorted(df["Target_Industry"].unique().tolist())
        industries = st.multiselect(
            "F4. Target Industry",
            options=all_industries,
            key="f_industries",
            placeholder="All 7 Industries"
        )

        all_sources = sorted(df["Attack_Source"].unique().tolist())
        attack_sources = st.multiselect(
            "F5. Attack Source",
            options=all_sources,
            key="f_attack_sources",
            placeholder="All Attack Sources"
        )

    # 3. Vulnerability & Defense
    with st.sidebar.expander("🔐 Security & Defense (F6, F7, F8)", expanded=False):
        all_vulns = sorted(df["Vulnerability_Type"].unique().tolist())
        vulnerabilities = st.multiselect(
            "F6. Security Vulnerability",
            options=all_vulns,
            key="f_vulnerabilities",
            placeholder="All Vulnerabilities"
        )

        all_defenses = sorted(df["Defense_Mechanism"].unique().tolist())
        defenses = st.multiselect(
            "F7. Defense Mechanism",
            options=all_defenses,
            key="f_defense",
            placeholder="All Defense Mechanisms"
        )

        severities = st.multiselect(
            "F8. Severity Rating",
            options=["Low", "Medium", "High"],
            key="f_severities",
            placeholder="All Severities"
        )

    # 4. Impact & Duration
    with st.sidebar.expander("💰 Quantitative Impact (F9, F10, F11)", expanded=False):
        min_loss = float(df["Financial_Loss_Million_USD"].min())
        max_loss = float(df["Financial_Loss_Million_USD"].max())
        loss_range = st.slider(
            "F9. Financial Loss ($M)",
            min_value=min_loss,
            max_value=max_loss,
            step=1.0,
            format="$%.0fM",
            key="f_loss_range"
        )

        min_res = int(df["Resolution_Time_Hours"].min())
        max_res = int(df["Resolution_Time_Hours"].max())
        resolution_range = st.slider(
            "F10. Resolution Time (Hours)",
            min_value=min_res,
            max_value=max_res,
            step=1,
            key="f_res_range"
        )

        min_users = int(df["Affected_Users"].min())
        max_users = int(df["Affected_Users"].max())
        users_range = st.slider(
            "F11. Affected Users",
            min_value=min_users,
            max_value=max_users,
            step=10000,
            key="f_users_range"
        )

    filter_state = FilterState(
        countries=countries,
        year_range=year_range,
        attack_types=attack_types,
        target_industries=industries,
        attack_sources=attack_sources,
        vulnerabilities=vulnerabilities,
        defense_mechanisms=defenses,
        severities=severities,
        loss_range=loss_range,
        resolution_range=resolution_range,
        users_range=users_range
    )

    # Apply unified filtering logic (AND between filters, OR inside multi-select)
    filtered = df.copy()

    if countries:
        filtered = filtered[filtered["Country"].isin(countries)]
    if year_range:
        filtered = filtered[(filtered["Year"] >= year_range[0]) & (filtered["Year"] <= year_range[1])]
    if attack_types:
        filtered = filtered[filtered["Attack_Type"].isin(attack_types)]
    if industries:
        filtered = filtered[filtered["Target_Industry"].isin(industries)]
    if attack_sources:
        filtered = filtered[filtered["Attack_Source"].isin(attack_sources)]
    if vulnerabilities:
        filtered = filtered[filtered["Vulnerability_Type"].isin(vulnerabilities)]
    if defenses:
        filtered = filtered[filtered["Defense_Mechanism"].isin(defenses)]
    if severities:
        filtered = filtered[filtered["Severity"].isin(severities)]
    if loss_range:
        filtered = filtered[
            (filtered["Financial_Loss_Million_USD"] >= loss_range[0]) &
            (filtered["Financial_Loss_Million_USD"] <= loss_range[1])
        ]
    if resolution_range:
        filtered = filtered[
            (filtered["Resolution_Time_Hours"] >= resolution_range[0]) &
            (filtered["Resolution_Time_Hours"] <= resolution_range[1])
        ]
    if users_range:
        filtered = filtered[
            (filtered["Affected_Users"] >= users_range[0]) &
            (filtered["Affected_Users"] <= users_range[1])
        ]

    # Quick summary in sidebar
    st.sidebar.markdown(
        f"""
        <div style="background: #111827; border: 1px solid #1E293B; border-radius: 8px; padding: 0.6rem 0.8rem; margin-top: 1rem;">
            <div style="font-size: 0.72rem; color: #9CA3AF; text-transform: uppercase;">Active Result Set</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 700; color: #38BDF8;">
                {len(filtered):,} <span style="font-size: 0.75rem; color: #6B7280;">/ {len(df):,} ({len(filtered)/len(df)*100:.1f}%)</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return filtered, filter_state


def render_active_filter_chips(filter_state: FilterState, total_matched: int, total_full: int):
    """Renders visual chips for every active non-default filter."""
    active_chips = []

    if filter_state.countries:
        active_chips.append(f"Country: {', '.join(filter_state.countries[:2])}{'...' if len(filter_state.countries) > 2 else ''}")
    if filter_state.year_range != (2015, 2024):
        active_chips.append(f"Years: {filter_state.year_range[0]}–{filter_state.year_range[1]}")
    if filter_state.attack_types:
        active_chips.append(f"Attack: {', '.join(filter_state.attack_types[:2])}{'...' if len(filter_state.attack_types) > 2 else ''}")
    if filter_state.target_industries:
        active_chips.append(f"Industry: {', '.join(filter_state.target_industries[:2])}{'...' if len(filter_state.target_industries) > 2 else ''}")
    if filter_state.attack_sources:
        active_chips.append(f"Source: {', '.join(filter_state.attack_sources)}")
    if filter_state.vulnerabilities:
        active_chips.append(f"Vuln: {', '.join(filter_state.vulnerabilities[:2])}{'...' if len(filter_state.vulnerabilities) > 2 else ''}")
    if filter_state.defense_mechanisms:
        active_chips.append(f"Defense: {', '.join(filter_state.defense_mechanisms[:2])}{'...' if len(filter_state.defense_mechanisms) > 2 else ''}")
    if filter_state.severities:
        active_chips.append(f"Severity: {', '.join(filter_state.severities)}")

    chip_html = "".join([f'<span class="filter-chip">🏷️ {chip}</span>' for chip in active_chips])
    status_text = f"Showing <b>{total_matched:,}</b> of <b>{total_full:,}</b> incidents ({total_matched/total_full*100:.1f}%)"

    st.markdown(
        f"""
        <div class="filter-chip-bar">
            <span style="font-size: 0.8rem; font-weight: 600; color: #CBD5E1; margin-right: 0.5rem;">{status_text}</span>
            {chip_html if chip_html else '<span style="font-size: 0.75rem; color: #64748B;">No filters active (Full 1000 incident dataset)</span>'}
        </div>
        """,
        unsafe_allow_html=True
    )
