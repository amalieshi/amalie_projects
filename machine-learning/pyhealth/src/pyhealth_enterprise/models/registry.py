"""
Model registry — factory for PyHealth models.
Decouples notebook/pipeline code from direct model imports so
swapping models requires changing only the ModelName enum value.

PyHealth models:
    RETAIN      — Reverse Time Attention (Choi et al. 2016); interpretable via attention
    Transformer — Standard transformer encoder; strong baseline
    GRASP       — Graph-based readmission prediction
    SafeDrug    — Drug recommendation with DDI constraint
    MoleRec     — Molecular-aware drug recommendation
    GAMENet     — Graph Augmented Memory for drug recommendation
"""
from enum import Enum
from typing import Any


class ModelName(str, Enum):
    RETAIN = "retain"
    TRANSFORMER = "transformer"
    SAFEDRUG = "safedrug"
    MOLEREC = "molerec"
    GRASP = "grasp"
    GAMENET = "gamenet"


def get_model(
    name: ModelName,
    dataset: Any,
    feature_keys: list[str],
    label_key: str,
    mode: str = "binary",
    **kwargs: Any,
) -> Any:
    """Instantiate a PyHealth model by name.

    Args:
        name: ModelName enum value
        dataset: PyHealth task dataset (output of dataset.set_task())
        feature_keys: input feature names (e.g. ["conditions", "drugs"])
        label_key: target label key (e.g. "readmission", "drugs")
        mode: "binary", "multiclass", or "multilabel"
        **kwargs: passed directly to the model constructor

    Returns:
        Instantiated PyHealth model
    """
    from pyhealth.models import (  # type: ignore[import]
        RETAIN,
        GAMENet,
        GRASP,
        MoleRec,
        SafeDrug,
        Transformer,
    )

    _MODEL_MAP = {
        ModelName.RETAIN: RETAIN,
        ModelName.TRANSFORMER: Transformer,
        ModelName.SAFEDRUG: SafeDrug,
        ModelName.MOLEREC: MoleRec,
        ModelName.GRASP: GRASP,
        ModelName.GAMENET: GAMENet,
    }

    cls = _MODEL_MAP[name]
    return cls(
        dataset=dataset,
        feature_keys=feature_keys,
        label_key=label_key,
        mode=mode,
        **kwargs,
    )
