# Dataset proposal

The project uses the Department for Transport's 2023 STATS19 collision extract.
It contains 104,258 police-recorded personal-injury collisions in Great Britain
and 44 coded collision-level fields.

The target is `collision_severity`: 1 Fatal, 2 Serious, and 3 Slight. The target
is imbalanced, which motivates stratified splitting and macro-F1 reporting.

Source: [DfT Road Safety Open Data](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data).
Licence: Open Government Licence v3.0.
Access date: 16 November 2026.

Predicting severity is useful as an educational demonstration for understanding
which collision circumstances are associated with different outcomes. It could
support exploratory safety analysis, but it must not be used for emergency
response or enforcement because the records are police-reported and the data
has important reporting and imbalance limitations.

