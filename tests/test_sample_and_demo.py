# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

import tempfile
from pathlib import Path
import pandas as pd

from src.create_sample import create_sample
from src.demo_quality_gate import run_quality_gate_demo


def test_create_sample_writes_2000_rows():
    """The sample creator makes a 2,000-row temporary CSV."""
    with tempfile.TemporaryDirectory() as directory:
        input_path = Path(directory) / "input.csv"
        output_path = Path(directory) / "sample.csv"
        pd.DataFrame({"collision_severity": list(range(1, 4)) * 800}).iloc[:2000].to_csv(
            input_path, index=False
        )
        result = create_sample(input_path, output_path)
        assert result == output_path
        assert len(pd.read_csv(output_path)) == 2000


def test_quality_gate_demo_reports_both_results():
    """The demo output includes a corrupt failure and real-data pass."""
    output = run_quality_gate_demo()
    assert "CORRUPT DATA: FAIL" in output
    assert "REAL DATA: PASS" in output
