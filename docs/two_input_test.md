# Two-input test

This test uses the real raw CSV and a reproducible random sample of 2,000 rows.
The sample was created by `python -m src.create_sample` with
`random_state=42`; it is stored at
`data/sample/collision_sample_2000.csv`.

| Input | Rows before | Rows after | Missing before | Missing after | Pass rate |
|---|---:|---:|---:|---:|---:|
| Real 2023 raw data | 104,258 | 104,258 | 0.001046% | 0.001071% | 100% |
| 2,000-row sample | 2,000 | 2,000 | 0.000000% | 0.000000% | 100% |

Both inputs passed all six quality checks. The sample target counts were
24 Fatal, 460 Serious, and 1,516 Slight collisions.

The sample run used:

```bash
python -m src.inspect_data --input data/sample/collision_sample_2000.csv --clean-output data/cleaned/collision_sample_2000-cleaned.csv --reports-output outputs/sample/reports
python -m src.analysis --input data/cleaned/collision_sample_2000-cleaned.csv --reports-output outputs/sample/reports
python -m src.visualization --input data/cleaned/collision_sample_2000-cleaned.csv --figures-output outputs/sample/figures
python -m src.database --input data/cleaned/collision_sample_2000-cleaned.csv --reports-output outputs/sample/reports --database-output outputs/sample/road_safety.sqlite
```

These commands wrote cleaned data and reports only under `outputs/sample/` and
`data/cleaned/`, so they did not replace the real output files.
