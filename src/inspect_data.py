# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Inspect, clean, validate, and save the collision dataset."""

import json
from pathlib import Path
import pandas as pd

from .cleaning import clean_data, load_raw_data
from .paths import CLEAN_FILE, RAW_FILE, REPORTS
from .validation import identify_numeric_outliers, validate_or_raise


def inspect(path: Path = RAW_FILE) -> dict:
    """Create a reproducible inspection report from the raw CSV."""
    data = load_raw_data(path)
    missing = data.isna().sum()
    numeric = data.select_dtypes(include="number")
    categorical = {}
    for column in data.columns:
        if data[column].nunique(dropna=True) <= 20:
            categorical[column] = {
                "unique_values": sorted(str(value) for value in data[column].dropna().unique()),
                "counts": {str(key): int(value) for key, value in data[column].value_counts().items()},
            }
    report = {
        "source_file": str(path),
        "rows": len(data),
        "columns": len(data.columns),
        "column_names": list(data.columns),
        "dtypes": {c: str(t) for c, t in data.dtypes.items()},
        "missing_values": {c: int(n) for c, n in missing.items() if n},
        "duplicate_rows": int(data.duplicated().sum()),
        "target_counts": {str(k): int(v) for k, v in data["collision_severity"].value_counts().items()},
        "numeric_descriptive_statistics": json.loads(numeric.describe().to_json()),
        "categorical_unique_values": categorical,
        "numeric_outlier_counts": identify_numeric_outliers(data),
        "first_five": data.head().fillna("").to_dict(orient="records"),
        "last_five": data.tail().fillna("").to_dict(orient="records"),
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "inspection_report.json").write_text(json.dumps(report, indent=2, default=str))
    numeric.describe().to_csv(REPORTS / "numeric_descriptive_statistics.csv")
    return report


def run() -> None:
    """Run inspection, cleaning, and validation from the repository root."""
    report = inspect()
    raw = load_raw_data(RAW_FILE)
    cleaned, metrics = clean_data(raw)
    cleaned_for_validation = cleaned.copy()
    cleaned_for_validation["date"] = pd.to_datetime(cleaned_for_validation["date"], errors="coerce")
    cleaned_for_validation["time"] = pd.to_datetime(
        cleaned_for_validation["time"].astype("string"), format="%H:%M:%S", errors="coerce"
    )
    validate_or_raise(cleaned_for_validation)
    CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEAN_FILE, index=False)
    metrics.update({"validation": "passed", "target_counts": report["target_counts"]})
    (REPORTS / "data_quality_metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    run()

