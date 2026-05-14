"""
Drug recommendation task setup.
Multilabel — predicts a set of medications for the current visit.

PyHealth API:
    from pyhealth.tasks import drug_recommendation_mimic3_fn
    # task_dataset.ddi_adj and task_dataset.ddi_mask_H are available after set_task
    # needed by SafeDrug and other DDI-constrained models
"""
from typing import Any, Tuple

from torch.utils.data import DataLoader


def setup_drug_recommendation_task(
    dataset: Any,
    batch_size: int = 32,
    split: tuple[float, float, float] = (0.8, 0.1, 0.1),
) -> Tuple[DataLoader, DataLoader, DataLoader, Any]:
    """Returns (train_loader, val_loader, test_loader, task_dataset).

    task_dataset is also returned because drug models like SafeDrug need
    task_dataset.ddi_adj and task_dataset.ddi_mask_H for DDI constraints.
    """
    from pyhealth.datasets import get_dataloader, split_by_patient  # type: ignore[import]
    from pyhealth.tasks import drug_recommendation_mimic3_fn  # type: ignore[import]

    task_dataset = dataset.set_task(drug_recommendation_mimic3_fn)
    train, val, test = split_by_patient(task_dataset, list(split))
    return (
        get_dataloader(train, batch_size=batch_size, shuffle=True),
        get_dataloader(val, batch_size=batch_size, shuffle=False),
        get_dataloader(test, batch_size=batch_size, shuffle=False),
        task_dataset,
    )
