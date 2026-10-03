"""
Data loader module for Global Cybersecurity Threats dataset.
Handles file ingestion, schema normalization, derived calculations, and caching.
"""
import os
from typing import Tuple
import pandas as pd
import streamlit as st
from utils.validation import validate_raw_dataset, ValidationReport

ISO3_MAP = {
    "China": "CHN",
    "India": "IND",
    "UK": "GBR",
    "Germany": "DEU",
    "France": "FRA",
    "Australia": "AUS",
    "Russia": "RUS",
    "Brazil": "BRA",
    "Japan": "JPN",
    "USA": "USA",
}

DEFAULT_CANDIDATE_PATHS = [
    os.path.join("data", "Global_Cybersecurity_Threats_2015-2024_1000_records.csv"),
    os.path.join("data", "Cybersecurity_Final_Countrywise.csv"),
    "Global_Cybersecurity_Threats_2015-2024_1000_records.csv",
    "Cybersecurity_Final_Countrywise.csv",
]


def find_data_file() -> str:
    """Finds the existing dataset file from configured candidate paths."""
    for p in DEFAULT_CANDIDATE_PATHS:
        if os.path.exists(p):
            return p
    return ""


@st.cache_data(show_spinner="Loading and validating cybersecurity dataset...")
def load_dataset(file_path: str = None) -> Tuple[pd.DataFrame, ValidationReport]:
    """
    Loads, cleans, validates, and enhances the cybersecurity dataset.
    Returns (cleaned_df, validation_report).
    """
    target_path = file_path or find_data_file()
    if not target_path or not os.path.exists(target_path):
        report = ValidationReport(is_valid=False)
        report.errors.append(f"Source dataset not found. Checked: {DEFAULT_CANDIDATE_PATHS}")
        return pd.DataFrame(), report

    # Ingest raw CSV
    try:
        raw_df = pd.read_csv(target_path)
    except Exception as e:
        report = ValidationReport(is_valid=False)
        report.errors.append(f"Failed to read CSV at '{target_path}': {str(e)}")
        return pd.DataFrame(), report

    # If it's already the standardized countrywise CSV
    if "Financial_Loss_Million_USD" in raw_df.columns and "Country_Code" in raw_df.columns:
        df = raw_df.copy()
        report = ValidationReport(is_valid=True, row_count=len(df), column_count=len(df.columns))
        report.metadata = {
            "source_path": target_path,
            "unique_countries": df["Country"].nunique(),
            "unique_years": sorted(df["Year"].unique().tolist()),
            "unique_attack_types": df["Attack_Type"].nunique(),
            "unique_industries": df["Target_Industry"].nunique(),
        }
        return df, report

    # Run validation on raw dataset
    report = validate_raw_dataset(raw_df)
    if not report.is_valid:
        return pd.DataFrame(), report

    # Rename to internal standard names
    col_mapping = {
        "Country": "Country",
        "Year": "Year",
        "Attack Type": "Attack_Type",
        "Target Industry": "Target_Industry",
        "Financial Loss (in Million $)": "Financial_Loss_Million_USD",
        "Number of Affected Users": "Affected_Users",
        "Attack Source": "Attack_Source",
        "Security Vulnerability Type": "Vulnerability_Type",
        "Defense Mechanism Used": "Defense_Mechanism",
        "Incident Resolution Time (in Hours)": "Resolution_Time_Hours",
    }
    df = raw_df.rename(columns=col_mapping).copy()

    # Clean text columns
    text_cols = [
        "Country", "Attack_Type", "Target_Industry",
        "Attack_Source", "Vulnerability_Type", "Defense_Mechanism"
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)

    # Cast numeric columns
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype(int)
    df["Financial_Loss_Million_USD"] = pd.to_numeric(df["Financial_Loss_Million_USD"], errors="coerce")
    df["Affected_Users"] = pd.to_numeric(df["Affected_Users"], errors="coerce").astype(int)
    df["Resolution_Time_Hours"] = pd.to_numeric(df["Resolution_Time_Hours"], errors="coerce").astype(int)

    # Derived attributes
    df["Country_Code"] = df["Country"].map(ISO3_MAP)
    df["Severity"] = pd.qcut(
        df["Financial_Loss_Million_USD"],
        q=3,
        labels=["Low", "Medium", "High"]
    ).astype(str)

    df["Period"] = pd.cut(
        df["Year"],
        bins=[2014, 2017, 2020, 2024],
        labels=["2015-2017", "2018-2020", "2021-2024"]
    ).astype(str)

    # Sort deterministically
    df = df.sort_values(
        ["Country", "Year", "Attack_Type", "Financial_Loss_Million_USD"],
        ascending=[True, True, True, False]
    ).reset_index(drop=True)

    df["Incident_No"] = df.groupby("Country").cumcount() + 1

    # Standardize column order
    ordered_cols = [
        "Country", "Country_Code", "Incident_No", "Year", "Period",
        "Attack_Type", "Target_Industry", "Attack_Source", "Vulnerability_Type",
        "Defense_Mechanism", "Financial_Loss_Million_USD", "Severity",
        "Affected_Users", "Resolution_Time_Hours"
    ]
    df = df[[c for c in ordered_cols if c in df.columns]]

    report.cleaning_operations.append("Standardized column schema and trimmed excess whitespace.")
    report.cleaning_operations.append("Calculated ISO-3 Country_Code, 3-tier Severity, Period, and Country-level Incident_No.")
    report.metadata["source_path"] = target_path

    return df, report
