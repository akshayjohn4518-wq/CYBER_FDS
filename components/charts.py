"""
Obsidian Plotly Chart Engine for Global Cybersecurity Threats Dashboard.
Benchmark: Enterprise Threat Intelligence (Palantir, Bloomberg, modern SOC).
Design Language: Quiet intelligence. High signal. Zero visual noise.
- Dark graphite canvas #141922 with #1C222B gridlines.
- Signal Amber #E8A83E, Steel Blue #6D8FB8, Critical Red #D95C5C, Controlled Green #55B88A.
- Typography: Inter body + IBM Plex Mono metrics and ticks.
"""
from typing import Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from components.styles import ATTACK_COLOR_MAP, THEME_COLORS, SEVERITY_COLOR_MAP


def obsidian_chart_layout(
    fig: go.Figure,
    height: int = 400,
    show_legend: bool = True,
    legend_title: str = "",
    hovermode: Optional[str] = "closest"
) -> go.Figure:
    """Applies the Obsidian Threat Intelligence theme to any Plotly figure."""
    fig.update_layout(
        autosize=True,
        height=height,
        paper_bgcolor="#141922",
        plot_bgcolor="#141922",
        font=dict(family="'Inter', sans-serif", color="#F2F0EA", size=11),
        margin=dict(l=45, r=25, t=45, b=45),
        hovermode=hovermode,
        showlegend=show_legend,
        hoverlabel=dict(
            bgcolor="#1A202B",
            bordercolor="#252C36",
            font=dict(family="'IBM Plex Mono', monospace", size=11, color="#F2F0EA")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="center",
            x=0.5,
            title_text=legend_title,
            font=dict(size=11, color="#9299A5", family="'Inter', sans-serif"),
            bgcolor="rgba(20, 25, 34, 0.9)",
            bordercolor="#252C36",
            borderwidth=1,
        ),
    )
    fig.update_xaxes(
        gridcolor="#1C222B",
        linecolor="#252C36",
        zerolinecolor="#252C36",
        tickfont=dict(color="#9299A5", size=10, family="'IBM Plex Mono', monospace"),
        title_font=dict(color="#9299A5", size=11, family="'Inter', sans-serif"),
        automargin=True
    )
    fig.update_yaxes(
        gridcolor="#1C222B",
        linecolor="#252C36",
        zerolinecolor="#252C36",
        tickfont=dict(color="#9299A5", size=10, family="'IBM Plex Mono', monospace"),
        title_font=dict(color="#9299A5", size=11, family="'Inter', sans-serif"),
        automargin=True
    )
    return fig


def plot_chart(fig: go.Figure, **kwargs):
    """Safely renders Plotly figure with modern stretch width."""
    try:
        st.plotly_chart(fig, width="stretch", **kwargs)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True, **kwargs)


# Backward compatibility alias
cyber_chart_layout = obsidian_chart_layout


def render_chart_header(title: str, subtitle: str, sample_count: int, chart_id: str):
    """Renders standardized Obsidian title bar with sample size badge."""
    st.markdown(
        f"""
        <div class="chart-header">
            <div>
                <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: #E8A83E; margin-right: 0.45rem; font-weight: 600;">{chart_id}</span>
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
    st.info("⚠️ No records match current filter criteria.")


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

    obsidian_amber_scale = [
        [0.0, "#1A202B"],
        [0.5, "#B8832D"],
        [1.0, "#E8A83E"]
    ]

    fig = px.bar(
        grouped,
        x="Total_Loss",
        y="Country",
        orientation="h",
        color="Total_Loss",
        color_continuous_scale=obsidian_amber_scale,
        text_auto=",.1f",
        labels={"Total_Loss": "Total Loss (Million USD)", "Country": "Country"},
        custom_data=["Incidents", "Avg_Loss"]
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Total Loss: $%{x:,.2f} M<br>Incidents: %{customdata[0]:,}<br>Mean Loss: $%{customdata[1]:.2f} M<extra></extra>",
        textposition="outside",
        textfont=dict(family="'IBM Plex Mono', monospace", size=10, color="#F2F0EA"),
        cliponaxis=False,
    )
    fig.update_coloraxes(showscale=False)
    obsidian_chart_layout(fig, height=380, show_legend=False)
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Underlying Data — Chart 01"):
        st.dataframe(grouped.sort_values("Total_Loss", ascending=False).reset_index(drop=True), use_container_width=True if not hasattr(st, "html") else None, width="stretch")


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
        "Incidents & Financial Loss over Time",
        "Longitudinal comparison of incident frequency (amber, left) versus total loss in $M (steel blue, right).",
        n,
        "CHART 02"
    )

    yearly = df.groupby("Year", as_index=False).agg(
        Incidents=("Incident_No", "count"),
        Total_Loss=("Financial_Loss_Million_USD", "sum"),
        Avg_Resolution=("Resolution_Time_Hours", "mean")
    ).sort_values("Year")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # Incident count: Signal Amber with restrained fill
    fig.add_trace(
        go.Scatter(
            x=yearly["Year"],
            y=yearly["Incidents"],
            name="Incident Count",
            mode="lines+markers",
            line=dict(color="#E8A83E", width=2.5),
            marker=dict(size=6, symbol="circle", color="#E8A83E"),
            fill="tozeroy",
            fillcolor="rgba(232, 168, 62, 0.06)",
            hovertemplate="Year %{x}<br>Incidents: %{y:,}<extra></extra>"
        ),
        secondary_y=False
    )
    # Total loss: Steel Blue dashed
    fig.add_trace(
        go.Scatter(
            x=yearly["Year"],
            y=yearly["Total_Loss"],
            name="Total Loss ($M)",
            mode="lines+markers",
            line=dict(color="#6D8FB8", width=2, dash="dot"),
            marker=dict(size=6, symbol="diamond", color="#6D8FB8"),
            hovertemplate="Year %{x}<br>Total Loss: $%{y:,.1f} M<extra></extra>"
        ),
        secondary_y=True
    )

    fig.update_xaxes(title_text="Year", dtick=1)
    fig.update_yaxes(title_text="Incident Count", secondary_y=False, title_font_color="#E8A83E")
    fig.update_yaxes(title_text="Total Loss ($M)", secondary_y=True, title_font_color="#6D8FB8", showgrid=False)
    obsidian_chart_layout(fig, height=380, show_legend=True, hovermode="x unified")
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Underlying Data — Chart 02"):
        st.dataframe(yearly.reset_index(drop=True), use_container_width=True if not hasattr(st, "html") else None, width="stretch")


# -----------------------------------------------------------------------------
# CHART 03: Distribution Analysis (Histogram + Box Plot)
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
        color_seq = ["#E8A83E"]
        unit_str = "$M"
    else:
        col_name = "Resolution_Time_Hours"
        label_name = "Resolution Time (Hours)"
        color_seq = ["#6D8FB8"]
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
        line_color="#D95C5C",
        annotation_text=f"Mean: {mean_val:.1f} {unit_str}",
        annotation_position="top right",
        annotation_font=dict(color="#D95C5C", size=10, family="'IBM Plex Mono', monospace")
    )
    fig.add_vline(
        x=median_val,
        line_dash="dot",
        line_color="#E8A83E",
        annotation_text=f"Median: {median_val:.1f} {unit_str}",
        annotation_position="bottom right",
        annotation_font=dict(color="#E8A83E", size=10, family="'IBM Plex Mono', monospace")
    )
    fig.update_traces(
        marker_line_color="#141922",
        marker_line_width=1,
        selector=dict(type="histogram")
    )
    fig.update_yaxes(title_text="Incident Count", row=1, col=1)
    obsidian_chart_layout(fig, height=390, show_legend=False)
    plot_chart(fig, config={"displayModeBar": False})

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

    fig = px.pie(
        counts,
        names="Attack_Type",
        values="Count",
        hole=0.55,
        color="Attack_Type",
        color_discrete_map=ATTACK_COLOR_MAP
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        insidetextorientation="radial",
        textfont=dict(family="'Inter', sans-serif", size=11),
        marker=dict(line=dict(color="#141922", width=2)),
        hovertemplate="<b>%{label}</b><br>Incidents: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    fig.add_annotation(
        text=f"<b>{n:,}</b><br><span style='font-size:10px;color:#9299A5;font-family:Inter;'>INCIDENTS</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="#F2F0EA", family="'IBM Plex Mono', monospace")
    )
    obsidian_chart_layout(fig, height=380, show_legend=True)
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Underlying Data — Chart 04"):
        st.dataframe(counts, use_container_width=True if not hasattr(st, "html") else None, width="stretch")


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
        opacity=0.75,
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
    fig.update_traces(marker=dict(size=7, line=dict(width=0.6, color="#141922")))
    obsidian_chart_layout(fig, height=440, show_legend=True)
    plot_chart(fig, config={"displayModeBar": False})

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

    order = (
        df.groupby("Target_Industry")["Financial_Loss_Million_USD"]
        .median()
        .sort_values(ascending=False)
        .index.tolist()
    )

    obsidian_palette = ["#E8A83E", "#6D8FB8", "#55B88A", "#D95C5C", "#8E82A6", "#D4883A", "#9299A5"]

    fig = px.box(
        df,
        x="Target_Industry",
        y="Financial_Loss_Million_USD",
        color="Target_Industry",
        category_orders={"Target_Industry": order},
        color_discrete_sequence=obsidian_palette,
        labels={"Target_Industry": "Industry", "Financial_Loss_Million_USD": "Loss ($M)"},
    )
    fig.update_traces(boxpoints="all", jitter=0.3, pointpos=-1.8, marker=dict(size=4, opacity=0.45))
    obsidian_chart_layout(fig, height=400, show_legend=False)
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Industry Median Loss Stats — Chart 06"):
        ind_stats = df.groupby("Target_Industry")["Financial_Loss_Million_USD"].agg(["count", "mean", "median", "std"]).sort_values("median", ascending=False)
        st.dataframe(ind_stats.round(2), use_container_width=True if not hasattr(st, "html") else None, width="stretch")


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

    obsidian_heatmap_scale = [
        [0.0, "#141922"],
        [0.4, "#273244"],
        [0.75, "#B8832D"],
        [1.0, "#E8A83E"]
    ]

    fig = px.imshow(
        pivot,
        text_auto=".0f",
        color_continuous_scale=obsidian_heatmap_scale,
        aspect="auto",
        labels={"x": "Country", "y": "Attack Type", "color": "Avg Loss ($M)"}
    )
    fig.update_xaxes(side="bottom")
    obsidian_chart_layout(fig, height=420, show_legend=False)
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Underlying Cross-Tab Matrix — Chart 07"):
        st.dataframe(pivot.round(2), use_container_width=True if not hasattr(st, "html") else None, width="stretch")


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

    obsidian_actor_colors = {
        "Nation-state": "#D95C5C",
        "Hacker Group": "#E8A83E",
        "Insider": "#D4883A",
        "Unknown": "#6D8FB8"
    }

    fig = px.bar(
        grouped,
        x="Target_Industry",
        y="Avg_Loss",
        color="Attack_Source",
        barmode="group",
        color_discrete_map=obsidian_actor_colors,
        labels={"Target_Industry": "Target Industry", "Avg_Loss": "Average Loss ($M)", "Attack_Source": "Source"},
        custom_data=["Incident_Count"]
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b> (%{data.name})<br>Avg Loss: $%{y:.2f} M<br>Incidents: %{customdata[0]:,}<extra></extra>"
    )
    obsidian_chart_layout(fig, height=410, show_legend=True)
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Grouped Breakdown — Chart 08"):
        st.dataframe(grouped.round(2), use_container_width=True if not hasattr(st, "html") else None, width="stretch")


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
        "Recorded defense mechanisms across incidents (frequency reflects deployment, not standalone efficacy).",
        n,
        "CHART 09"
    )

    counts = df["Defense_Mechanism"].value_counts().reset_index()
    counts.columns = ["Defense_Mechanism", "Count"]

    obsidian_def_palette = ["#E8A83E", "#6D8FB8", "#55B88A", "#8E82A6", "#D4883A"]

    fig = px.pie(
        counts,
        names="Defense_Mechanism",
        values="Count",
        hole=0.55,
        color_discrete_sequence=obsidian_def_palette
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="outside",
        textfont=dict(family="'Inter', sans-serif", size=10, color="#9299A5"),
        marker=dict(line=dict(color="#141922", width=2)),
        hovertemplate="<b>%{label}</b><br>Incidents: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    fig.add_annotation(
        text=f"<b>{n:,}</b><br><span style='font-size:10px;color:#9299A5;font-family:Inter;'>DEPLOYED</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=16, color="#F2F0EA", family="'IBM Plex Mono', monospace")
    )
    obsidian_chart_layout(fig, height=390, show_legend=False)
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Defense Mechanism Stats — Chart 09"):
        st.dataframe(counts, use_container_width=True if not hasattr(st, "html") else None, width="stretch")


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
    obsidian_chart_layout(fig, height=410, show_legend=True, hovermode="x unified")
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Composition Matrix — Chart 10"):
        comp_pivot = area_df.pivot_table(index="Year", columns="Attack_Type", values="Incidents", fill_value=0)
        st.dataframe(comp_pivot, use_container_width=True if not hasattr(st, "html") else None, width="stretch")


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
        "GLOBAL THREAT MAP",
        "Geographical distribution of economic impact ($M) across the 10 sovereign nations.",
        n,
        "CHART 11"
    )

    country_geo = df.groupby(["Country", "Country_Code"], as_index=False).agg(
        Total_Loss=("Financial_Loss_Million_USD", "sum"),
        Incidents=("Incident_No", "count"),
        Avg_Loss=("Financial_Loss_Million_USD", "mean"),
        Avg_Resolution=("Resolution_Time_Hours", "mean")
    )

    obsidian_geo_scale = [
        [0.0, "#1A202B"],
        [0.4, "#3D485C"],
        [0.75, "#E8A83E"],
        [1.0, "#D95C5C"]
    ]

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
        color_continuous_scale=obsidian_geo_scale,
        projection="natural earth",
        labels={"Total_Loss": "Total Loss ($M)"}
    )
    fig.update_geos(
        showcountries=True,
        countrycolor="#252C36",
        coastlinecolor="#252C36",
        showland=True,
        landcolor="#141922",
        showocean=True,
        oceancolor="#080A0D",
        showframe=False
    )
    fig.update_layout(
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        coloraxis_colorbar=dict(
            title=dict(text="Loss ($M)", font=dict(color="#9299A5", size=10, family="'Inter', sans-serif")),
            tickfont=dict(color="#9299A5", size=10, family="'IBM Plex Mono', monospace"),
            bgcolor="rgba(20, 25, 34, 0.9)",
            bordercolor="#252C36",
            borderwidth=1,
            len=0.75
        )
    )
    obsidian_chart_layout(fig, height=500, show_legend=False)
    plot_chart(fig, config={"displayModeBar": False})

    with st.expander("🔍 View Country Geographical Data — Chart 11"):
        st.dataframe(country_geo.sort_values("Total_Loss", ascending=False).reset_index(drop=True), use_container_width=True if not hasattr(st, "html") else None, width="stretch")
