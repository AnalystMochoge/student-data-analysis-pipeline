"""Clean, transform, analyze, and save the student data."""

import argparse
from pathlib import Path

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate/empty rows and fill missing numeric values."""
    df = df.drop_duplicates().dropna(how="all").copy()
    numeric_columns = df.select_dtypes(include="number").columns
    df.loc[:, numeric_columns] = df.loc[:, numeric_columns].fillna(
        df.loc[:, numeric_columns].median()
    )
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Add readable labels for the dataset's study-time categories."""
    df = df.copy()
    if "studytime" in df.columns:
        study_labels = {
            1: "Under 2 hours",
            2: "2–5 hours",
            3: "5–10 hours",
            4: "Over 10 hours",
        }
        df["study_group"] = df["studytime"].map(study_labels)
    return df


def analyze_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Summarize study and attendance-related measures by pass status."""
    group_column = "passed" if "passed" in df.columns else "study_group"
    aggregations = {}
    if "studytime" in df.columns:
        aggregations["avg_studytime"] = ("studytime", "mean")
    if "absences" in df.columns:
        aggregations["avg_absences"] = ("absences", "mean")
    aggregations["students"] = (group_column, "count")

    summary = df.groupby(group_column, dropna=False).agg(**aggregations).reset_index()
    correlations = df.corr(numeric_only=True)
    return summary, correlations


def load_results(
    df: pd.DataFrame,
    summary: pd.DataFrame,
    correlations: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Write the cleaned data and analysis reports to the output directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "clean_students.csv", index=False)
    summary.to_csv(output_dir / "summary.csv", index=False)
    correlations.to_csv(output_dir / "correlations.csv")


def run_pipeline(raw_file: Path, output_dir: Path) -> None:
    df = pd.read_csv(raw_file)
    df = clean_data(df)
    df = transform_data(df)
    summary, correlations = analyze_data(df)
    load_results(df, summary, correlations, output_dir)


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data",
        type=Path,
        default=project_dir / "student-data.csv",
        help="Path to the input student CSV file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_dir / "data",
        help="Directory where cleaned data and reports are written.",
    )
    args = parser.parse_args()
    run_pipeline(args.data, args.output_dir)
    print(f"Pipeline complete. Results saved to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
