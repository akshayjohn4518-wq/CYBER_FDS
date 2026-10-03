"""
KPI calculation engine and baseline comparisons for the dashboard.
Adheres strictly to PRD Section 7:
- Baseline is always the full unfiltered dataset (not previous year).
- Explicit non-temporal delta labeling.
- Handles empty/zero states gracefully with 'N/A'.
"""
from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class KPIMetric:
    label: str
    current_value: float
    current_display: str
    baseline_value: float
    baseline_display: str
    delta_value: Optional[float]
    delta_display: str
    unit: str
    description: str


@dataclass
class KPISuite:
    total_incidents: KPIMetric
    total_loss: KPIMetric
    avg_loss: KPIMetric
    total_affected_users: KPIMetric
    avg_resolution_time: KPIMetric
    high_severity_share: KPIMetric
    countries_represented: KPIMetric
    sample_size: int
    is_empty: bool
    is_small_sample: bool


def calculate_kpis(filtered_df: pd.DataFrame, full_df: pd.DataFrame) -> KPISuite:
    """Calculates all 6 core KPIs + countries count with comparison against full dataset."""
    full_count = len(full_df)
    filtered_count = len(filtered_df)
    is_empty = filtered_count == 0
    is_small_sample = 0 < filtered_count < 30

    # 1. Full dataset baselines
    base_incidents = full_count
    base_total_loss = full_df["Financial_Loss_Million_USD"].sum() if not full_df.empty else 0.0
    base_avg_loss = full_df["Financial_Loss_Million_USD"].mean() if not full_df.empty else 0.0
    base_affected_users = full_df["Affected_Users"].sum() if not full_df.empty else 0
    base_avg_res = full_df["Resolution_Time_Hours"].mean() if not full_df.empty else 0.0
    base_high_sev_share = (
        (full_df["Severity"] == "High").sum() / full_count * 100.0 if full_count > 0 else 0.0
    )
    base_countries = full_df["Country"].nunique() if not full_df.empty else 0

    if is_empty:
        return KPISuite(
            total_incidents=KPIMetric(
                label="Total Incidents",
                current_value=0,
                current_display="0",
                baseline_value=base_incidents,
                baseline_display=f"{base_incidents:,}",
                delta_value=-base_incidents,
                delta_display=f"-{base_incidents:,}",
                unit="incidents",
                description="Number of recorded incidents matching filters"
            ),
            total_loss=KPIMetric(
                label="Total Financial Loss",
                current_value=0.0,
                current_display="$0.0 M",
                baseline_value=base_total_loss,
                baseline_display=f"${base_total_loss:,.1f} M",
                delta_value=-base_total_loss,
                delta_display=f"-${base_total_loss:,.1f} M",
                unit="M$",
                description="Cumulative financial loss in million USD"
            ),
            avg_loss=KPIMetric(
                label="Average Loss / Incident",
                current_value=0.0,
                current_display="N/A",
                baseline_value=base_avg_loss,
                baseline_display=f"${base_avg_loss:,.2f} M",
                delta_value=None,
                delta_display="N/A",
                unit="M$",
                description="Mean loss per recorded incident"
            ),
            total_affected_users=KPIMetric(
                label="Recorded Affected Users",
                current_value=0,
                current_display="0",
                baseline_value=base_affected_users,
                baseline_display=f"{base_affected_users:,}",
                delta_value=-base_affected_users,
                delta_display=f"-{base_affected_users:,}",
                unit="users",
                description="Sum of recorded affected user metric (non-unique)"
            ),
            avg_resolution_time=KPIMetric(
                label="Avg Resolution Time",
                current_value=0.0,
                current_display="N/A",
                baseline_value=base_avg_res,
                baseline_display=f"{base_avg_res:.1f} hrs",
                delta_value=None,
                delta_display="N/A",
                unit="hours",
                description="Mean incident recovery and resolution duration"
            ),
            high_severity_share=KPIMetric(
                label="High-Severity Share",
                current_value=0.0,
                current_display="N/A",
                baseline_value=base_high_sev_share,
                baseline_display=f"{base_high_sev_share:.1f}%",
                delta_value=None,
                delta_display="N/A",
                unit="%",
                description="Proportion of incidents falling into top loss tertile"
            ),
            countries_represented=KPIMetric(
                label="Countries Represented",
                current_value=0,
                current_display="0",
                baseline_value=base_countries,
                baseline_display=str(base_countries),
                delta_value=-base_countries,
                delta_display=f"-{base_countries}",
                unit="countries",
                description="Distinct countries matching current selection"
            ),
            sample_size=0,
            is_empty=True,
            is_small_sample=False
        )

    # 2. Filtered calculations
    curr_incidents = filtered_count
    curr_total_loss = filtered_df["Financial_Loss_Million_USD"].sum()
    curr_avg_loss = filtered_df["Financial_Loss_Million_USD"].mean()
    curr_affected_users = int(filtered_df["Affected_Users"].sum())
    curr_avg_res = filtered_df["Resolution_Time_Hours"].mean()
    curr_high_sev_count = int((filtered_df["Severity"] == "High").sum())
    curr_high_sev_share = (curr_high_sev_count / filtered_count) * 100.0
    curr_countries = filtered_df["Country"].nunique()

    # 3. Baseline differences
    delta_incidents = curr_incidents - base_incidents
    delta_total_loss = curr_total_loss - base_total_loss
    delta_avg_loss = curr_avg_loss - base_avg_loss
    delta_affected_users = curr_affected_users - base_affected_users
    delta_avg_res = curr_avg_res - base_avg_res
    delta_high_sev = curr_high_sev_share - base_high_sev_share
    delta_countries = curr_countries - base_countries

    def format_diff(val: float, prefix: str = "", suffix: str = "", decimals: int = 1) -> str:
        sign = "+" if val > 0 else ""
        if decimals == 0:
            return f"{sign}{prefix}{int(val):,}{suffix}"
        return f"{sign}{prefix}{val:,.{decimals}f}{suffix}"

    return KPISuite(
        total_incidents=KPIMetric(
            label="Total Incidents",
            current_value=curr_incidents,
            current_display=f"{curr_incidents:,}",
            baseline_value=base_incidents,
            baseline_display=f"{base_incidents:,}",
            delta_value=delta_incidents,
            delta_display=format_diff(delta_incidents, decimals=0),
            unit="incidents",
            description="Number of recorded incidents matching filters"
        ),
        total_loss=KPIMetric(
            label="Total Financial Loss",
            current_value=curr_total_loss,
            current_display=f"${curr_total_loss:,.1f} M",
            baseline_value=base_total_loss,
            baseline_display=f"${base_total_loss:,.1f} M",
            delta_value=delta_total_loss,
            delta_display=format_diff(delta_total_loss, prefix="$", suffix=" M", decimals=1),
            unit="M$",
            description="Cumulative financial loss in million USD"
        ),
        avg_loss=KPIMetric(
            label="Average Loss / Incident",
            current_value=curr_avg_loss,
            current_display=f"${curr_avg_loss:,.2f} M",
            baseline_value=base_avg_loss,
            baseline_display=f"${base_avg_loss:,.2f} M",
            delta_value=delta_avg_loss,
            delta_display=format_diff(delta_avg_loss, prefix="$", suffix=" M", decimals=2),
            unit="M$",
            description="Mean loss per recorded incident"
        ),
        total_affected_users=KPIMetric(
            label="Recorded Affected Users",
            current_value=curr_affected_users,
            current_display=f"{curr_affected_users:,}",
            baseline_value=base_affected_users,
            baseline_display=f"{base_affected_users:,}",
            delta_value=delta_affected_users,
            delta_display=format_diff(delta_affected_users, decimals=0),
            unit="users",
            description="Sum of recorded affected user metric (non-unique individuals)"
        ),
        avg_resolution_time=KPIMetric(
            label="Avg Resolution Time",
            current_value=curr_avg_res,
            current_display=f"{curr_avg_res:.1f} hrs",
            baseline_value=base_avg_res,
            baseline_display=f"{base_avg_res:.1f} hrs",
            delta_value=delta_avg_res,
            delta_display=format_diff(delta_avg_res, suffix=" hrs", decimals=1),
            unit="hours",
            description="Mean incident recovery and resolution duration"
        ),
        high_severity_share=KPIMetric(
            label="High-Severity Share",
            current_value=curr_high_sev_share,
            current_display=f"{curr_high_sev_share:.1f}%",
            baseline_value=base_high_sev_share,
            baseline_display=f"{base_high_sev_share:.1f}%",
            delta_value=delta_high_sev,
            delta_display=format_diff(delta_high_sev, suffix=" pp", decimals=1),
            unit="%",
            description="Proportion of incidents falling into top loss tertile (> 33rd percentile)"
        ),
        countries_represented=KPIMetric(
            label="Countries Represented",
            current_value=curr_countries,
            current_display=str(curr_countries),
            baseline_value=base_countries,
            baseline_display=str(base_countries),
            delta_value=delta_countries,
            delta_display=format_diff(delta_countries, decimals=0),
            unit="countries",
            description="Distinct countries matching current selection"
        ),
        sample_size=filtered_count,
        is_empty=is_empty,
        is_small_sample=is_small_sample
    )
