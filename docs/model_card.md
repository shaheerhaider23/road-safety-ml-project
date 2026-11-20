# Model card

## Purpose

Predict the STATS19 `collision_severity` class from collision context for an
educational demonstration of a tabular classification workflow.

## Intended users and use

The intended users are students and instructors evaluating reproducible data and
machine-learning methods. The model may support exploratory analysis and
demonstration only.

## Training data and features

Training uses the supplied 2023 collision-level CSV. The target classes are
Fatal (1), Serious (2), and Slight (3). The baseline uses road, environmental,
location-code, temporal-derived, and vehicle-count features. Identifiers,
outcome-derived adjustment fields, casualty count, and police attendance are
excluded to reduce leakage.

## Evaluation

`outputs/reports/model_comparison.csv` contains accuracy, macro/weighted F1,
macro precision/recall, one-vs-rest ROC-AUC and PR-AUC where available, and
training-fold cross-validation macro-F1. Model choice uses cross-validation
macro-F1 only. The test set is held out and used once for final held-out
reporting.

The top permutation-importance features are saved in
`outputs/reports/permutation_importance.csv`. Longitude, police force, number
of vehicles, light conditions, and location northing have the largest ranking,
which is plausible for road-safety context but does not prove that these
features cause severity; location and coded police-force patterns may reflect
data collection and reporting differences.

## Limitations and risks

The target is strongly imbalanced, the data describes only police-recorded
personal-injury collisions, and coded fields may be difficult to interpret
without the DfT guide. Correlation is not causation. This educational baseline
must not be used for emergency response, enforcement, insurance decisions, or
operational road-safety allocation.
