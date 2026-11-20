# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Validation checks that fail explicitly for critical data problems."""

import pandas as pd

REQUIRED_COLUMNS = {"collision_severity", "date", "time", "road_type", "speed_limit"}
VALID_SEVERITIES = {1, 2, 3}
VALID_SPEED_LIMITS = {20, 30, 40, 50, 60, 70}


def identify_numeric_outliers(data: pd.DataFrame) -> dict[str, int]:
    """Count IQR outliers without removing valid unusual collisions."""
    outliers = {}
    for column in ("number_of_vehicles", "number_of_casualties"):
        if column not in data:
            continue
        values = pd.to_numeric(data[column], errors="coerce").dropna()
        if values.empty:
            outliers[column] = 0
            continue
        first_quartile, third_quartile = values.quantile([0.25, 0.75])
        iqr = third_quartile - first_quartile
        outliers[column] = int(((values < first_quartile - 1.5 * iqr) |
                                (values > third_quartile + 1.5 * iqr)).sum())
    return outliers


def validate_required_columns(data: pd.DataFrame) -> list[str]:
    """Return messages for missing required columns."""
    missing = sorted(REQUIRED_COLUMNS - set(data.columns))
    return [f"Missing required columns: {', '.join(missing)}"] if missing else []


def validate_values(data: pd.DataFrame) -> list[str]:
    """Check target, dates, and core numeric ranges."""
    errors = validate_required_columns(data)
    if errors:
        return errors
    if data["collision_severity"].isna().any():
        errors.append("collision_severity contains missing values.")
    severity = pd.to_numeric(data["collision_severity"], errors="coerce")
    if not set(severity.dropna()).issubset(VALID_SEVERITIES):
        errors.append("collision_severity contains values outside 1, 2, and 3.")
    if data["date"].isna().any():
        errors.append("date contains invalid values.")
    if data["time"].isna().any():
        errors.append("time contains invalid values.")
    speed_limit = pd.to_numeric(data["speed_limit"], errors="coerce")
    if not set(speed_limit.dropna()).issubset(VALID_SPEED_LIMITS):
        errors.append("speed_limit contains values outside 20, 30, 40, 50, 60, and 70.")
    day_of_week = pd.to_numeric(data.get("day_of_week", pd.Series(dtype=float)), errors="coerce")
    if not set(day_of_week.dropna()).issubset(set(range(1, 8))):
        errors.append("day_of_week contains values outside 1 through 7.")
    for column in ("number_of_vehicles", "number_of_casualties"):
        if column in data and (pd.to_numeric(data[column], errors="coerce") < 1).any():
            errors.append(f"{column} contains values below 1.")
    if "latitude" in data:
        latitude = pd.to_numeric(data["latitude"], errors="coerce")
        if ((latitude.notna()) & ~latitude.between(49, 61)).any():
            errors.append("latitude contains values outside the expected Great Britain range.")
    if "longitude" in data:
        longitude = pd.to_numeric(data["longitude"], errors="coerce")
        if ((longitude.notna()) & ~longitude.between(-9, 3)).any():
            errors.append("longitude contains values outside the expected Great Britain range.")
    if data.duplicated().any():
        errors.append("Duplicate records remain after cleaning.")
    return errors


def validate_or_raise(data: pd.DataFrame) -> None:
    """Stop the pipeline when critical validation checks fail."""
    errors = validate_values(data)
    if errors:
        raise ValueError("Validation failed:\n- " + "\n- ".join(errors))

