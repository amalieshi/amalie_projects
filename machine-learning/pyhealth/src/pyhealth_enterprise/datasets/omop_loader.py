"""
Loader for OMOP CDM data using PyHealth's OMOP dataset class.
Requires OMOP-formatted data in the configured data path.

PyHealth API:
    from pyhealth.datasets import OMOP
    dataset = OMOP(root=..., tables=[...], code_mapping={...}, dev=True)
    dataset.stat()
    dataset.info()
"""
from typing import Any

import pandas as pd

from pyhealth_enterprise.config import settings
from pyhealth_enterprise.datasets.base import BaseEHRDataset


class OMOPDataset(BaseEHRDataset):
    def __init__(self, dev: bool = True) -> None:
        self.dev = dev
        self.dataset: Any = None  # pyhealth.datasets.OMOP

    def load(self) -> None:
        from pyhealth.datasets import OMOP  # type: ignore[import]

        self.dataset = OMOP(
            root=str(settings.OMOP_DATA_PATH),
            tables=[
                "condition_occurrence",
                "drug_exposure",
                "measurement",
                "procedure_occurrence",
            ],
            code_mapping={
                "condition_occurrence": "ICD10CM",
                "drug_exposure": "ATC",
            },
            dev=self.dev,
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
