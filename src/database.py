# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

"""Load cleaned data into SQLite and run a genuine GROUP BY query."""

import argparse
from pathlib import Path
import sqlite3
import pandas as pd

from .paths import CLEAN_FILE, REPORTS, ROOT


SQL_FILE = ROOT / "sql" / "analysis.sql"
DB_FILE = ROOT / "outputs" / "road_safety.sqlite"


def run_database(path=CLEAN_FILE, reports_output=REPORTS, database_output=None) -> None:
    """Create the database and save collision counts by road type and severity."""
    data = pd.read_csv(path)
    data["severity_label"] = data["collision_severity"].map({1: "Fatal", 2: "Serious", 3: "Slight"})
    if database_output is None:
        database_output = DB_FILE
    database_output.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_output) as connection:
        data.to_sql("collisions", connection, if_exists="replace", index=False)
        query = """
        SELECT road_type, severity_label, COUNT(*) AS collision_count
        FROM collisions
        GROUP BY road_type, severity_label
        ORDER BY road_type, collision_count DESC;
        """
        result = pd.read_sql_query(query, connection)
    SQL_FILE.parent.mkdir(parents=True, exist_ok=True)
    SQL_FILE.write_text(query.strip() + "\n")
    reports_output.mkdir(parents=True, exist_ok=True)
    result.to_csv(reports_output / "sql_road_type_severity.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Store cleaned collisions in SQLite.")
    parser.add_argument("--input", type=Path, default=CLEAN_FILE)
    parser.add_argument("--reports-output", type=Path, default=REPORTS)
    parser.add_argument("--database-output", type=Path, default=DB_FILE)
    arguments = parser.parse_args()
    run_database(arguments.input, arguments.reports_output, arguments.database_output)

