# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-16

"""Train comparable multiclass baseline models with leakage-safe preprocessing."""

import json
import warnings
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .paths import CLEAN_FILE, MODEL_FILE, REPORTS

warnings.filterwarnings("ignore", category=FutureWarning)

TARGET = "collision_severity"
DROP_COLUMNS = {
    TARGET, "collision_index", "collision_ref_no", "date", "time",
    "number_of_casualties", "did_police_officer_attend_scene_of_accident",
    "lsoa_of_accident_location",
}


def make_preprocessor(data: pd.DataFrame) -> ColumnTransformer:
    """Create numeric and categorical preprocessing fitted only inside a pipeline."""
    features = data.drop(columns=list(DROP_COLUMNS & set(data.columns)))
    numeric = features.select_dtypes(include=["number"]).columns.tolist()
    categorical = [c for c in features.columns if c not in numeric]
    return ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), numeric),
        ("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]), categorical),
    ])


def run_training(path=CLEAN_FILE) -> None:
    """Train four models, save metrics, and persist the best fitted pipeline."""
    data = pd.read_csv(path)
    X = data.drop(columns=[TARGET])
    y = data[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    models = {
        "dummy": DummyClassifier(strategy="most_frequent", random_state=42),
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=150, random_state=42, n_jobs=-1, class_weight="balanced_subsample"
        ),
        "extra_trees": ExtraTreesClassifier(
            n_estimators=150, random_state=42, n_jobs=-1, class_weight="balanced"
        ),
    }
    results = []
    fitted = {}
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    for name, model in models.items():
        pipeline = Pipeline([("preprocessor", make_preprocessor(data)), ("model", model)])
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        probabilities = pipeline.predict_proba(X_test) if hasattr(pipeline, "predict_proba") else None
        row = {
            "model": name,
            "accuracy": accuracy_score(y_test, predictions),
            "macro_precision": precision_score(y_test, predictions, average="macro", zero_division=0),
            "macro_recall": recall_score(y_test, predictions, average="macro", zero_division=0),
            "macro_f1": f1_score(y_test, predictions, average="macro", zero_division=0),
            "weighted_f1": f1_score(y_test, predictions, average="weighted", zero_division=0),
            "cv_macro_f1": cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1_macro").mean(),
        }
        if probabilities is not None:
            row["roc_auc_ovr_macro"] = roc_auc_score(y_test, probabilities, multi_class="ovr")
        results.append(row)
        fitted[name] = (pipeline, predictions, y_test)
    metrics = pd.DataFrame(results).sort_values("macro_f1", ascending=False)
    REPORTS.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(REPORTS / "model_comparison.csv", index=False)
    best_name = metrics.iloc[0]["model"]
    best_pipeline, predictions, y_test = fitted[best_name]
    joblib.dump(best_pipeline, MODEL_FILE)
    test_output = X_test.copy()
    test_output["actual"] = y_test
    test_output["predicted"] = predictions
    test_output.to_csv(REPORTS / "test_predictions.csv", index=False)
    (REPORTS / "training_summary.json").write_text(json.dumps({
        "best_model": best_name,
        "test_rows": len(y_test),
        "features_excluded": sorted(DROP_COLUMNS),
    }, indent=2))
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    run_training()

