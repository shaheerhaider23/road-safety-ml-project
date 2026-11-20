# Assumptions and cleaning decisions

- The raw CSV is read-only and copied into `data/raw/`; cleaning writes a
  separate file.
- Valid unusual collisions are retained; only exact duplicates and records
  without a target are removed.
- Missing predictors are imputed inside the model pipeline rather than deleting
  otherwise valid rows.
- Severity adjustment and injury-based fields are excluded because they are
  derived from outcome information.
- Identifiers and fields likely unavailable before or at the collision are
  excluded from the baseline model.
- Speed limits are validated against the observed DfT set of 20, 30, 40, 50,
  60, and 70 mph; day codes must be 1 through 7; vehicle and casualty counts
  must be at least 1.
- Latitude and longitude are checked against broad Great Britain bounds
  (49–61 and -9–3) to catch malformed coordinates, while missing coordinates
  are retained for model imputation.
- IQR outliers in vehicle and casualty counts are reported for review but are
  not deleted because unusual collisions can be valid records.

## Short model card summary

The selected educational model predicts Fatal, Serious, or Slight from collision
context. It uses a held-out test set, cross-validation on training data only,
and macro-F1 to compare balanced performance. The full model card is
[model_card.md](./model_card.md).

## Model risks

The model may repeat location, reporting, and data collection patterns rather
than learn a true cause. It has low precision for the rare Fatal class and
must not be used for emergency response, enforcement, insurance, or resource
allocation decisions.

