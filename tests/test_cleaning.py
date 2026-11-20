# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

import pandas as pd
from src.cleaning import clean_data, correct_data_types, remove_exact_duplicates


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
