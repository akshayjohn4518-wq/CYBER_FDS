"""
Obsidian Centralized Global Filtering System (F1 - F11).
Implements Obsidian Threat Intelligence specification:
- Sidebar header: OBSIDIAN THREAT INTELLIGENCE with geometric security mark.
- Navigation rail with subtle amber indicators.
- All 11 global analytical filters preserved with unified cross-filtering logic.
- Compact filter chips with monospaced telemetry counts.
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
    Renders the Obsidian navigation sidebar and analytical filter engine.
    Applies unified filtering logic and returns (filtered_df, filter_state).
    """
    init_session_state(df)

    # 1. Sidebar Brand Header
    st.sidebar.markdown(
        """
        <div style="padding-bottom: 0.85rem; border-bottom: 1px solid #1C222B; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.2rem;">
                <span style="display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; background: #141922; border: 1px solid #E8A83E; border-radius: 4px; color: #E8A83E; font-size: 0.75rem; font-weight: 800;">⬡</span>
                <span style="font-family: 'Inter', sans-serif; font-size: 0.92rem; font-weight: 800; letter-spacing: 0.08em; color: #F2F0EA; text-transform: uppercase;">
                    OBSIDIAN
                </span>
            </div>
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #9299A5; letter-spacing: 0.06em; text-transform: uppercase;">
                THREAT INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Workspace Navigation Rail
    st.sidebar.markdown(
        """
        <div style="margin-bottom: 1.15rem;">
            <div style="font-size: 0.68rem; font-weight: 700; color: #626A76; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; font-family: 'IBM Plex Mono', monospace;">
                GLOBAL VIEW
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.2rem; font-size: 0.78rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0.5rem; background: #141922; border-left: 2px solid #E8A83E; border-radius: 0 4px 4px 0; color: #F2F0EA; font-weight: 600;">
                    <span style="color: #E8A83E; font-size: 0.7rem;">●</span> 01 Executive Overview
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0.5rem; color: #9299A5;">
                    <span style="color: #626A76; font-size: 0.7rem;">○</span> 02 Geography & Time
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0.5rem; color: #9299A5;">
                    <span style="color: #626A76; font-size: 0.7rem;">○</span> 03 Attack & Industry
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0.5rem; color: #9299A5;">
                    <span style="color: #626A76; font-size: 0.7rem;">○</span> 04 Financial Impact
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0.5rem; color: #9299A5;">
                    <span style="color: #626A76; font-size: 0.7rem;">○</span> 05 Defense Dynamics
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0.5rem; color: #9299A5;">
                    <span style="color: #626A76; font-size: 0.7rem;">○</span> 06 Incident Explorer
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Filters Section Header & Reset Action
    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; padding-top: 0.75rem; border-top: 1px solid #1C222B;">
            <div style="font-size: 0.72rem; font-weight: 700; color: #626A76; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'IBM Plex Mono', monospace;">
                ANALYTICAL FILTERS
            </div>
            <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #E8A83E; background: rgba(232, 168, 62, 0.08); padding: 0.1rem 0.35rem; border-radius: 4px; border: 1px solid rgba(232, 168, 62, 0.2);">
                F1 – F11
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.sidebar.button("↺ Reset All Filters", width="stretch", help="Restores full 1,000 incident dataset"):
        reset_filters(df)
        st.rerun()

    st.sidebar.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # 4. Filter Groups (F1 - F11)
    # Group 1: Geography & Time
    with st.sidebar.expander("📍 Geography & Time (F1, F2)", expanded=True):
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

    # Group 2: Threat Vector & Target
    with st.sidebar.expander("⚔️ Attack & Industry (F3, F4, F5)", expanded=True):
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

    # Group 3: Vulnerability & Defense
    with st.sidebar.expander("🛡️ Security & Defense (F6, F7, F8)", expanded=False):
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

    # Group 4: Quantitative Impact
    with st.sidebar.expander("📊 Quantitative Impact (F9, F10, F11)", expanded=False):
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

    # Apply unified filtering logic (AND between dimensions, OR inside multiselects)
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

    # Active Result Set Telemetry Widget in Sidebar
    st.sidebar.markdown(
        f"""
        <div style="background: #141922; border: 1px solid #252C36; border-radius: 6px; padding: 0.65rem 0.8rem; margin-top: 1.15rem;">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.2rem;">
                <span style="font-size: 0.68rem; color: #9299A5; text-transform: uppercase; font-family: 'IBM Plex Mono', monospace;">ACTIVE COHORT</span>
                <span style="font-size: 0.68rem; color: #55B88A; font-family: 'IBM Plex Mono', monospace;">{len(filtered)/len(df)*100:.1f}%</span>
            </div>
            <div style="font-family: 'IBM Plex Mono', monospace; font-size: 1.15rem; font-weight: 700; color: #F2F0EA;">
                {len(filtered):,} <span style="font-size: 0.72rem; color: #626A76; font-weight: 400;">/ {len(df):,} incidents</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return filtered, filter_state


def render_active_filter_chips(filter_state: FilterState, total_matched: int, total_full: int):
    """Renders visual telemetry chips for all active non-default filters."""
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

    chip_html = "".join([f'<span class="filter-chip">▪ {chip}</span>' for chip in active_chips])
    status_text = f"ACTIVE FILTER COHORT: <b>{total_matched:,}</b> / <b>{total_full:,}</b> incidents ({total_matched/total_full*100:.1f}%)"

    st.markdown(
        f"""
        <div class="filter-chip-bar">
            <span style="font-size: 0.74rem; font-weight: 600; color: #9299A5; margin-right: 0.5rem; font-family: 'IBM Plex Mono', monospace;">
                {status_text}
            </span>
            {chip_html if chip_html else '<span style="font-size: 0.72rem; color: #626A76; font-family: \'IBM Plex Mono\', monospace;">Baseline State (Full 1,000 incident dataset)</span>'}
        </div>
        """,
        unsafe_allow_html=True
    )
