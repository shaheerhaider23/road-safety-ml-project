# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

import pandas as pd
import pytest
from src.validation import identify_numeric_outliers, validate_values, validate_or_raise


def valid_data():
    return pd.DataFrame({
        "collision_severity": [1, 2, 3],
        "date": pd.to_datetime(["2023-01-01"] * 3),
        "time": pd.to_datetime(["12:00:00"] * 3, format="%H:%M:%S"),
        "road_type": ["1", "6", "6"],
        "speed_limit": [30, 40, 60],
    })


def test_valid_data_has_no_errors():
    assert validate_values(valid_data()) == []


def test_missing_required_column_is_reported():
    data = valid_data().drop(columns=["road_type"])
    assert "Missing required columns" in validate_values(data)[0]


def test_invalid_target_stops_pipeline():
    data = valid_data()
    data.loc[0, "collision_severity"] = 9
    with pytest.raises(ValueError, match="outside 1, 2, and 3"):
        validate_or_raise(data)


def test_duplicate_records_are_reported():
    data = pd.concat([valid_data(), valid_data().iloc[[0]]], ignore_index=True)
    assert any("Duplicate" in message for message in validate_values(data))


def test_invalid_speed_limit_is_reported():
    data = valid_data()
    data.loc[0, "speed_limit"] = 25
    assert any("speed_limit" in message for message in validate_values(data))


def test_outlier_counts_are_reported_without_rejecting_data():
    data = pd.concat([valid_data()] * 3, ignore_index=True)
    data["number_of_vehicles"] = [1, 1, 1, 1, 1, 1, 1, 1, 20]
    data["number_of_casualties"] = [1] * 9
    assert identify_numeric_outliers(data)["number_of_vehicles"] == 1
