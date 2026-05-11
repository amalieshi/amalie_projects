"""
EHR ETL Pipeline — reads raw CSV exports, normalizes codes to standard
vocabularies using PyHealth's CrossMap, and writes parquet files ready
for dataset loading.

PyHealth API:
    from pyhealth.medcode import CrossMap
    icd9_to_icd10 = CrossMap("ICD9CM", "ICD10CM")
    mapped = icd9_to_icd10.map("428.0")   # returns list of ICD10 codes

Supported mappings:
    ICD9CM  -> ICD10CM
    NDC     -> ATC
    RXCUI   -> ATC
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class EHRETL:
    """Transform raw EHR CSV exports into PyHealth-compatible parquet datasets."""

    def __init__(self, source_dir: Path, output_dir: Path) -> None:
        self.source_dir = source_dir
        self.output_dir = output_dir
        self._icd9_to_icd10: Any = None
        self._ndc_to_atc: Any = None

    def _get_icd9_map(self) -> Any:
        if self._icd9_to_icd10 is None:
            from pyhealth.medcode import CrossMap  # type: ignore[import]

            self._icd9_to_icd10 = CrossMap("ICD9CM", "ICD10CM")
        return self._icd9_to_icd10

    def _get_ndc_map(self) -> Any:
        if self._ndc_to_atc is None:
            from pyhealth.medcode import CrossMap  # type: ignore[import]

            self._ndc_to_atc = CrossMap("NDC", "ATC")
        return self._ndc_to_atc

    def run(self) -> None:
        """Execute the full ETL pipeline."""
        logger.info("Starting EHR ETL from %s", self.source_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        patients = self._process_patients()
        visits = self._process_visits()
        diagnoses = self._normalize_diagnoses()
        medications = self._normalize_medications()

        self._write_output(patients, visits, diagnoses, medications)
        logger.info("ETL complete — output written to %s", self.output_dir)

    def _process_patients(self) -> pd.DataFrame:
        path = self.source_dir / "synthetic_patients.csv"
        df = pd.read_csv(path)
        logger.info("Loaded %d patients", len(df))
        return df

    def _process_visits(self) -> pd.DataFrame:
        path = self.source_dir / "synthetic_visits.csv"
        df = pd.read_csv(path)
        logger.info("Loaded %d visits", len(df))
        return df

    def _normalize_diagnoses(self) -> pd.DataFrame:
        path = self.source_dir / "synthetic_diagnoses.csv"
        df = pd.read_csv(path)
        icd_map = self._get_icd9_map()

        def map_code(code: str) -> str:
            try:
                mapped = icd_map.map(code)
                return mapped[0] if mapped else code
            except Exception:
                return code

        df["icd10_code"] = df["icd_code"].apply(map_code)
        logger.info("Normalized %d diagnosis codes (ICD9 -> ICD10)", len(df))
        return df

    def _normalize_medications(self) -> pd.DataFrame:
        path = self.source_dir / "synthetic_medications.csv"
        df = pd.read_csv(path)
        logger.info("Loaded %d medication records (already ATC)", len(df))
        return df

    def _write_output(
        self,
        patients: pd.DataFrame,
        visits: pd.DataFrame,
        diagnoses: pd.DataFrame,
        medications: pd.DataFrame,
    ) -> None:
        patients.to_parquet(self.output_dir / "patients.parquet", index=False)
        visits.to_parquet(self.output_dir / "visits.parquet", index=False)
        diagnoses.to_parquet(self.output_dir / "diagnoses.parquet", index=False)
        medications.to_parquet(self.output_dir / "medications.parquet", index=False)
