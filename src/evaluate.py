# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Create a classification report, confusion matrix, and simple error analysis."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

from .paths import REPORTS, FIGURES


def run_evaluation() -> None:
    """Save evaluation artifacts generated from held-out test predictions."""
    predictions = pd.read_csv(REPORTS / "test_predictions.csv")
    labels = [1, 2, 3]
    report = classification_report(
        predictions["actual"], predictions["predicted"], labels=labels,
        target_names=["Fatal", "Serious", "Slight"], output_dict=True, zero_division=0
    )
    (REPORTS / "classification_report.json").write_text(pd.Series(report).to_json(indent=2))
    matrix = confusion_matrix(predictions["actual"], predictions["predicted"], labels=labels)
    FIGURES.mkdir(parents=True, exist_ok=True)
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Fatal", "Serious", "Slight"],
                yticklabels=["Fatal", "Serious", "Slight"])
    plt.title("Confusion matrix for selected model")
    plt.xlabel("Predicted severity")
    plt.ylabel("Actual severity")
    plt.tight_layout()
    plt.savefig(FIGURES / "confusion_matrix.png", dpi=150)
    plt.close()
    predictions["correct"] = predictions["actual"] == predictions["predicted"]
    predictions[predictions["correct"] == False].head(100).to_csv(
        REPORTS / "prediction_errors_sample.csv", index=False
    )
    subgroup_columns = [
        "road_type", "weather_conditions", "light_conditions",
        "road_surface_conditions", "urban_or_rural_area",
    ]
    summaries = []
    for column in subgroup_columns:
        if column not in predictions:
            continue
        summary = predictions.groupby(column, dropna=False).agg(
            records=("correct", "size"),
            errors=("correct", lambda values: int((~values).sum())),
            error_rate=("correct", lambda values: float((~values).mean())),
        ).reset_index()
        summary.insert(0, "subgroup", column)
        summary = summary.rename(columns={column: "value"})
        summaries.append(summary)
    if summaries:
        pd.concat(summaries, ignore_index=True).to_csv(
            REPORTS / "error_analysis_by_subgroup.csv", index=False
        )


if __name__ == "__main__":
    run_evaluation()

