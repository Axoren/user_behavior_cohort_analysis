"""Cohort retention analysis for transaction-level customer data.

This script builds monthly cohorts, calculates customer retention rates,
and saves a retention heatmap for reporting.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


DATA_PATH = Path("data/data.csv")
OUTPUT_DIR = Path("screenshots")
OUTPUT_PATH = OUTPUT_DIR / "retention_heatmap.png"


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load transaction-level data."""
    return pd.read_csv(path, encoding="ISO-8859-1")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean transaction data for cohort analysis."""
    clean_df = df.copy()
    clean_df.columns = clean_df.columns.str.strip()
    clean_df = clean_df.dropna(subset=["CustomerID", "InvoiceDate"])
    clean_df["InvoiceDate"] = pd.to_datetime(clean_df["InvoiceDate"])
    clean_df["CustomerID"] = clean_df["CustomerID"].astype(int)
    return clean_df


def get_month_start(series: pd.Series) -> pd.Series:
    """Convert datetime values to first day of month."""
    return series.dt.to_period("M").dt.to_timestamp()


def build_cohort_table(df: pd.DataFrame) -> pd.DataFrame:
    """Build a retention table with cohorts as rows and cohort age as columns."""
    cohort_df = df.copy()
    cohort_df["invoice_month"] = get_month_start(cohort_df["InvoiceDate"])
    cohort_df["cohort_month"] = cohort_df.groupby("CustomerID")["invoice_month"].transform(
        "min"
    )

    cohort_df["cohort_index"] = (
        (cohort_df["invoice_month"].dt.year - cohort_df["cohort_month"].dt.year) * 12
        + (cohort_df["invoice_month"].dt.month - cohort_df["cohort_month"].dt.month)
        + 1
    )

    cohort_counts = (
        cohort_df.groupby(["cohort_month", "cohort_index"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )

    cohort_pivot = cohort_counts.pivot_table(
        index="cohort_month",
        columns="cohort_index",
        values="active_customers",
    )

    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_sizes, axis=0)

    return retention


def save_retention_heatmap(retention: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> None:
    """Save a monthly cohort retention heatmap."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(14, 8))
    sns.heatmap(
        retention,
        annot=True,
        fmt=".0%",
        cmap="Blues",
        cbar_kws={"label": "Retention rate"},
    )
    plt.title("Monthly Cohort Retention")
    plt.xlabel("Cohort Age, Months")
    plt.ylabel("Cohort Month")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()


def print_summary(retention: pd.DataFrame) -> None:
    """Print concise retention summary."""
    month_2_retention = retention.get(2)
    month_3_retention = retention.get(3)

    print("Cohort Retention Summary")
    print("=" * 50)
    print(f"Number of cohorts: {retention.shape[0]}")

    if month_2_retention is not None:
        print(f"Average Month 2 retention: {month_2_retention.mean():.2%}")

    if month_3_retention is not None:
        print(f"Average Month 3 retention: {month_3_retention.mean():.2%}")

    print("=" * 50)


def main() -> None:
    """Run the cohort retention analysis pipeline."""
    raw_df = load_data()
    clean_df = clean_data(raw_df)
    retention = build_cohort_table(clean_df)
    save_retention_heatmap(retention)
    print_summary(retention)


if __name__ == "__main__":
    main()
