"""
Incident Explorer Table Component.
Implements PRD Section 9:
- Multi-field text search across categorical dimensions.
- Column sorting with default order (Country -> Year -> Attack Type).
- Client-friendly pagination (10, 25, 50, 100 records per page).
- Full filtered dataset CSV export (all records, not just active page).
- High-impact records identification without misleading 'live incident' tags.
"""
import math
import pandas as pd
import streamlit as st
from utils.export import prepare_filtered_csv, get_export_filename, generate_country_summary


def render_incident_explorer(df: pd.DataFrame):
    """Renders the interactive Incident Explorer with search, sort, pagination, and CSV download."""
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.5rem;">
            <div>
                <h3 style="margin: 0; font-size: 1.25rem; font-weight: 700; color: #F3F4F6;">
                    🔎 Incident Explorer & Records Inspector
                </h3>
                <p style="margin: 0.2rem 0 0 0; font-size: 0.82rem; color: #9CA3AF;">
                    Inspect individual records matching the shared filter state. Default sort: Country &rarr; Year &rarr; Attack Type.
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
                <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🔍</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #F3F4F6; margin-bottom: 0.25rem;">
                    No incidents match your current filters.
                </div>
                <div style="font-size: 0.85rem; color: #9CA3AF; margin-bottom: 1.25rem;">
                    Try widening your filter selections in the sidebar or click Reset All Filters.
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
            label=f"📥 Export All {len(df):,} Filtered Records (CSV)",
            data=csv_data,
            file_name=get_export_filename("cybersecurity_filtered_incidents"),
            mime="text/csv",
            use_container_width=True,
            help="Download the entire filtered dataset currently active across the dashboard."
        )
    with t2:
        country_summary_df = generate_country_summary(df)
        if not country_summary_df.empty:
            summary_csv = country_summary_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📊 Export Country Summary Table (CSV)",
                data=summary_csv,
                file_name=get_export_filename("cybersecurity_country_summary"),
                mime="text/csv",
                use_container_width=True,
                help="Download country-level aggregate summary table."
            )

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    # Search & Controls bar
    col_search, col_sort, col_order, col_page_size = st.columns([3, 2, 1.5, 1.5])

    with col_search:
        search_query = st.text_input(
            "Search within filtered records:",
            placeholder="Type country, attack type, industry, defense...",
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
        <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5rem 0 0.75rem 0; font-size: 0.82rem; color: #9CA3AF;">
            <span>Showing records <b>{start_idx + 1 if total_table_rows > 0 else 0}</b> to <b>{end_idx}</b> of <b>{total_table_rows:,}</b> {f'(filtered from {len(df):,})' if search_query else ''}</span>
            <span style="font-family: 'JetBrains Mono', monospace;">Page {curr_page} of {total_pages}</span>
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
        "Attack_Type": "Attack Type",
        "Target_Industry": "Target Industry",
        "Attack_Source": "Source",
        "Vulnerability_Type": "Vulnerability",
        "Defense_Mechanism": "Defense"
    })

    st.dataframe(
        display_df.style.format({
            "Loss ($M)": "${:,.2f} M",
            "Affected Users": "{:,}",
            "Resolution (hrs)": "{:,} hrs"
        }),
        use_container_width=True,
        hide_index=True,
        height=min(450, 40 + len(page_data) * 36)
    )

    # Pagination navigation controls
    c_prev, c_space, c_jump, c_next = st.columns([1.5, 3, 2, 1.5])
    with c_prev:
        if st.button("⬅️ Previous", disabled=(curr_page <= 1), use_container_width=True):
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
        if st.button("Next ➡️", disabled=(curr_page >= total_pages), use_container_width=True):
            st.session_state.table_current_page += 1
            st.rerun()

    # Highest impact record callout (PRD Section 3.5: "Highest-impact records in the selected dataset")
    if not df.empty:
        highest_impact = df.sort_values("Financial_Loss_Million_USD", ascending=False).iloc[0]
        st.markdown(
            f"""
            <div style="background: #111827; border: 1px solid #1E293B; border-left: 4px solid #38BDF8; border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1.5rem; font-size: 0.84rem;">
                <span style="font-weight: 700; color: #38BDF8;">Highest-Impact Record in Selected Dataset:</span>
                <span style="color: #F3F4F6;">
                    <b>{highest_impact['Country']}</b> ({highest_impact['Year']}) suffered a <b>${highest_impact['Financial_Loss_Million_USD']:,.2f} Million</b> loss from a <b>{highest_impact['Attack_Type']}</b> attack targeting the <b>{highest_impact['Target_Industry']}</b> industry ({highest_impact['Affected_Users']:,} affected users, resolved in {highest_impact['Resolution_Time_Hours']} hours via {highest_impact['Defense_Mechanism']}).
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
