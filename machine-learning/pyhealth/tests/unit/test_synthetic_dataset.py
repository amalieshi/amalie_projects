import pandas as pd
import pytest


@pytest.mark.integration
def test_synthetic_dataset_loads(synthetic_dataset):
    assert synthetic_dataset.dataset is not None


@pytest.mark.integration
def test_synthetic_dataset_has_patients(synthetic_dataset):
    assert synthetic_dataset.get_patient_count() >= 100


@pytest.mark.integration
def test_synthetic_dataset_has_visits(synthetic_dataset):
    assert synthetic_dataset.get_visit_count() >= 100


@pytest.mark.integration
def test_summary_returns_dataframe(synthetic_dataset):
    result = synthetic_dataset.summary()
    assert isinstance(result, pd.DataFrame)
    assert "metric" in result.columns
    assert "count" in result.columns
