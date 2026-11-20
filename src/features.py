# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

"""Create simple time-based features for collision records."""

import pandas as pd


def add_temporal_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add month, hour, and weekend indicators without using the target."""
    result = data.copy()
    result["month"] = result["date"].dt.month
    result["hour"] = pd.to_datetime(
        result["time"].astype("string"),
        format="%H:%M:%S",
        errors="coerce",
    ).dt.hour
    result["is_weekend"] = result["date"].dt.dayofweek.ge(5).astype("Int64")
    return result
