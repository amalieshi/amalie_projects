"""
Abstract base class for all dataset loaders.
Provides a consistent interface regardless of source (MIMIC, OMOP, synthetic).
"""
from abc import ABC, abstractmethod

import pandas as pd


class BaseEHRDataset(ABC):
    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def get_patient_count(self) -> int: ...

    @abstractmethod
    def get_visit_count(self) -> int: ...

    @abstractmethod
    def summary(self) -> pd.DataFrame: ...
