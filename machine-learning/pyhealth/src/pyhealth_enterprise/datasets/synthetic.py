"""
Loader for the local synthetic demo dataset (data/samples/).
Uses PyHealth's SampleDataset so all downstream task functions work identically
to MIMIC/OMOP loaders.

PyHealth API:
    from pyhealth.datasets import SampleDataset
    dataset = SampleDataset(root=..., tables=[...], code_mapping={...})
    dataset.stat()
    dataset.info()
"""
from pathlib import Path
from typing import Any

import pandas as pd

from pyhealth_enterprise.config import settings
from pyhealth_enterprise.datasets.base import BaseEHRDataset


class SyntheticEHRDataset(BaseEHRDataset):
    """Wraps pyhealth.datasets.SampleDataset over the local synthetic CSVs."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or settings.SYNTHETIC_DATA_PATH
        self.dataset: Any = None  # pyhealth.datasets.SampleDataset

    def load(self) -> None:
        from pyhealth.datasets import SampleDataset  # type: ignore[import]

        self.dataset = SampleDataset(
            root=str(self.root),
            tables=["patients", "visits", "diagnoses", "medications", "labs"],
            code_mapping={"diagnoses": "ICD9CM", "medications": "ATC"},
        )

    def _assert_loaded(self) -> None:
        if self.dataset is None:
            raise RuntimeError("Call .load() before accessing dataset properties.")

    def get_patient_count(self) -> int:
        self._assert_loaded()
        return len(self.dataset.patients)

    def get_visit_count(self) -> int:
        self._assert_loaded()
        return sum(len(p.visits) for p in self.dataset.patients.values())

    def summary(self) -> pd.DataFrame:
        self._assert_loaded()
        return pd.DataFrame(
            {
                "metric": ["patients", "visits"],
                "count": [self.get_patient_count(), self.get_visit_count()],
            }
        )

    def stat(self) -> None:
        self._assert_loaded()
        self.dataset.stat()

    def info(self) -> None:
        self._assert_loaded()
        self.dataset.info()
