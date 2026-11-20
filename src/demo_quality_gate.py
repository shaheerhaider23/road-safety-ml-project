# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

"""Show the quality gate passing real data and failing deliberately bad data."""

import tempfile
from pathlib import Path
import pandas as pd

from .paths import RAW_FILE, REPORTS
from .validation import quality_gate


def run_quality_gate_demo() -> str:
    """Create corrupt temporary data, then compare it with the real raw data."""
    real = pd.read_csv(RAW_FILE, low_memory=False)
    lines = []
    with tempfile.TemporaryDirectory() as temporary_directory:
        corrupt = real.head(100).copy()
        corrupt.loc[0, "collision_severity"] = 9
        corrupt.loc[1, "date"] = "not-a-date"
        corrupt.loc[2, "speed_limit"] = 999
        corrupt.to_csv(Path(temporary_directory) / "corrupt.csv", index=False)
        try:
            quality_gate(corrupt)
            lines.append("CORRUPT DATA: PASS")
        except ValueError as error:
            lines.append(f"CORRUPT DATA: FAIL - {error}")
    try:
        quality_gate(real)
        lines.append("REAL DATA: PASS")
    except ValueError as error:
        lines.append(f"REAL DATA: FAIL - {error}")
    output = "\n".join(lines)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "quality_gate_demo.txt").write_text(output)
    print(output)
    return output


if __name__ == "__main__":
    run_quality_gate_demo()
