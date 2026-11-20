# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

"""Create a reproducible random sample of 2,000 raw collision rows."""

from pathlib import Path
import pandas as pd

from .cleaning import load_raw_data
from .paths import RAW_FILE


def create_sample(input_path: Path = RAW_FILE, output_path: Path = None) -> Path:
    """Create 2,000 random rows without changing the raw CSV."""
    if output_path is None:
        output_path = input_path.parents[1] / "sample" / "collision_sample_2000.csv"
    data = load_raw_data(input_path)
    sample = data.sample(n=2000, random_state=42)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(output_path, index=False)
    print(f"Created {len(sample)} rows in {output_path}")
    return output_path


if __name__ == "__main__":
    create_sample()
