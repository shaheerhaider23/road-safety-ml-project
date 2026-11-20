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
macro precision/recall, one-vs-rest ROC-AUC where available, and training-fold
cross-validation macro-F1. The test set is stratified and held out until final
evaluation.

## Limitations and risks

The target is strongly imbalanced, the data describes only police-recorded
personal-injury collisions, and coded fields may be difficult to interpret
without the DfT guide. Correlation is not causation. This educational baseline
must not be used for emergency response, enforcement, insurance decisions, or
operational road-safety allocation.
