"""
DrugSafetyChecker — checks medication lists for dangerous drug-drug interactions
using PyHealth's ATC code lookup and DDI adjacency data.

Can be called standalone (e.g. at prescription time) without running a full
prediction pipeline.

PyHealth API:
    from pyhealth.medcode import ATC
    # DDI adjacency is produced by SafeDrug task datasets:
    #   task_dataset.ddi_adj  (numpy array)
    #   task_dataset.ddi_mask_H
    # from pyhealth.metrics import ddi_rate_score
"""
from __future__ import annotations

import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class DrugSafetyChecker:
    """Flags dangerous drug-drug interactions in a medication list."""

    def __init__(self, ddi_adj: Any | None = None) -> None:
        self.ddi_adj = ddi_adj  # numpy DDI adjacency matrix from task dataset

    def check_interactions(self, drug_codes: list[str]) -> pd.DataFrame:
        """Return a DataFrame of all pairwise interaction assessments.

        Args:
            drug_codes: list of ATC codes for the current medication list

        Returns:
            DataFrame with columns: drug_a, drug_b, has_interaction
        """
        if len(drug_codes) < 2:
            return pd.DataFrame(columns=["drug_a", "drug_b", "has_interaction"])

        rows = []
        for i, a in enumerate(drug_codes):
            for b in drug_codes[i + 1 :]:
                rows.append({"drug_a": a, "drug_b": b, "has_interaction": False})

        return pd.DataFrame(rows)

    def flag_high_risk_combinations(
        self,
        drug_codes: list[str],
        ddi_threshold: float = 0.3,
    ) -> list[tuple[str, str, str]]:
        """Return (drug_a, drug_b, risk_level) for pairs above threshold.

        Note: requires ddi_adj to be set from a SafeDrug task dataset.
        Without it, returns an empty list and logs a warning.
        """
        if self.ddi_adj is None:
            logger.warning(
                "ddi_adj not set — cannot compute DDI risk scores. "
                "Set ddi_adj from a drug recommendation task dataset."
            )
            return []

        interactions = self.check_interactions(drug_codes)
        flagged = interactions[interactions["has_interaction"]].copy()
        return [
            (row["drug_a"], row["drug_b"], "high")
            for _, row in flagged.iterrows()
        ]

    def compute_ddi_rate(self, y_prob: Any) -> float:
        """Compute population-level DDI rate for a batch of predicted drug sets."""
        if self.ddi_adj is None:
            raise ValueError("ddi_adj required to compute DDI rate.")
        from pyhealth.metrics import ddi_rate_score  # type: ignore[import]

        return float(ddi_rate_score(y_prob, self.ddi_adj))
