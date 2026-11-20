# Explain me

## New files

- `src/features.py`: contains `add_temporal_features`, which adds month, hour,
  and weekend columns. It is separate so temporal feature code is easy to test.
- `src/demo_quality_gate.py`: deliberately corrupts temporary data and compares
  quality-gate FAIL with real-data PASS. It never changes the raw file.
- `src/create_sample.py`: creates a seeded 2,000-row sample from the raw CSV.
- `tests/test_train.py`: tests the grid setup and macro PR-AUC helper.
- `tests/test_sample_and_demo.py`: tests sample creation and the quality demo.
- `docs/two_input_test.md`: records the real-input and sample-input Part A runs.

## Changed functions

- `make_preprocessor`: builds numeric and categorical preprocessing for one
  pipeline, so preprocessing is fitted only on training data.
- `make_logistic_grid`: tries three small C values for Logistic Regression with
  training-fold CV, keeping the search practical.
- `macro_pr_auc`: converts held-out labels to one-vs-rest targets and returns
  macro PR-AUC.
- `run_training`: compares four models, chooses the highest CV macro-F1, adds
  test scores, saves permutation importance, and records the grid result.
- `validation_results`: evaluates each quality rule separately and calculates a
  pass rate.
- `quality_gate`: raises a clear error if the pass rate is below 95%.
- `load_raw_data`: fails clearly when a raw file is missing.
- `standardize_categorical_values`: converts coded categories to strings.
- `add_temporal_features`: creates month, hour, and weekend values.
- `handle_missing_values`: removes missing target rows, if present.
- `clean_data`: now also calculates missing-value percentages before and after.
- `inspect/run`: accepts an input and output folder and writes both metrics file
  names.
- `run_analysis`, `run_visualizations`, and `run_database`: accept optional
  input and separate output locations for the sample run.
- `run_evaluation`: saves the confusion matrix, classification report, and
  concrete error analysis.
