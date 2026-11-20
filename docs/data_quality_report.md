# Data quality report

These values were calculated from the supplied CSV on 2026-11-16. They are also
written by `python -m src.inspect_data` to
`outputs/reports/data_quality_metrics.json`.

## Before and after summary

| Metric | Before cleaning | After cleaning |
|---|---:|---:|
| Rows | 104,258 | 104,258 |
| Columns | 44 | 43 |
| Total missing values | 48 | 48 |
| Exact duplicate rows | 0 | 0 |
| Missing target values | 0 | 0 |
| Invalid target values | 0 | 0 |
| Invalid speed limits | 0 | 0 |
| Invalid day-of-week values | 0 | 0 |
| Records rejected | 0 | 0 |

The 48 missing values are coordinate values: 12 each in
`location_easting_osgr`, `location_northing_osgr`, `longitude`, and `latitude`.
They are retained because the collision records and target remain usable;
numeric model preprocessing imputes missing predictors.

## Cleaning changes

No duplicates or target-missing records were removed. Four outcome-derived
columns were removed from the modelling-ready file:

- `enhanced_severity_collision`
- `collision_injury_based`
- `collision_adjusted_severity_serious`
- `collision_adjusted_severity_slight`

Three derived columns were added: `month`, `hour`, and `is_weekend`. Therefore,
the cleaned file has 43 columns rather than 44. Target counts were unchanged:
1,522 Fatal, 23,438 Serious, and 79,298 Slight collisions.

## Invalid values and outliers

The following checks found zero invalid records: severity outside 1–3, speed
limits outside 20/30/40/50/60/70 mph, day codes outside 1–7, vehicle or
casualty counts below 1, and coordinates outside the documented broad Great
Britain ranges (latitude 49–61 and longitude -9–3).

IQR outlier counts for vehicle and casualty counts are reported in the generated
inspection JSON. They are flagged for review only; valid unusual collisions are
not deleted solely because they are statistical outliers.

## Validation result

Validation passed. The raw dataset was not overwritten, and the cleaned data
was written separately to `data/cleaned/collision-2023-cleaned.csv`.

