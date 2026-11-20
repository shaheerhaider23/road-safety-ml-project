# Dataset proposal

The project uses the Department for Transport's 2023 STATS19 collision extract.
It contains 104,258 police-recorded personal-injury collisions in Great Britain
and 44 coded collision-level fields.

The target is `collision_severity`: 1 Fatal, 2 Serious, and 3 Slight. The target
is imbalanced, which motivates stratified splitting and macro-F1 reporting.

