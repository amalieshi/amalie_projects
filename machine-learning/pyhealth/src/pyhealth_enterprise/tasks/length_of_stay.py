"""
Length-of-stay prediction task setup.

PyHealth API:
    from pyhealth.tasks import length_of_stay_prediction_mimic3_fn
"""
from typing import Any, Tuple

from torch.utils.data import DataLoader


def setup_los_task(
    dataset: Any,
    batch_size: int = 32,
    split: tuple[float, float, float] = (0.8, 0.1, 0.1),
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    from pyhealth.datasets import get_dataloader, split_by_patient  # type: ignore[import]
    from pyhealth.tasks import length_of_stay_prediction_mimic3_fn  # type: ignore[import]

    task_dataset = dataset.set_task(length_of_stay_prediction_mimic3_fn)
    train, val, test = split_by_patient(task_dataset, list(split))
    return (
        get_dataloader(train, batch_size=batch_size, shuffle=True),
        get_dataloader(val, batch_size=batch_size, shuffle=False),
        get_dataloader(test, batch_size=batch_size, shuffle=False),
    )
