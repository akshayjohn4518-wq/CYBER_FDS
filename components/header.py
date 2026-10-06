"""
Obsidian Header and Global Telemetry Navigation Component.
Benchmark: Palantir / Bloomberg Terminal enterprise interface.
Features:
- Global system status, live telemetry heartbeat, analyst credential badge.
- Methodology & dataset validation modal expander.
- Precision section jump anchor rail.
"""
from datetime import datetime
import streamlit as st
from utils.validation import ValidationReport


def render_header(report: ValidationReport, total_records: int):
    """Renders the top enterprise header, telemetry status, caveats modal, and navigation bar."""
    current_time_str = datetime.now().strftime("%d %b %Y · %H:%M") + " IST"

    # 1. Compact Global Enterprise Header
    st.markdown(
        f"""
        <div class="obsidian-topbar">
            <div class="obsidian-brand-lockup">
                <span class="obsidian-mark">⬡</span>
                <div>
                    <div class="obsidian-brand-title">OBSIDIAN // THREAT INTELLIGENCE</div>
                    <div class="obsidian-brand-sub">Enterprise Security Analytics Platform</div>
                </div>
            </div>
            <div style="flex: 1; max-width: 380px; margin: 0 1rem;">
                <div style="background: #141922; border: 1px solid #252C36; border-radius: 6px; padding: 0.35rem 0.75rem; display: flex; align-items: center; gap: 0.5rem; font-size: 0.76rem; color: #626A76;">
                    <span>⌕</span>
                    <span style="color: #9299A5; font-family: 'Inter', sans-serif;">Search threats, countries, industries...</span>
                </div>
            </div>
            <div class="obsidian-telemetry-bar">
                <span class="live-badge">
                    <span class="live-dot"></span>
                    LIVE TELEMETRY
                </span>
                <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: #9299A5;">
                    {current_time_str}
                </span>
                <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; padding: 0.18rem 0.5rem; background: #141922; border: 1px solid #252C36; border-radius: 4px; color: #E8A83E;">
                    SEC-OP // LVL-4
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Methodology & Caveats Expander
    with st.expander("ℹ️ System Architecture, Schema Dimensions & Analytical Caveats", expanded=False):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.markdown(
                f"""
                <div style="font-size: 0.82rem; line-height: 1.5; color: #9299A5;">
                    <div style="font-weight: 700; color: #F2F0EA; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.04em;">Dataset Telemetry</div>
                    <div>• <b>Source:</b> <code>1,000 Verified Incident Logs</code></div>
                    <div>• <b>Temporal Span:</b> 2015 – 2024 (10-Year Horizon)</div>
                    <div>• <b>Coverage:</b> 10 Sovereign Nations</div>
                    <div>• <b>Integrity:</b> {'<span style="color:#55B88A">● Verified Clean</span>' if report.is_valid else '<span style="color:#D95C5C">⚠️ Attention</span>'}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                """
                <div style="font-size: 0.82rem; line-height: 1.5; color: #9299A5;">
                    <div style="font-weight: 700; color: #F2F0EA; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.04em;">Obsidian Dimensions</div>
                    <div>• <b>Attack Vectors:</b> 6 Distinct Categories</div>
                    <div>• <b>Industry Cohorts:</b> 7 Critical Sectors</div>
                    <div>• <b>Vulnerabilities:</b> 4 Primary Exploitation Vectors</div>
                    <div>• <b>Defenses:</b> 5 Architectural Mechanisms</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c3:
            st.markdown(
                """
                <div style="font-size: 0.82rem; line-height: 1.5; color: #9299A5;">
                    <div style="font-weight: 700; color: #F2F0EA; margin-bottom: 0.35rem; text-transform: uppercase; letter-spacing: 0.04em;">Operational Caveats</div>
                    <div>• <b>Benchmark Feed:</b> Structured analytical baseline for intelligence evaluation.</div>
                    <div>• <b>Affected Users:</b> Cumulative exposures across incidents.</div>
                    <div>• <b>Distributions:</b> Controlled synthetic benchmark characteristics.</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # 3. Sticky Section Navigation Rail
    st.markdown(
        """
        <div class="nav-anchor-bar">
            <span style="font-size: 0.72rem; font-weight: 700; color: #626A76; margin-right: 0.5rem; display: flex; align-items: center; letter-spacing: 0.06em; font-family: 'IBM Plex Mono', monospace;">
                NAV //
            </span>
            <a class="nav-anchor-link" href="#section-01-executive-overview">01 Executive Overview</a>
            <a class="nav-anchor-link" href="#section-02-global-threat-landscape">02 Threat Landscape</a>
            <a class="nav-anchor-link" href="#section-03-attack-intelligence">03 Attack Intelligence</a>
            <a class="nav-anchor-link" href="#section-04-financial-operational-impact">04 Financial Impact</a>
            <a class="nav-anchor-link" href="#section-05-defense-response-dynamics">05 Defense Dynamics</a>
            <a class="nav-anchor-link" href="#section-06-incident-explorer">06 Incident Explorer</a>
        </div>
        """,
        unsafe_allow_html=True
    )
