# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "dft-road-casualty-statistics-collision-2023.csv"
CLEAN_FILE = ROOT / "data" / "cleaned" / "collision-2023-cleaned.csv"
REPORTS = ROOT / "outputs" / "reports"
FIGURES = ROOT / "outputs" / "figures"
MODEL_FILE = ROOT / "models" / "collision-severity-pipeline.joblib"

