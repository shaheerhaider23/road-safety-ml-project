# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Command-line inference using the saved preprocessing-and-model pipeline."""

import argparse
from pathlib import Path
import joblib
import pandas as pd

from .paths import MODEL_FILE
from .train import DROP_COLUMNS


def predict(input_path: Path, output_path: Path) -> None:
    """Validate an unseen CSV, predict severity, and save a new CSV."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV was not found: {input_path}")
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Trained model was not found: {MODEL_FILE}")
    data = pd.read_csv(input_path)
    if "collision_severity" in data.columns:
        raise ValueError("Input for prediction must not contain collision_severity.")
    pipeline = joblib.load(MODEL_FILE)
    if not hasattr(pipeline, "feature_names_in_"):
        raise ValueError("Saved model does not expose its required input columns.")
    required_columns = set(pipeline.feature_names_in_) - DROP_COLUMNS
    missing_columns = sorted(required_columns - set(data.columns))
    if missing_columns:
        raise ValueError("Input CSV is missing required columns: " + ", ".join(missing_columns))
    output = data.copy()
    output["predicted_collision_severity"] = pipeline.predict(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)


def main() -> None:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Predict collision severity.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    predict(args.input, args.output)


if __name__ == "__main__":
    main()
