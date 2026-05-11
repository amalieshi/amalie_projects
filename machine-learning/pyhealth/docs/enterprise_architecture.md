# Enterprise Architecture

## Layered Design

```
┌─────────────────────────────────────────────────────────────┐
│  Application Layer (notebooks, scripts, FastAPI endpoints)  │
├─────────────────────────────────────────────────────────────┤
│  pyhealth_enterprise (this package)                         │
│  ├── datasets/     — dataset loading + normalization        │
│  ├── tasks/        — task setup (loaders + splits)          │
│  ├── models/       — model registry                         │
│  ├── pipelines/    — BatchRiskScorer, DrugSafetyChecker,    │
│  │                   EHRETL, ReportGenerator                │
│  └── evaluation/   — metrics wrappers                       │
├─────────────────────────────────────────────────────────────┤
│  PyHealth core (pyhealth pip package)                       │
│  ├── pyhealth.datasets  — MIMIC3, MIMIC4, OMOP, eICU        │
│  ├── pyhealth.tasks     — task functions                    │
│  ├── pyhealth.models    — RETAIN, Transformer, SafeDrug...  │
│  ├── pyhealth.trainer   — training loop                     │
│  ├── pyhealth.metrics   — evaluation metrics                │
│  └── pyhealth.medcode   — code mapping (CrossMap, ATC)      │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                 │
│  ├── data/samples/    — synthetic, no credentials           │
│  ├── data/raw/        — MIMIC, OMOP (gitignored)            │
│  └── data/processed/  — ETL outputs (gitignored)            │
└─────────────────────────────────────────────────────────────┘
```

## Pipeline Modules

### BatchRiskScorer
Model-agnostic: accepts any PyHealth model. Wraps `pyhealth.trainer.Trainer`.
- `.train()` — fits the model, returns validation metrics
- `.score_batch()` — batch inference → `pd.DataFrame` with `risk_score`, `risk_label`
- `.export_csv()` — writes results for downstream consumption

**Extension**: to use a new model, pass a different instantiated PyHealth model. No changes to `BatchRiskScorer`.

### DrugSafetyChecker
Standalone: callable at prescription time without a prediction pipeline.
- `.check_interactions()` — pairwise interaction flags for a medication list
- `.flag_high_risk_combinations()` — filters pairs above a DDI threshold
- `.compute_ddi_rate()` — population-level DDI rate (requires `ddi_adj`)

**Extension**: pass `ddi_adj` from a `SafeDrug` task dataset to enable DDI scoring.

### EHRETL
Runs before training. Normalizes codes via `pyhealth.medcode.CrossMap`.
- ICD-9 → ICD-10 via `CrossMap("ICD9CM", "ICD10CM")`
- NDC → ATC via `CrossMap("NDC", "ATC")`
- Writes parquet outputs consumed by dataset loaders

**Extension**: add `_normalize_labs()` or `_normalize_procedures()` methods.

### ReportGenerator
Pure output layer — no PyHealth calls.
- Consumes DataFrames from `BatchRiskScorer` and `DrugSafetyChecker`
- Renders HTML reports via Jinja2 templates
- Exports Excel via openpyxl

**Extension**: add Jinja2 templates to `docs/report_templates/` and add a corresponding method.

## Deployment Patterns

### Batch Scoring (Scheduled)
```python
# Run nightly via scheduled script or Azure/AWS Lambda
from pyhealth_enterprise.pipelines import BatchRiskScorer
# Load trained model from checkpoint, score today's admissions, export CSV
```

### REST API (FastAPI)
```python
from fastapi import FastAPI
from pyhealth_enterprise.pipelines import BatchRiskScorer, DrugSafetyChecker

app = FastAPI()

@app.post("/risk-score")
def score_patient(patient_data: dict) -> dict:
    # preprocess -> score -> return risk label
    ...

@app.post("/drug-safety")
def check_drugs(drug_codes: list[str]) -> dict:
    checker = DrugSafetyChecker()
    return {"interactions": checker.check_interactions(drug_codes).to_dict()}
```

### Model Versioning
Store trained model checkpoints in `data/processed/models/` (gitignored).
PyHealth's `Trainer` supports checkpoint loading:
```python
trainer.load_ckpt("data/processed/models/retain_readmission_v1.ckpt")
```

## Adding a New Clinical Task

1. Create `src/pyhealth_enterprise/tasks/new_task.py` with `setup_new_task()` following the existing pattern
2. Export from `tasks/__init__.py`
3. Add a notebook in `notebooks/03_clinical_tasks/`
4. Add unit tests in `tests/unit/`
