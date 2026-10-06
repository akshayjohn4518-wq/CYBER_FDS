"""
Obsidian Incident Explorer Table Component.
Implements Obsidian Threat Intelligence specification:
- Multi-field text search across categorical dimensions.
- Deterministic column sorting with default order.
- Compact pagination with monospaced range indicators.
- CSV telemetry export for both active page and full filtered dataset.
- Highest-impact incident callout with Obsidian amber left border.
"""
import math
import pandas as pd
import streamlit as st
from utils.export import prepare_filtered_csv, get_export_filename, generate_country_summary


def render_incident_explorer(df: pd.DataFrame):
    """Renders the interactive Incident Explorer with search, sort, pagination, and CSV download."""
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.85rem; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <h3 style="margin: 0; font-size: 1.1rem; font-weight: 700; color: #F2F0EA; letter-spacing: -0.01em;">
                    INCIDENT EXPLORER & AUDIT LOGS
                </h3>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.78rem; color: #9299A5;">
                    Granular record-level telemetry matching active filter criteria. Default sort: Country &rarr; Year &rarr; Attack Type.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:
        st.markdown(
            """
            <div class="cyber-empty-card">
                <div style="font-size: 1.8rem; margin-bottom: 0.5rem; color: #626A76;">⬡</div>
                <div style="font-size: 1rem; font-weight: 700; color: #F2F0EA; margin-bottom: 0.25rem;">
                    No incident records match active filter selection.
                </div>
                <div style="font-size: 0.8rem; color: #9299A5; margin-bottom: 1.25rem;">
                    Broaden filter parameters in the left sidebar navigation rail to restore telemetry.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Export toolbar at top of table section
    t1, t2 = st.columns([1, 1])
    with t1:
        csv_data = prepare_filtered_csv(df)
        st.download_button(
            label=f"↓ Export Filtered Records ({len(df):,} Rows, CSV)",
            data=csv_data,
            file_name=get_export_filename("cybersecurity_filtered_incidents"),
            mime="text/csv",
            width="stretch",
            help="Download the entire filtered dataset currently active across the dashboard."
        )
    with t2:
        country_summary_df = generate_country_summary(df)
        if not country_summary_df.empty:
            summary_csv = country_summary_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="↓ Export Sovereign Summary Aggregate (CSV)",
                data=summary_csv,
                file_name=get_export_filename("cybersecurity_country_summary"),
                mime="text/csv",
                width="stretch",
                help="Download country-level aggregate summary table."
            )

    st.markdown("<div style='height: 0.4rem;'></div>", unsafe_allow_html=True)

    # Search & Controls bar
    col_search, col_sort, col_order, col_page_size = st.columns([3, 2, 1.5, 1.5])

    with col_search:
        search_query = st.text_input(
            "Search within filtered records:",
            placeholder="Search country, attack vector, industry, defense...",
            key="table_search_input"
        )

    with col_sort:
        sort_column = st.selectbox(
            "Sort By:",
            options=[
                "Country",
                "Year",
                "Financial_Loss_Million_USD",
                "Attack_Type",
                "Affected_Users",
                "Resolution_Time_Hours",
                "Severity"
            ],
            index=0,
            key="table_sort_col"
        )

    with col_order:
        sort_order = st.selectbox(
            "Order:",
            options=["Ascending", "Descending"],
            index=0 if sort_column in ["Country", "Year", "Attack_Type"] else 1,
            key="table_sort_dir"
        )

    with col_page_size:
        page_size = st.selectbox(
            "Rows / Page:",
            options=[10, 25, 50, 100],
            index=1,
            key="table_page_size"
        )

    # Process search query
    filtered_table = df.copy()
    if search_query:
        query_lower = search_query.strip().lower()
        search_mask = (
            filtered_table["Country"].astype(str).str.lower().str.contains(query_lower) |
            filtered_table["Attack_Type"].astype(str).str.lower().str.contains(query_lower) |
            filtered_table["Target_Industry"].astype(str).str.lower().str.contains(query_lower) |
            filtered_table["Attack_Source"].astype(str).str.lower().str.contains(query_lower) |
            filtered_table["Vulnerability_Type"].astype(str).str.lower().str.contains(query_lower) |
            filtered_table["Defense_Mechanism"].astype(str).str.lower().str.contains(query_lower) |
            filtered_table["Severity"].astype(str).str.lower().str.contains(query_lower)
        )
        filtered_table = filtered_table[search_mask]

    # Process sorting
    is_ascending = (sort_order == "Ascending")
    if sort_column == "Country":
        filtered_table = filtered_table.sort_values(
            ["Country", "Year", "Attack_Type", "Financial_Loss_Million_USD"],
            ascending=[is_ascending, True, True, False]
        )
    else:
        filtered_table = filtered_table.sort_values(by=sort_column, ascending=is_ascending)

    total_table_rows = len(filtered_table)
    total_pages = max(1, math.ceil(total_table_rows / page_size))

    # Pagination state
    if "table_current_page" not in st.session_state:
        st.session_state.table_current_page = 1

    # Keep page within valid bounds
    if st.session_state.table_current_page > total_pages:
        st.session_state.table_current_page = total_pages
    if st.session_state.table_current_page < 1:
        st.session_state.table_current_page = 1

    curr_page = st.session_state.table_current_page
    start_idx = (curr_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_table_rows)

    # Display range info
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.4rem 0 0.65rem 0; font-size: 0.76rem; color: #9299A5; font-family: 'IBM Plex Mono', monospace;">
            <span>RECORDS <b>{start_idx + 1 if total_table_rows > 0 else 0}</b> – <b>{end_idx}</b> OF <b>{total_table_rows:,}</b> {f'(filtered from {len(df):,})' if search_query else ''}</span>
            <span>PAGE {curr_page} / {total_pages}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    page_data = filtered_table.iloc[start_idx:end_idx]

    # Render table with custom formatting
    display_df = page_data[[
        "Country", "Year", "Attack_Type", "Target_Industry",
        "Financial_Loss_Million_USD", "Affected_Users", "Resolution_Time_Hours",
        "Attack_Source", "Vulnerability_Type", "Defense_Mechanism", "Severity"
    ]].copy()

    display_df = display_df.rename(columns={
        "Financial_Loss_Million_USD": "Loss ($M)",
        "Affected_Users": "Affected Users",
        "Resolution_Time_Hours": "Resolution (hrs)",
        "Attack_Type": "Attack Vector",
        "Target_Industry": "Target Industry",
        "Attack_Source": "Source",
        "Vulnerability_Type": "Vulnerability",
        "Defense_Mechanism": "Defense Architecture",
        "Severity": "Severity Level"
    })

    st.dataframe(
        display_df.style.format({
            "Loss ($M)": "${:,.2f} M",
            "Affected Users": "{:,}",
            "Resolution (hrs)": "{:,} hrs"
        }),
        width="stretch",
        hide_index=True,
        height=min(450, 40 + len(page_data) * 36)
    )

    # Pagination navigation controls
    c_prev, c_space, c_jump, c_next = st.columns([1.5, 3, 2, 1.5])
    with c_prev:
        if st.button("← Previous", disabled=(curr_page <= 1), width="stretch"):
            st.session_state.table_current_page -= 1
            st.rerun()

    with c_jump:
        selected_page = st.number_input(
            "Jump to page",
            min_value=1,
            max_value=total_pages,
            value=curr_page,
            step=1,
            label_visibility="collapsed",
            key="table_page_jump"
        )
        if selected_page != curr_page:
            st.session_state.table_current_page = int(selected_page)
            st.rerun()

    with c_next:
        if st.button("Next →", disabled=(curr_page >= total_pages), width="stretch"):
            st.session_state.table_current_page += 1
            st.rerun()

    # Highest impact record callout
    if not df.empty:
        highest_impact = df.sort_values("Financial_Loss_Million_USD", ascending=False).iloc[0]
        st.markdown(
            f"""
            <div style="background: #141922; border: 1px solid #252C36; border-left: 3px solid #E8A83E; border-radius: 6px; padding: 0.75rem 1rem; margin-top: 1.25rem; font-size: 0.8rem; line-height: 1.45;">
                <span style="font-weight: 700; color: #E8A83E; font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; font-size: 0.74rem;">PEAK EXPOSURE RECORD // </span>
                <span style="color: #F2F0EA;">
                    <b>{highest_impact['Country']}</b> ({highest_impact['Year']}) logged maximum exposure of <b>${highest_impact['Financial_Loss_Million_USD']:,.2f} Million</b> from <b>{highest_impact['Attack_Type']}</b> targeting <b>{highest_impact['Target_Industry']}</b> ({highest_impact['Affected_Users']:,} affected users, resolved in {highest_impact['Resolution_Time_Hours']} hours via {highest_impact['Defense_Mechanism']}).
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
