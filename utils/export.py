"""
Export utility module for downloading filtered datasets and summaries.
"""
from datetime import datetime
import pandas as pd


def prepare_filtered_csv(df: pd.DataFrame) -> bytes:
    """Encodes the filtered dataframe into UTF-8 CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")


def generate_country_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generates an aggregated summary table for countries in the filtered dataset."""
    if df.empty:
        return pd.DataFrame()

    def mode_or_na(series: pd.Series):
        counts = series.value_counts()
        return counts.index[0] if not counts.empty else "N/A"

    summary = df.groupby(["Country", "Country_Code"], as_index=False).agg(
        Incidents=("Incident_No", "count"),
        Total_Loss_Million_USD=("Financial_Loss_Million_USD", "sum"),
        Avg_Loss_Million_USD=("Financial_Loss_Million_USD", "mean"),
        Total_Affected_Users=("Affected_Users", "sum"),
        Avg_Resolution_Hours=("Resolution_Time_Hours", "mean"),
        Primary_Attack_Type=("Attack_Type", mode_or_na),
        Primary_Industry=("Target_Industry", mode_or_na),
        Primary_Defense=("Defense_Mechanism", mode_or_na)
    ).sort_values("Total_Loss_Million_USD", ascending=False).reset_index(drop=True)

    summary.insert(0, "Rank", summary.index + 1)
    summary["Total_Loss_Million_USD"] = summary["Total_Loss_Million_USD"].round(2)
    summary["Avg_Loss_Million_USD"] = summary["Avg_Loss_Million_USD"].round(2)
    summary["Avg_Resolution_Hours"] = summary["Avg_Resolution_Hours"].round(1)

    return summary


def get_export_filename(prefix: str = "cybersecurity_incidents_filtered") -> str:
    """Generates timestamped filename for export."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.csv"
