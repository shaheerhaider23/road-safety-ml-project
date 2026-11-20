# Student name: Syed Shaheer Haider
# Roll number: TRN-2026-000343
# Date: 2026-11-20

import pandas as pd
from sklearn.model_selection import GridSearchCV

from src.train import macro_pr_auc, make_logistic_grid, make_preprocessor


def test_make_logistic_grid_is_grid_search():
    """The Logistic Regression setup is a small cross-validation grid."""
    data = pd.DataFrame({
        "collision_severity": [1, 2, 3, 1, 2, 3],
        "road_type": ["1", "2", "3", "1", "2", "3"],
    })
    preprocessor = make_preprocessor(data)
    grid = make_logistic_grid(preprocessor)
    assert isinstance(grid, GridSearchCV)
    assert grid.param_grid == {"model__C": [0.1, 1.0, 10.0]}


def test_macro_pr_auc_returns_a_score():
    """Macro PR-AUC accepts held-out labels and class probabilities."""
    actual = pd.Series([1, 2, 3])
    probabilities = [
        [0.8, 0.1, 0.1],
        [0.1, 0.8, 0.1],
        [0.1, 0.1, 0.8],
    ]
    score = macro_pr_auc(actual, probabilities)
    assert 0.0 <= score <= 1.0
