# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

"""Pandas and NumPy analysis of cleaned collisions."""

import argparse
from pathlib import Path
import numpy as np
import pandas as pd

from .paths import CLEAN_FILE, REPORTS


def run_analysis(path=CLEAN_FILE, reports_output=REPORTS) -> None:
    """Save grouped summaries answering practical road-safety questions."""
    data = pd.read_csv(path)
    data["severity_label"] = data["collision_severity"].map({1: "Fatal", 2: "Serious", 3: "Slight"})
    data["speed_band"] = np.select(
        [data["speed_limit"] <= 30, data["speed_limit"] <= 50],
        ["Low (20-30)", "Medium (40-50)"],
        default="High (60-70)",
    )
    data["casualties_per_vehicle"] = np.divide(
        data["number_of_casualties"], data["number_of_vehicles"],
        out=np.zeros(len(data), dtype=float), where=data["number_of_vehicles"].to_numpy() != 0,
    )
    reports_output.mkdir(parents=True, exist_ok=True)
    data["severity_label"].value_counts().rename_axis("severity").reset_index(name="collisions").to_csv(
        reports_output / "severity_counts.csv", index=False
    )
    data.groupby("day_of_week", as_index=False).agg(collisions=("collision_index", "count")).to_csv(
        reports_output / "collisions_by_day.csv", index=False
    )
    data.groupby(["road_type", "severity_label"], as_index=False).agg(
        collisions=("collision_index", "count")
    ).to_csv(reports_output / "road_type_by_severity.csv", index=False)
    pd.pivot_table(data, index="speed_band", columns="severity_label", values="collision_index",
                   aggfunc="count", fill_value=0).reset_index().to_csv(
        reports_output / "speed_band_by_severity.csv", index=False
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse a cleaned collision CSV.")
    parser.add_argument("--input", type=Path, default=CLEAN_FILE)
    parser.add_argument("--reports-output", type=Path, default=REPORTS)
    arguments = parser.parse_args()
    run_analysis(arguments.input, arguments.reports_output)

