# PyHealth API Quick Reference

## The 4-Step Pipeline

```python
# 1. Dataset
from pyhealth.datasets import MIMIC3, OMOP, SampleDataset
dataset = MIMIC3(root=..., tables=[...], code_mapping={...}, dev=True)
dataset.stat()   # print statistics
dataset.info()   # print schema

# 2. Task
from pyhealth.tasks import (
    readmission_prediction_mimic3_fn,
    mortality_prediction_mimic3_fn,
    length_of_stay_prediction_mimic3_fn,
    drug_recommendation_mimic3_fn,
)
task_dataset = dataset.set_task(readmission_prediction_mimic3_fn)

# 3. Split + DataLoaders
from pyhealth.datasets import split_by_patient, get_dataloader
train, val, test = split_by_patient(task_dataset, [0.8, 0.1, 0.1])
train_loader = get_dataloader(train, batch_size=32, shuffle=True)
val_loader   = get_dataloader(val,   batch_size=32, shuffle=False)
test_loader  = get_dataloader(test,  batch_size=32, shuffle=False)

# 4. Model + Trainer
from pyhealth.models import RETAIN, Transformer, SafeDrug, MoleRec, GRASP, GAMENet
from pyhealth.trainer import Trainer

model = RETAIN(
    dataset=task_dataset,
    feature_keys=["conditions", "drugs"],
    label_key="readmission",
    mode="binary",           # "binary" | "multiclass" | "multilabel"
)
trainer = Trainer(model=model, metrics=["pr_auc", "roc_auc", "f1"])
trainer.train(train_dataloader=train_loader, val_dataloader=val_loader,
              epochs=50, monitor="pr_auc")
result = trainer.evaluate(test_loader)
# result = {"pr_auc": 0.xx, "roc_auc": 0.xx, "f1": 0.xx}
```

## Datasets

| Class | Source | Required tables |
|---|---|---|
| `MIMIC3` | MIMIC-III (PhysioNet) | DIAGNOSES_ICD, PRESCRIPTIONS, ADMISSIONS, ... |
| `MIMIC4` | MIMIC-IV (PhysioNet) | diagnoses_icd, prescriptions, admissions, ... |
| `OMOP` | OMOP CDM | condition_occurrence, drug_exposure, measurement, ... |
| `eICU` | eICU CRD (PhysioNet) | patient, diagnosis, medication, ... |
| `SampleDataset` | Custom CSVs | patients, visits, + custom tables |

## Task Functions

| Function | Task | Mode |
|---|---|---|
| `readmission_prediction_mimic3_fn` | 30-day readmission | binary |
| `mortality_prediction_mimic3_fn` | In-hospital mortality | binary |
| `length_of_stay_prediction_mimic3_fn` | LOS > 3 days | binary |
| `drug_recommendation_mimic3_fn` | Medication set | multilabel |

## Models

| Model | Best for | Notes |
|---|---|---|
| `RETAIN` | Readmission, mortality | Interpretable (attention weights) |
| `Transformer` | Any task | Strong general baseline |
| `GRASP` | Readmission | Graph-based |
| `SafeDrug` | Drug rec | DDI-constrained; needs `ddi_adj` |
| `MoleRec` | Drug rec | Molecular structure-aware |
| `GAMENet` | Drug rec | Graph augmented memory |

## Metrics

```python
from pyhealth.metrics import (
    binary_metrics_fn,      # readmission, mortality, LOS
    multilabel_metrics_fn,  # drug recommendation
    ddi_rate_score,         # drug safety
)

# Binary
result = binary_metrics_fn(y_true, y_prob,
    metrics=["pr_auc", "roc_auc", "f1", "accuracy", "balanced_accuracy"])

# Multilabel
result = multilabel_metrics_fn(y_true, y_prob,
    metrics=["jaccard", "prauc", "f1"])

# DDI rate (lower = safer)
ddi = ddi_rate_score(y_prob, ddi_adj)
```

## Code Mapping (pyhealth.medcode)

```python
from pyhealth.medcode import CrossMap, ATC

# Map between vocabularies
icd9_to_icd10 = CrossMap("ICD9CM", "ICD10CM")
codes = icd9_to_icd10.map("428.0")   # returns list of ICD10 codes

ndc_to_atc = CrossMap("NDC", "ATC")
atc_codes = ndc_to_atc.map("0069-0105-68")

# ATC lookup
drug = ATC("A02BC01")
print(drug.name)    # "omeprazole"
print(drug.level)   # ATC level (1-5)

# Available CrossMap vocabularies:
# ICD9CM, ICD10CM, ICD10PROC, SNOMED, NDC, RXCUI, ATC, CCSCM, CCSPROC
```

## dev=True Pattern

All dataset classes accept `dev=True` to load only the first 1000 patients:

```python
dataset = MIMIC3(root=..., tables=[...], dev=True)   # fast, for learning
dataset = MIMIC3(root=..., tables=[...], dev=False)  # full dataset, for production
```

Always start with `dev=True` when exploring a new task or model.
