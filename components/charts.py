"""
Plotly Chart Engine for Global Cybersecurity Threats Dashboard.
Implements all 11 visualizations required by PRD Section 8 with consistent
dark cyber styling, hover tooltips, sample counts, units, and view-data toggles.
"""
from typing import Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from components.styles import ATTACK_COLOR_MAP, THEME_COLORS


def cyber_chart_layout(
    fig: go.Figure,
    height: int = 420,
    show_legend: bool = True,
    legend_title: str = "",
    hovermode: Optional[str] = "closest"
) -> go.Figure:
    """Applies a consistent, polished cyber dark theme to any Plotly figure."""
    fig.update_layout(
        autosize=True,
        height=height,
        paper_bgcolor="rgba(17, 24, 39, 0.6)",
        plot_bgcolor="rgba(17, 24, 39, 0.4)",
        font=dict(family="'Plus Jakarta Sans', sans-serif", color="#CBD5E1", size=12),
        margin=dict(l=45, r=25, t=55, b=45),
        hovermode=hovermode,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title_text=legend_title,
            font=dict(size=11, color="#9CA3AF"),
            bgcolor="rgba(17, 24, 39, 0.8)",
            bordercolor="#263244",
            borderwidth=1,
        ),
    )
    fig.update_xaxes(
        gridcolor="#1E293B",
        linecolor="#263244",
        zerolinecolor="#263244",
        tickfont=dict(color="#9CA3AF", size=11),
        title_font=dict(color="#CBD5E1", size=12),
        automargin=True
    )
    fig.update_yaxes(
        gridcolor="#1E293B",
        linecolor="#263244",
        zerolinecolor="#263244",
        tickfont=dict(color="#9CA3AF", size=11),
        title_font=dict(color="#CBD5E1", size=12),
        automargin=True
    )
    return fig


def render_chart_header(title: str, subtitle: str, sample_count: int, chart_id: str):
    """Renders standardized title bar with sample size badge."""
    st.markdown(
        f"""
        <div class="chart-header">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #38BDF8; margin-right: 0.4rem;">{chart_id}</span>
                <span class="chart-title">{title}</span>
            </div>
            <span class="chart-sample-badge">n = {sample_count:,}</span>
        </div>
        <div class="chart-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


def render_empty_chart(title: str, chart_id: str):
    """Graceful placeholder when current filter produces 0 matching records."""
    render_chart_header(title, "No records match current filter criteria.", 0, chart_id)
    st.info("⚠️ No data available to render this visualization with the current filter selection.")


# -----------------------------------------------------------------------------
# CHART 01: Financial Loss by Country (Horizontal Bar)
# -----------------------------------------------------------------------------
def render_chart_01(df: pd.DataFrame):
    """Chart 01: Horizontal bar chart of Total Financial Loss by Country."""
    if df.empty:
        render_empty_chart("Financial Loss by Country", "CHART 01")
        return

    n = len(df)
    render_chart_header(
        "Total Financial Loss by Country",
        "Cumulative financial loss (Million USD) across sovereign nations, sorted descending.",
        n,
        "CHART 01"
    )

    grouped = df.groupby("Country", as_index=False).agg(
        Total_Loss=("Financial_Loss_Million_USD", "sum"),
        Incidents=("Incident_No", "count"),
        Avg_Loss=("Financial_Loss_Million_USD", "mean")
    ).sort_values("Total_Loss", ascending=True)

    fig = px.bar(
        grouped,
        x="Total_Loss",
        y="Country",
        orientation="h",
        color="Total_Loss",
        color_continuous_scale="Tealgrn",
        text_auto=",.1f",
        labels={"Total_Loss": "Total Loss (Million USD)", "Country": "Country"},
        custom_data=["Incidents", "Avg_Loss"]
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Total Loss: $%{x:,.2f} M<br>Incidents: %{customdata[0]:,}<br>Mean Loss: $%{customdata[1]:.2f} M<extra></extra>",
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_coloraxes(showscale=False)
    cyber_chart_layout(fig, height=380, show_legend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "toImageButtonOptions": {"format": "png"}})

    with st.expander("🔍 View Underlying Data — Chart 01"):
        st.dataframe(grouped.sort_values("Total_Loss", ascending=False).reset_index(drop=True), use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 02: Yearly Incident and Loss Trend (Dual-Axis Line)
# -----------------------------------------------------------------------------
def render_chart_02(df: pd.DataFrame):
    """Chart 02: Dual-axis line chart of Incidents and Total Loss per Year."""
    if df.empty:
        render_empty_chart("Yearly Incident and Loss Trend", "CHART 02")
        return

    n = len(df)
    render_chart_header(
        "Yearly Incident & Loss Dynamics (2015–2024)",
        "Temporal comparison of incident frequency (left) versus cumulative loss in $M (right).",
        n,
        "CHART 02"
    )

    yearly = df.groupby("Year", as_index=False).agg(
        Incidents=("Incident_No", "count"),
        Total_Loss=("Financial_Loss_Million_USD", "sum"),
        Avg_Resolution=("Resolution_Time_Hours", "mean")
    ).sort_values("Year")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=yearly["Year"],
            y=yearly["Incidents"],
            name="Incident Count",
            mode="lines+markers",
            line=dict(color="#38BDF8", width=3),
            marker=dict(size=8, symbol="circle"),
            hovertemplate="Year %{x}<br>Incidents: %{y:,}<extra></extra>"
        ),
        secondary_y=False
    )
    fig.add_trace(
        go.Scatter(
            x=yearly["Year"],
            y=yearly["Total_Loss"],
            name="Total Loss ($M)",
            mode="lines+markers",
            line=dict(color="#F87171", width=3, dash="dot"),
            marker=dict(size=8, symbol="diamond"),
            hovertemplate="Year %{x}<br>Total Loss: $%{y:,.1f} M<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_xaxes(title_text="Year", dtick=1)
    fig.update_yaxes(title_text="Number of Incidents", secondary_y=False, title_font_color="#38BDF8")
    fig.update_yaxes(title_text="Total Loss ($M)", secondary_y=True, title_font_color="#F87171", showgrid=False)
    cyber_chart_layout(fig, height=380, show_legend=True, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Underlying Data — Chart 02"):
        st.dataframe(yearly.reset_index(drop=True), use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 03: Distribution Analysis (Histogram + Marginal Box Plot)
# -----------------------------------------------------------------------------
def render_chart_03(df: pd.DataFrame):
    """Chart 03: Toggleable distribution analysis between Loss and Resolution Time."""
    if df.empty:
        render_empty_chart("Distribution Analysis", "CHART 03")
        return

    n = len(df)
    render_chart_header(
        "Parametric Distribution & Boxplot Analysis",
        "Explore frequency density, central tendency, quartiles, and outliers with parametric toggle.",
        n,
        "CHART 03"
    )

    var_choice = st.radio(
        "Select Distribution Metric:",
        ["Financial Loss (Million USD)", "Resolution Time (Hours)"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if var_choice.startswith("Financial"):
        col_name = "Financial_Loss_Million_USD"
        label_name = "Financial Loss (Million USD)"
        color_seq = ["#38BDF8"]
        unit_str = "$M"
    else:
        col_name = "Resolution_Time_Hours"
        label_name = "Resolution Time (Hours)"
        color_seq = ["#34D399"]
        unit_str = "hrs"

    mean_val = df[col_name].mean()
    median_val = df[col_name].median()

    fig = px.histogram(
        df,
        x=col_name,
        nbins=20,
        marginal="box",
        color_discrete_sequence=color_seq,
        labels={col_name: label_name},
        opacity=0.85
    )
    fig.add_vline(
        x=mean_val,
        line_dash="dash",
        line_color="#F87171",
        annotation_text=f"Mean: {mean_val:.1f} {unit_str}",
        annotation_position="top right",
        annotation_font=dict(color="#F87171", size=11)
    )
    fig.add_vline(
        x=median_val,
        line_dash="dot",
        line_color="#FBBF24",
        annotation_text=f"Median: {median_val:.1f} {unit_str}",
        annotation_position="bottom right",
        annotation_font=dict(color="#FBBF24", size=11)
    )
    fig.update_traces(
        marker_line_color="#080B12",
        marker_line_width=1,
        selector=dict(type="histogram")
    )
    fig.update_yaxes(title_text="Incident Count", row=1, col=1)
    cyber_chart_layout(fig, height=400, show_legend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Summary Statistics — Chart 03"):
        st.write(df[[col_name]].describe().T)


# -----------------------------------------------------------------------------
# CHART 04: Attack Type Distribution (Donut Chart)
# -----------------------------------------------------------------------------
def render_chart_04(df: pd.DataFrame):
    """Chart 04: Donut chart showing share of incidents by attack vector."""
    if df.empty:
        render_empty_chart("Attack Type Distribution", "CHART 04")
        return

    n = len(df)
    render_chart_header(
        "Attack Type Vector Breakdown",
        "Proportionate distribution of threats across the 6 tracked cybersecurity attack modalities.",
        n,
        "CHART 04"
    )

    counts = df["Attack_Type"].value_counts().reset_index()
    counts.columns = ["Attack_Type", "Count"]

    color_seq = [ATTACK_COLOR_MAP.get(a, "#38BDF8") for a in counts["Attack_Type"]]

    fig = px.pie(
        counts,
        names="Attack_Type",
        values="Count",
        hole=0.45,
        color="Attack_Type",
        color_discrete_map=ATTACK_COLOR_MAP
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        insidetextorientation="radial",
        marker=dict(line=dict(color="#111827", width=2)),
        hovertemplate="<b>%{label}</b><br>Incidents: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    cyber_chart_layout(fig, height=380, show_legend=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Underlying Data — Chart 04"):
        st.dataframe(counts, use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 05: Affected Users vs Financial Loss (Scatter Plot)
# -----------------------------------------------------------------------------
def render_chart_05(df: pd.DataFrame):
    """Chart 05: Scatter plot analyzing correlation between affected users and economic loss."""
    if df.empty:
        render_empty_chart("Affected Users vs Financial Loss", "CHART 05")
        return

    n = len(df)
    render_chart_header(
        "Affected Users vs Financial Loss Correlation",
        "Evaluation of user impact footprint versus economic damage with log-scaling toggle.",
        n,
        "CHART 05"
    )

    use_log = st.checkbox("Apply Log Scale to Affected Users (X-Axis)", value=False, key="scatter_log_toggle")

    fig = px.scatter(
        df,
        x="Affected_Users",
        y="Financial_Loss_Million_USD",
        color="Attack_Type",
        color_discrete_map=ATTACK_COLOR_MAP,
        opacity=0.72,
        log_x=use_log,
        hover_data={
            "Country": True,
            "Year": True,
            "Target_Industry": True,
            "Affected_Users": ":,",
            "Financial_Loss_Million_USD": ":.2f"
        },
        labels={
            "Affected_Users": "Recorded Affected Users",
            "Financial_Loss_Million_USD": "Financial Loss ($M)",
            "Attack_Type": "Attack Type"
        }
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=0.8, color="#080B12")))
    cyber_chart_layout(fig, height=450, show_legend=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Correlation Analysis — Chart 05"):
        corr = df["Affected_Users"].corr(df["Financial_Loss_Million_USD"])
        st.caption(f"Pearson Correlation Coefficient (r) = {corr:.4f} (Confirms near-zero linear dependence).")


# -----------------------------------------------------------------------------
# CHART 06: Financial Loss by Industry (Box Plot)
# -----------------------------------------------------------------------------
def render_chart_06(df: pd.DataFrame):
    """Chart 06: Box plot showing loss spread across target industries."""
    if df.empty:
        render_empty_chart("Financial Loss by Target Industry", "CHART 06")
        return

    n = len(df)
    render_chart_header(
        "Financial Loss Dispersion by Target Industry",
        "Median losses, interquartile ranges, and outliers sorted by industry median.",
        n,
        "CHART 06"
    )

    # Sort industries by median loss descending
    order = (
        df.groupby("Target_Industry")["Financial_Loss_Million_USD"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )

    fig = px.box(
        df,
        x="Target_Industry",
        y="Financial_Loss_Million_USD",
        color="Target_Industry",
        category_orders={"Target_Industry": order},
        color_discrete_sequence=px.colors.qualitative.Dark24,
        labels={"Target_Industry": "Industry", "Financial_Loss_Million_USD": "Loss ($M)"},
    )
    fig.update_traces(boxpoints="all", jitter=0.3, pointpos=-1.8, marker=dict(size=4, opacity=0.5))
    cyber_chart_layout(fig, height=420, show_legend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Industry Median Loss Stats — Chart 06"):
        ind_stats = df.groupby("Target_Industry")["Financial_Loss_Million_USD"].agg(["count", "mean", "median", "std"]).sort_values("median", ascending=False)
        st.dataframe(ind_stats.round(2), use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 07: Attack Type × Country Heatmap
# -----------------------------------------------------------------------------
def render_chart_07(df: pd.DataFrame):
    """Chart 07: Heatmap matrix of mean loss across Attack Types and Sovereign Nations."""
    if df.empty:
        render_empty_chart("Attack Type × Country Loss Heatmap", "CHART 07")
        return

    n = len(df)
    render_chart_header(
        "Attack Type × Country Average Loss Heatmap",
        "Cross-tabulated average financial impact ($M) per vector-nation intersection. Empty cells preserved.",
        n,
        "CHART 07"
    )

    pivot = df.pivot_table(
        index="Attack_Type",
        columns="Country",
        values="Financial_Loss_Million_USD",
        aggfunc="mean"
    )

    fig = px.imshow(
        pivot,
        text_auto=".0f",
        color_continuous_scale="Viridis",
        aspect="auto",
        labels={"x": "Country", "y": "Attack Type", "color": "Avg Loss ($M)"}
    )
    fig.update_xaxes(side="bottom")
    cyber_chart_layout(fig, height=440, show_legend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Underlying Cross-Tab Matrix — Chart 07"):
        st.dataframe(pivot.round(2), use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 08: Industry by Attack Source (Grouped Bar Chart)
# -----------------------------------------------------------------------------
def render_chart_08(df: pd.DataFrame):
    """Chart 08: Grouped bar chart comparing average loss by industry and threat actor source."""
    if df.empty:
        render_empty_chart("Industry Loss by Threat Actor Source", "CHART 08")
        return

    n = len(df)
    render_chart_header(
        "Industry Loss by Threat Actor Source",
        "Comparison of mean losses across target sectors attributed to Nation-state, Hacker Group, Insider, or Unknown.",
        n,
        "CHART 08"
    )

    grouped = df.groupby(["Target_Industry", "Attack_Source"], as_index=False).agg(
        Avg_Loss=("Financial_Loss_Million_USD", "mean"),
        Incident_Count=("Incident_No", "count")
    )

    fig = px.bar(
        grouped,
        x="Target_Industry",
        y="Avg_Loss",
        color="Attack_Source",
        barmode="group",
        color_discrete_sequence=["#38BDF8", "#F87171", "#FBBF24", "#34D399"],
        labels={"Target_Industry": "Target Industry", "Avg_Loss": "Average Loss ($M)", "Attack_Source": "Source"},
        custom_data=["Incident_Count"]
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b> (%{data.name})<br>Avg Loss: $%{y:.2f} M<br>Incidents: %{customdata[0]:,}<extra></extra>"
    )
    cyber_chart_layout(fig, height=420, show_legend=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Grouped Breakdown — Chart 08"):
        st.dataframe(grouped.round(2), use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 09: Defense Mechanism Distribution (Donut Chart)
# -----------------------------------------------------------------------------
def render_chart_09(df: pd.DataFrame):
    """Chart 09: Donut chart displaying utilization of defense mechanisms."""
    if df.empty:
        render_empty_chart("Defense Mechanism Distribution", "CHART 09")
        return

    n = len(df)
    render_chart_header(
        "Defense Mechanism Deployment Frequency",
        "Recorded defense mechanisms across incidents (Note: frequency reflects deployment, not standalone efficacy).",
        n,
        "CHART 09"
    )

    counts = df["Defense_Mechanism"].value_counts().reset_index()
    counts.columns = ["Defense_Mechanism", "Count"]

    fig = px.pie(
        counts,
        names="Defense_Mechanism",
        values="Count",
        hole=0.55,
        color_discrete_sequence=["#38BDF8", "#818CF8", "#34D399", "#FBBF24", "#F472B6"]
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="outside",
        marker=dict(line=dict(color="#111827", width=2)),
        hovertemplate="<b>%{label}</b><br>Incidents: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    fig.add_annotation(
        text=f"<b>{n:,}</b><br><span style='font-size:11px;color:#9CA3AF;'>incidents</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=18, color="#F3F4F6")
    )
    cyber_chart_layout(fig, height=400, show_legend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Defense Mechanism Stats — Chart 09"):
        st.dataframe(counts, use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 10: Yearly Attack Composition (Stacked Area Chart)
# -----------------------------------------------------------------------------
def render_chart_10(df: pd.DataFrame):
    """Chart 10: Stacked area chart showing year-by-year attack composition."""
    if df.empty:
        render_empty_chart("Yearly Attack Composition", "CHART 10")
        return

    n = len(df)
    render_chart_header(
        "Yearly Attack Vector Trajectory (Stacked Area)",
        "Cumulative evolution of attack types across the 2015–2024 longitudinal window.",
        n,
        "CHART 10"
    )

    area_df = df.groupby(["Year", "Attack_Type"]).size().reset_index(name="Incidents")

    fig = px.area(
        area_df,
        x="Year",
        y="Incidents",
        color="Attack_Type",
        color_discrete_map=ATTACK_COLOR_MAP,
        labels={"Year": "Year", "Incidents": "Incidents", "Attack_Type": "Attack Vector"}
    )
    fig.update_xaxes(dtick=1)
    cyber_chart_layout(fig, height=420, show_legend=True, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Composition Matrix — Chart 10"):
        comp_pivot = area_df.pivot_table(index="Year", columns="Attack_Type", values="Incidents", fill_value=0)
        st.dataframe(comp_pivot, use_container_width=True)


# -----------------------------------------------------------------------------
# CHART 11: Geographic Financial Impact (Choropleth Map)
# -----------------------------------------------------------------------------
def render_chart_11(df: pd.DataFrame):
    """Chart 11: Interactive choropleth map with total economic losses per country."""
    if df.empty:
        render_empty_chart("Geographic Financial Impact Map", "CHART 11")
        return

    n = len(df)
    render_chart_header(
        "Geographic Financial Impact (Choropleth Map)",
        "Global distribution of economic damage ($M) across the 10 covered sovereign nations.",
        n,
        "CHART 11"
    )

    country_geo = df.groupby(["Country", "Country_Code"], as_index=False).agg(
        Total_Loss=("Financial_Loss_Million_USD", "sum"),
        Incidents=("Incident_No", "count"),
        Avg_Loss=("Financial_Loss_Million_USD", "mean"),
        Avg_Resolution=("Resolution_Time_Hours", "mean")
    )

    fig = px.choropleth(
        country_geo,
        locations="Country_Code",
        color="Total_Loss",
        hover_name="Country",
        hover_data={
            "Country_Code": False,
            "Total_Loss": ":,.1f",
            "Incidents": True,
            "Avg_Loss": ":.2f",
            "Avg_Resolution": ":.1f"
        },
        color_continuous_scale="Reds",
        projection="natural earth",
        labels={"Total_Loss": "Total Loss ($M)"}
    )
    fig.update_geos(
        showcountries=True,
        countrycolor="#334155",
        coastlinecolor="#334155",
        showland=True,
        landcolor="#111827",
        showocean=True,
        oceancolor="#080B12",
        showframe=False
    )
    fig.update_layout(
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        coloraxis_colorbar=dict(
            title=dict(text="Loss ($M)", font=dict(color="#9CA3AF", size=11)),
            tickfont=dict(color="#9CA3AF", size=10),
            bgcolor="rgba(17, 24, 39, 0.8)",
            bordercolor="#263244",
            borderwidth=1,
            len=0.75
        )
    )
    cyber_chart_layout(fig, height=520, show_legend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

    with st.expander("🔍 View Country Geographical Data — Chart 11"):
        st.dataframe(country_geo.sort_values("Total_Loss", ascending=False).reset_index(drop=True), use_container_width=True)
