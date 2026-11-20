# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Reusable cleaning functions for the DfT collision table."""

from pathlib import Path
import pandas as pd

TARGET = "collision_severity"
OUTCOME_COLUMNS = [
    "enhanced_severity_collision",
    "collision_injury_based",
    "collision_adjusted_severity_serious",
    "collision_adjusted_severity_slight",
]


def load_raw_data(path: Path) -> pd.DataFrame:
    """Load a collision CSV and raise a clear error when it is unavailable."""
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset was not found: {path}")
    return pd.read_csv(path, low_memory=False)


def correct_data_types(data: pd.DataFrame) -> pd.DataFrame:
    """Convert dates, times, numeric fields, and the target to useful types."""
    result = data.copy()
    result["date"] = pd.to_datetime(result["date"], format="%d/%m/%Y", errors="coerce")
    result["time"] = pd.to_datetime(result["time"], format="%H:%M", errors="coerce").dt.time
    for column in result.columns:
        if column not in {"date", "time", "collision_index", "collision_ref_no",
                          "local_authority_ons_district", "local_authority_highway",
                          "local_authority_highway_current", "lsoa_of_accident_location"}:
            result[column] = pd.to_numeric(result[column], errors="coerce")
    return result


def standardize_categorical_values(data: pd.DataFrame) -> pd.DataFrame:
    """Represent coded categorical columns as strings for safe one-hot encoding."""
    result = data.copy()
    categorical = [
        "day_of_week", "road_type", "first_road_class", "junction_detail",
        "junction_control", "light_conditions", "weather_conditions",
        "road_surface_conditions", "urban_or_rural_area", "trunk_road_flag",
    ]
    for column in categorical:
        if column in result:
            result[column] = result[column].astype("string")
    return result


def add_temporal_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add month, hour, and weekend indicators without using target information."""
    result = data.copy()
    result["month"] = result["date"].dt.month
    result["hour"] = pd.to_datetime(result["time"].astype("string"), format="%H:%M:%S",
                                    errors="coerce").dt.hour
    result["is_weekend"] = result["date"].dt.dayofweek.ge(5).astype("Int64")
    return result


def handle_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """Keep valid records and leave imputation to the model pipeline."""
    result = data.copy()
    if TARGET not in result or result[TARGET].isna().any():
        result = result.dropna(subset=[TARGET])
    return result


def remove_exact_duplicates(data: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Remove exact duplicate rows and return the number removed."""
    before = len(data)
    result = data.drop_duplicates().reset_index(drop=True)
    return result, before - len(result)


def clean_data(data: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply documented cleaning steps and return data plus quality metrics."""
    result = correct_data_types(data)
    result = standardize_categorical_values(result)
    result = add_temporal_features(result)
    result = handle_missing_values(result)
    result, duplicates_removed = remove_exact_duplicates(result)
    result = result.drop(columns=[c for c in OUTCOME_COLUMNS if c in result], errors="ignore")
    result["date"] = result["date"].dt.strftime("%Y-%m-%d")
    result["time"] = result["time"].astype("string")
    metrics = {
        "rows_before": len(data),
        "rows_after": len(result),
        "columns_after": len(result.columns),
        "duplicates_removed": duplicates_removed,
        "target_missing_after": int(result[TARGET].isna().sum()),
        "missing_values_after": int(result.isna().sum().sum()),
    }
    return result, metrics

