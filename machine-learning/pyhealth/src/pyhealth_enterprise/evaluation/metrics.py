"""
Thin wrappers around PyHealth's evaluation utilities.
Returns pd.Series for easy model comparison in notebooks.

PyHealth API:
    from pyhealth.metrics import binary_metrics_fn      # binary classification
    from pyhealth.metrics import multilabel_metrics_fn  # drug recommendation
    from pyhealth.metrics import ddi_rate_score         # DDI safety metric
"""
from typing import Any

import numpy as np
import pandas as pd


def evaluate_binary_classifier(
    y_true: Any,
    y_prob: Any,
    metrics: list[str] | None = None,
) -> pd.Series:
    """Evaluate a binary classifier (readmission, mortality, LOS).

    Args:
        y_true: ground truth labels (0/1)
        y_prob: predicted probabilities
        metrics: metric names; defaults to pr_auc, roc_auc, f1, accuracy

    Returns:
        pd.Series keyed by metric name
    """
    from pyhealth.metrics import binary_metrics_fn  # type: ignore[import]

    if metrics is None:
        metrics = ["pr_auc", "roc_auc", "f1", "accuracy"]

    result = binary_metrics_fn(
        np.array(y_true), np.array(y_prob), metrics=metrics
    )
    return pd.Series(result)


def evaluate_drug_recommendation(
    y_true: Any,
    y_prob: Any,
    ddi_adj: Any | None = None,
    metrics: list[str] | None = None,
) -> pd.Series:
    """Evaluate a drug recommendation model (multilabel).

    Args:
        y_true: ground truth drug sets
        y_prob: predicted drug probabilities
        ddi_adj: DDI adjacency matrix (optional; required for ddi_rate)
        metrics: metric names; defaults to jaccard, prauc, f1

    Returns:
        pd.Series including DDI rate if ddi_adj is provided
    """
    from pyhealth.metrics import multilabel_metrics_fn  # type: ignore[import]

    if metrics is None:
        metrics = ["jaccard", "prauc", "f1"]

    result = multilabel_metrics_fn(
        np.array(y_true), np.array(y_prob), metrics=metrics
    )
    series = pd.Series(result)

    if ddi_adj is not None:
        from pyhealth.metrics import ddi_rate_score  # type: ignore[import]

        series["ddi_rate"] = ddi_rate_score(np.array(y_prob), ddi_adj)

    return series


def compare_models(results: dict[str, pd.Series]) -> pd.DataFrame:
    """Build a comparison DataFrame from multiple model evaluation results.

    Args:
        results: dict mapping model_name -> pd.Series from evaluate_*

    Returns:
        DataFrame with models as rows and metrics as columns
    """
    return pd.DataFrame(results).T
