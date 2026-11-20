# Dataset schema

Source: [DfT Road Safety Open Data](https://www.gov.uk/government/statistical-data-sets/road-safety-open-data).
The table below describes the supplied 2023 collision CSV as actually read.
Values are coded; the DfT data guide is the authority for code meanings.

| Column | Raw type | Description | Missing | Observed values or range |
|---|---|---|---:|---|
| `collision_index` | object | Unique collision identifier | 0 | 104,258 observed identifiers |
| `collision_year` | int64 | Collision year | 0 | 2023 |
| `collision_ref_no` | object | Collision reference number | 0 | 104,258 observed references |
| `location_easting_osgr` | float64 | National Grid easting coordinate | 12 | 70,537–655,160 |
| `location_northing_osgr` | float64 | National Grid northing coordinate | 12 | 10,528–1,152,174 |
| `longitude` | float64 | Geographic longitude | 12 | -7.42934–1.75602 |
| `latitude` | float64 | Geographic latitude | 12 | 49.9145–60.2524 |
| `police_force` | int64 | Reporting police-force code | 0 | 44 observed codes |
| `collision_severity` | int64 | Target: 1 Fatal, 2 Serious, 3 Slight | 0 | 1, 2, 3 |
| `number_of_vehicles` | int64 | Vehicles involved | 0 | 1–17 |
| `number_of_casualties` | int64 | Casualties recorded | 0 | 1–70 |
| `date` | object | Collision date, DD/MM/YYYY | 0 | 365 dates in 2023 |
| `day_of_week` | int64 | DfT day code | 0 | 1–7 |
| `time` | object | Collision time, HH:MM | 0 | 1,440 observed times |
| `local_authority_district` | int64 | Legacy local-authority district code | 0 | -1 only |
| `local_authority_ons_district` | object | ONS local-authority district code | 0 | 351 observed codes |
| `local_authority_highway` | object | Highway-authority code | 0 | 208 observed codes |
| `local_authority_highway_current` | object | Current highway-authority code | 0 | 208 observed codes |
| `first_road_class` | int64 | First road classification code | 0 | 1–6 |
| `first_road_number` | int64 | First road number | 0 | 0–9,176; 3,082 unique values |
| `road_type` | int64 | Road-type code | 0 | 1, 2, 3, 6, 7, 9 |
| `speed_limit` | int64 | Speed limit in mph | 0 | 20, 30, 40, 50, 60, 70 |
| `junction_detail_historic` | int64 | Historic junction-detail code | 0 | -1, 0–9, 99 |
| `junction_detail` | int64 | Current junction-detail code | 0 | -1, 0, 13, 16–19 |
| `junction_control` | int64 | Junction-control code | 0 | -1, 1, 2, 3, 4, 9 |
| `second_road_class` | int64 | Second road classification code | 0 | -1, 0–6 |
| `second_road_number` | int64 | Second road number | 0 | -1–9,999; 2,360 unique values |
| `pedestrian_crossing_human_control_historic` | int64 | Historic human-control crossing code | 0 | -1, 0, 1, 2, 9 |
| `pedestrian_crossing_physical_facilities_historic` | int64 | Historic physical-facilities crossing code | 0 | -1, 0, 1, 4, 5, 7, 8, 9 |
| `pedestrian_crossing` | int64 | Current pedestrian-crossing code | 0 | -1, 0, 11–17, 99 |
| `light_conditions` | int64 | Lighting-condition code | 0 | 1, 4, 5, 6, 7 |
| `weather_conditions` | int64 | Weather-condition code | 0 | 1–9 |
| `road_surface_conditions` | int64 | Road-surface-condition code | 0 | -1, 1–5, 9 |
| `special_conditions_at_site` | int64 | Special-site-condition code | 0 | -1, 0–7, 9 |
| `carriageway_hazards_historic` | int64 | Historic carriageway-hazard code | 0 | -1, 0–3, 6, 7, 9 |
| `carriageway_hazards` | int64 | Current carriageway-hazard code | 0 | -1, 0, 11, 13–21, 99 |
| `urban_or_rural_area` | int64 | Urban/rural classification code | 0 | -1, 1, 2, 3 |
| `did_police_officer_attend_scene_of_accident` | int64 | Officer-attendance code | 0 | 1, 2, 3 |
| `trunk_road_flag` | int64 | Trunk-road indicator | 0 | -1, 1, 2 |
| `lsoa_of_accident_location` | object | LSOA location code | 0 | 26,838 observed codes |
| `enhanced_severity_collision` | int64 | DfT enhanced-severity field | 0 | -1, 1, 3, 5, 6, 7; excluded from modelling |
| `collision_injury_based` | int64 | Injury-based reporting indicator | 0 | 0, 1; excluded from modelling |
| `collision_adjusted_severity_serious` | float64 | Adjusted serious-severity value | 0 | 0–1; excluded from modelling |
| `collision_adjusted_severity_slight` | float64 | Adjusted slight-severity value | 0 | 0–1; excluded from modelling |

The four coordinate fields each contain 12 missing values. The dataset has no
missing target values and no exact duplicate rows. Values such as `-1`, `9`,
and `99` are retained as coded DfT values rather than guessed or silently
converted to missing values. Dates and times are parsed by the cleaning
pipeline. The four outcome-derived severity fields are removed from the
modelling-ready file to avoid target leakage.
