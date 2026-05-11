"""
Shared fixtures. Uses synthetic data only — no PhysioNet credentials required.
Run `python data/samples/generate_synthetic_data.py` before running tests.
"""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def sample_data_path() -> Path:
    return Path(__file__).parent.parent / "data" / "samples"


@pytest.fixture(scope="session")
def synthetic_dataset(sample_data_path: Path):
    from pyhealth_enterprise.datasets.synthetic import SyntheticEHRDataset

    ds = SyntheticEHRDataset(root=sample_data_path)
    ds.load()
    return ds
