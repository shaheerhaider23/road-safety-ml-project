# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

import pandas as pd
from src.cleaning import (
    clean_data,
    correct_data_types,
    handle_missing_values,
    load_raw_data,
    remove_exact_duplicates,
    standardize_categorical_values,
)
from src.features import add_temporal_features


def sample_data():
    return pd.DataFrame({
        "collision_index": ["a", "a", "b"],
        "collision_ref_no": ["1", "1", "2"],
        "collision_severity": [3, 3, 2],
        "date": ["01/01/2023", "01/01/2023", "02/01/2023"],
        "time": ["12:00", "12:00", "13:00"],
        "road_type": [6, 6, 1],
        "speed_limit": [30, 30, 60],
        "number_of_vehicles": [1, 1, 2],
        "number_of_casualties": [1, 1, 2],
        "day_of_week": [1, 1, 2],
    })


def test_clean_data_removes_duplicates_and_adds_features():
    cleaned, metrics = clean_data(sample_data())
    assert len(cleaned) == 2
    assert metrics["duplicates_removed"] == 1
    assert {"month", "hour", "is_weekend"} <= set(cleaned.columns)


def test_correct_data_types_invalid_date_becomes_missing():
    data = sample_data()
    data.loc[0, "date"] = "not-a-date"
    converted = correct_data_types(data)
    assert pd.isna(converted.loc[0, "date"])


def test_remove_exact_duplicates_handles_empty_data():
    result, removed = remove_exact_duplicates(pd.DataFrame())
    assert result.empty
    assert removed == 0


def test_load_raw_data_missing_file_raises():
    """A missing raw file produces a clear FileNotFoundError."""
    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as directory:
        try:
            load_raw_data(Path(directory) / "missing.csv")
            raise AssertionError("Expected FileNotFoundError")
        except FileNotFoundError:
            pass


def test_standardize_categorical_values_uses_strings():
    """Coded categories become strings for one-hot encoding."""
    result = standardize_categorical_values(sample_data())
    assert str(result["road_type"].dtype) == "string"


def test_add_temporal_features_adds_three_columns():
    """The moved temporal feature function adds month, hour, and weekend."""
    converted = correct_data_types(sample_data())
    result = add_temporal_features(converted)
    assert {"month", "hour", "is_weekend"} <= set(result.columns)


def test_handle_missing_values_drops_missing_target():
    """Missing target rows are removed before model preparation."""
    data = sample_data()
    data.loc[0, "collision_severity"] = None
    result = handle_missing_values(data)
    assert len(result) == 2
