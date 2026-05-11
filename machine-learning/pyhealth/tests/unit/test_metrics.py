import numpy as np
import pandas as pd
import pytest


@pytest.mark.integration
def test_binary_metrics_returns_series():
    from pyhealth_enterprise.evaluation.metrics import evaluate_binary_classifier

    y_true = np.array([0, 1, 0, 1, 1])
    y_prob = np.array([0.1, 0.9, 0.2, 0.8, 0.7])
    result = evaluate_binary_classifier(y_true, y_prob)
    assert isinstance(result, pd.Series)
    assert "pr_auc" in result.index
    assert "roc_auc" in result.index


@pytest.mark.integration
def test_binary_metrics_values_in_range():
    from pyhealth_enterprise.evaluation.metrics import evaluate_binary_classifier

    y_true = np.array([0, 1, 0, 1])
    y_prob = np.array([0.2, 0.8, 0.3, 0.7])
    result = evaluate_binary_classifier(y_true, y_prob)
    assert 0.0 <= result["pr_auc"] <= 1.0
    assert 0.0 <= result["roc_auc"] <= 1.0


@pytest.mark.integration
def test_compare_models_returns_dataframe():
    from pyhealth_enterprise.evaluation.metrics import (
        compare_models,
        evaluate_binary_classifier,
    )

    y_true = np.array([0, 1, 0, 1])
    y_prob = np.array([0.2, 0.8, 0.3, 0.7])
    r = evaluate_binary_classifier(y_true, y_prob)
    df = compare_models({"model_a": r, "model_b": r})
    assert isinstance(df, pd.DataFrame)
    assert "model_a" in df.index
    assert "model_b" in df.index
