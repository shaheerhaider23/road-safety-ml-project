# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Load cleaned data into SQLite and run a genuine GROUP BY query."""

import sqlite3
import pandas as pd

from .paths import CLEAN_FILE, REPORTS, ROOT


SQL_FILE = ROOT / "sql" / "analysis.sql"
DB_FILE = ROOT / "outputs" / "road_safety.sqlite"


def run_database(path=CLEAN_FILE) -> None:
    """Create the database and save collision counts by road type and severity."""
    data = pd.read_csv(path)
    data["severity_label"] = data["collision_severity"].map({1: "Fatal", 2: "Serious", 3: "Slight"})
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_FILE) as connection:
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
    REPORTS.mkdir(parents=True, exist_ok=True)
    result.to_csv(REPORTS / "sql_road_type_severity.csv", index=False)


if __name__ == "__main__":
    run_database()

