# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Generate three readable PNG figures from analysis data."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .paths import CLEAN_FILE, FIGURES


def run_visualizations(path=CLEAN_FILE) -> None:
    """Save severity, weekday, and speed/severity charts."""
    data = pd.read_csv(path)
    data["severity"] = data["collision_severity"].map({1: "Fatal", 2: "Serious", 3: "Slight"})
    data["weekday"] = data["day_of_week"].map({
        1: "Sunday", 2: "Monday", 3: "Tuesday", 4: "Wednesday",
        5: "Thursday", 6: "Friday", 7: "Saturday",
    })
    FIGURES.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    order = ["Fatal", "Serious", "Slight"]
    sns.countplot(data=data, x="severity", order=order)
    plt.title("Collision severity distribution")
    plt.xlabel("Collision severity")
    plt.ylabel("Number of collisions")
    plt.tight_layout()
    plt.savefig(FIGURES / "severity_distribution.png", dpi=150)
    plt.close()

    weekday_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    counts = data["weekday"].value_counts().reindex(weekday_order)
    counts.plot(kind="bar")
    plt.title("Collisions by day of week")
    plt.xlabel("Day of week")
    plt.ylabel("Number of collisions")
    plt.tight_layout()
    plt.savefig(FIGURES / "collisions_by_day.png", dpi=150)
    plt.close()

    sns.countplot(data=data, x="speed_limit", hue="severity", hue_order=order)
    plt.title("Collision severity by speed limit")
    plt.xlabel("Speed limit (mph)")
    plt.ylabel("Number of collisions")
    plt.legend(title="Severity")
    plt.tight_layout()
    plt.savefig(FIGURES / "severity_by_speed_limit.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    run_visualizations()

