"""
BatchRiskScorer — trains a PyHealth model and runs batch inference over
a patient population, returning structured risk scores as a DataFrame.

Designed to be model-agnostic: pass any instantiated PyHealth model.

PyHealth API:
    from pyhealth.trainer import Trainer
    trainer = Trainer(model=model, metrics=["pr_auc","roc_auc","f1"])
    trainer.train(train_dataloader=..., val_dataloader=...,
                  epochs=50, monitor="pr_auc")
    result = trainer.evaluate(test_dataloader)
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class RiskScoreConfig:
    epochs: int = 50
    monitor: str = "pr_auc"
    metrics: list[str] = field(default_factory=lambda: ["pr_auc", "roc_auc", "f1"])
    threshold_high: float = 0.7
    threshold_medium: float = 0.4


class BatchRiskScorer:
    """Wraps a trained PyHealth model for batch inference over a population."""

    def __init__(
        self,
        model: Any,
        model_name: str,
        config: RiskScoreConfig | None = None,
    ) -> None:
        self.model = model
        self.model_name = model_name
        self.config = config or RiskScoreConfig()
        self._trainer: Any = None

    def _get_trainer(self) -> Any:
        if self._trainer is None:
            from pyhealth.trainer import Trainer  # type: ignore[import]

            self._trainer = Trainer(model=self.model, metrics=self.config.metrics)
        return self._trainer

    def train(
        self,
        train_loader: Any,
        val_loader: Any,
        epochs: int | None = None,
        monitor: str | None = None,
    ) -> dict[str, float]:
        """Train the model and return best validation metrics."""
        trainer = self._get_trainer()
        return trainer.train(
            train_dataloader=train_loader,
            val_dataloader=val_loader,
            epochs=epochs or self.config.epochs,
            monitor=monitor or self.config.monitor,
        )

    def score_batch(self, dataloader: Any) -> pd.DataFrame:
        """Run inference and return a DataFrame of risk scores per patient/visit."""
        trainer = self._get_trainer()
        result = trainer.evaluate(dataloader)

        scored_at = datetime.utcnow().isoformat()
        rows = []

        y_prob = result.get("y_prob", [])
        y_true = result.get("y_true", [])
        patient_ids = result.get("patient_id", [None] * len(y_prob))
        visit_ids = result.get("visit_id", [None] * len(y_prob))

        for i, prob in enumerate(y_prob):
            score = float(prob) if not hasattr(prob, "__len__") else float(max(prob))
            rows.append(
                {
                    "patient_id": patient_ids[i] if i < len(patient_ids) else None,
                    "visit_id": visit_ids[i] if i < len(visit_ids) else None,
                    "risk_score": round(score, 4),
                    "risk_label": self._label(score),
                    "true_label": y_true[i] if i < len(y_true) else None,
                    "model_name": self.model_name,
                    "scored_at": scored_at,
                }
            )

        return pd.DataFrame(rows)

    def _label(self, score: float) -> str:
        if score >= self.config.threshold_high:
            return "high"
        if score >= self.config.threshold_medium:
            return "medium"
        return "low"

    def export_csv(self, results: pd.DataFrame, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(output_path, index=False)
        logger.info("Risk scores exported to %s (%d rows)", output_path, len(results))
