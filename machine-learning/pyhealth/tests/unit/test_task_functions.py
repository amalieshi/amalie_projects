import pytest


@pytest.mark.integration
@pytest.mark.slow
def test_readmission_task_returns_three_loaders(synthetic_dataset):
    from pyhealth_enterprise.tasks.readmission import setup_readmission_task

    train, val, test = setup_readmission_task(
        synthetic_dataset.dataset, batch_size=8
    )
    assert train is not None
    assert val is not None
    assert test is not None


@pytest.mark.integration
@pytest.mark.slow
def test_mortality_task_returns_three_loaders(synthetic_dataset):
    from pyhealth_enterprise.tasks.mortality import setup_mortality_task

    train, val, test = setup_mortality_task(
        synthetic_dataset.dataset, batch_size=8
    )
    assert train is not None
