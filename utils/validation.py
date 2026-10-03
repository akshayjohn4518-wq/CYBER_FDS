"""
Validation utilities for the Global Cybersecurity Threats dataset.
Validates schema, data types, ranges, duplicates, and categorical values.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any
import pandas as pd


@dataclass
class ValidationReport:
    is_valid: bool = True
    row_count: int = 0
    column_count: int = 0
    missing_cells: int = 0
    duplicate_rows: int = 0
    cleaning_operations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


REQUIRED_RAW_COLUMNS = [
    "Country",
    "Year",
    "Attack Type",
    "Target Industry",
    "Financial Loss (in Million $)",
    "Number of Affected Users",
    "Attack Source",
    "Security Vulnerability Type",
    "Defense Mechanism Used",
    "Incident Resolution Time (in Hours)"
]

EXPECTED_STANDARDIZED_COLUMNS = [
    "Country",
    "Country_Code",
    "Incident_No",
    "Year",
    "Period",
    "Attack_Type",
    "Target_Industry",
    "Attack_Source",
    "Vulnerability_Type",
    "Defense_Mechanism",
    "Financial_Loss_Million_USD",
    "Severity",
    "Affected_Users",
    "Resolution_Time_Hours"
]


def validate_raw_dataset(df: pd.DataFrame) -> ValidationReport:
    """Validates raw incoming CSV dataframe against PRD data integrity rules."""
    report = ValidationReport()
    report.row_count = len(df)
    report.column_count = len(df.columns)

    # 1. Column existence
    missing_cols = [col for col in REQUIRED_RAW_COLUMNS if col not in df.columns]
    if missing_cols:
        report.is_valid = False
        report.errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        return report

    # 2. Missing values check
    missing_sum = int(df[REQUIRED_RAW_COLUMNS].isnull().sum().sum())
    report.missing_cells = missing_sum
    if missing_sum > 0:
        report.warnings.append(f"Found {missing_sum} missing cell(s) across required fields.")

    # 3. Duplicate rows check
    duplicates = int(df.duplicated().sum())
    report.duplicate_rows = duplicates
    if duplicates > 0:
        report.warnings.append(f"Found {duplicates} duplicate row(s) in source dataset.")

    # 4. Numeric value & range validation
    try:
        years = pd.to_numeric(df["Year"], errors="coerce")
        invalid_years = years.isna() | (years < 2010) | (years > 2030)
        if invalid_years.any():
            report.warnings.append(f"{invalid_years.sum()} record(s) contain unexpected year values.")

        losses = pd.to_numeric(df["Financial Loss (in Million $)"], errors="coerce")
        neg_losses = losses.isna() | (losses < 0)
        if neg_losses.any():
            report.errors.append(f"{neg_losses.sum()} record(s) contain invalid or negative financial losses.")
            report.is_valid = False

        users = pd.to_numeric(df["Number of Affected Users"], errors="coerce")
        neg_users = users.isna() | (users < 0)
        if neg_users.any():
            report.errors.append(f"{neg_users.sum()} record(s) contain invalid or negative affected user counts.")
            report.is_valid = False

        res_time = pd.to_numeric(df["Incident Resolution Time (in Hours)"], errors="coerce")
        neg_res = res_time.isna() | (res_time < 0)
        if neg_res.any():
            report.errors.append(f"{neg_res.sum()} record(s) contain invalid or negative resolution times.")
            report.is_valid = False
    except Exception as e:
        report.is_valid = False
        report.errors.append(f"Numeric validation failed with error: {str(e)}")

    # 5. Metadata summary
    report.metadata = {
        "unique_countries": df["Country"].nunique() if "Country" in df else 0,
        "unique_years": sorted(df["Year"].dropna().unique().tolist()) if "Year" in df else [],
        "unique_attack_types": df["Attack Type"].nunique() if "Attack Type" in df else 0,
        "unique_industries": df["Target Industry"].nunique() if "Target Industry" in df else 0,
    }

    return report
