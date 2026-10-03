"""
Header and Navigation component for the Cybersecurity Dashboard.
Displays product title, academic credits, validation status, caveats modal, and section jump anchors.
"""
import streamlit as st
from utils.validation import ValidationReport


def render_header(report: ValidationReport, total_records: int):
    """Renders the top application header, badges, caveats expander, and navigation bar."""
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.25rem;">
                    <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #34D399; box-shadow: 0 0 10px #34D399;"></span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #38BDF8; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700;">
                        Cyber Threat Intelligence Workspace • V1.1
                    </span>
                    <span style="background: rgba(56, 189, 248, 0.12); color: #38BDF8; font-size: 0.72rem; padding: 0.1rem 0.45rem; border-radius: 4px; border: 1px solid rgba(56, 189, 248, 0.25);">
                        CSE-QE-2A
                    </span>
                </div>
                <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #CBD5E1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Global Cybersecurity Threats Analytics Dashboard
                </h1>
                <p style="margin: 0.35rem 0 0 0; color: #9CA3AF; font-size: 0.9rem;">
                    Temporal and categorical intelligence exploration across 1,000 incidents (2015–2024).
                </p>
            </div>
            <div style="text-align: right; background: #111827; border: 1px solid #1E293B; border-radius: 10px; padding: 0.6rem 0.9rem;">
                <div style="font-size: 0.72rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em;">Project Owner</div>
                <div style="font-size: 0.9rem; font-weight: 700; color: #F3F4F6;">REDDY &bull; CSE-QE-2A</div>
                <div style="font-size: 0.74rem; color: #38BDF8;">Fundamentals of Data Science</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Methodology & Caveats Expander
    with st.expander("ℹ️ Dataset Information, Validation Status & Analytical Caveats", expanded=False):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.markdown(
                f"""
                **Dataset Verification**
                - **Source File:** `Global_Cybersecurity_Threats_2015-2024_1000_records.csv`
                - **Total Records:** `{total_records:,}`
                - **Time Period:** 2015 – 2024 (10 Years)
                - **Geographic Coverage:** 10 Sovereign Nations
                - **Integrity Status:** {'✅ Verified Clean' if report.is_valid else '⚠️ Attention Needed'}
                """
            )
        with c2:
            st.markdown(
                """
                **Schema Dimensions**
                - **Attack Types:** 6 (Ransomware, DDoS, Malware, Phishing, SQL Injection, MitM)
                - **Target Industries:** 7 (Banking, IT, Healthcare, Government, Retail, etc.)
                - **Vulnerability Types:** 4 (Social Engineering, Zero-day, Unpatched, Weak Passwords)
                - **Defense Mechanisms:** 5 (Firewall, Encryption, VPN, Antivirus, AI-based)
                """
            )
        with c3:
            st.markdown(
                """
                **Methodological Caveats (PRD §3.5)**
                - **Exploration Dataset:** Benchmark analytical data for coursework evaluation; not a live SOC telemetry feed.
                - **Affected Users:** Represents cumulative incident-reported exposure, not unique de-duplicated human individuals.
                - **Statistical Uniformity:** Record distributions exhibit near-uniform synthetic benchmark characteristics.
                """
            )

    # Sticky Section Anchor Navigation
    st.markdown(
        """
        <div class="nav-anchor-bar">
            <span style="font-size: 0.8rem; font-weight: 700; color: #6B7280; margin-right: 0.4rem; display: flex; align-items: center;">SECTIONS:</span>
            <a class="nav-anchor-link" href="#section-01-executive-overview">01. Overview</a>
            <a class="nav-anchor-link" href="#section-02-global-threat-landscape">02. Threat Landscape</a>
            <a class="nav-anchor-link" href="#section-03-attack-intelligence">03. Attack Intelligence</a>
            <a class="nav-anchor-link" href="#section-04-financial-operational-impact">04. Financial Impact</a>
            <a class="nav-anchor-link" href="#section-05-defense-response-dynamics">05. Defense & Response</a>
            <a class="nav-anchor-link" href="#section-06-incident-explorer">06. Incident Explorer</a>
        </div>
        """,
        unsafe_allow_html=True
    )
