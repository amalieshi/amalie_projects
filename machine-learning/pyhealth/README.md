# PyHealth Learning and Experimentation

A project for learning the PyHealth library and building enterprise-grade health informatics automation tools. PyHealth provides clinical EHR predictive modeling — drug recommendation, readmission prediction, mortality prediction, length-of-stay prediction, and drug-drug interaction checking.

## Project Goals
- Master the PyHealth API through hands-on notebooks
- Build reusable enterprise automation pipelines (batch risk scoring, drug safety checking, EHR ETL, automated reporting)
- Demonstrate the full PyHealth 4-step pipeline: Dataset → Task → Model → Trainer

## Project Structure

```
pyhealth/
├── data/
│   ├── raw/        ← MIMIC-III/IV, eICU, OMOP (requires PhysioNet credentials; gitignored)
│   ├── processed/  ← ETL outputs (gitignored)
│   └── samples/    ← Synthetic demo data, no credentials needed
├── notebooks/
│   ├── 01_getting_started/    ← Installation, PyHealth overview
│   ├── 02_datasets/           ← Synthetic, MIMIC-III, OMOP CDM, custom CSV
│   ├── 03_clinical_tasks/     ← Readmission, mortality, LOS, drug recommendation
│   ├── 04_models/             ← RETAIN, Transformer, GRASP, SafeDrug
│   ├── 05_evaluation/         ← Metrics, model comparison, DDI evaluation
│   └── 06_enterprise_pipelines/ ← Batch scoring, drug safety, ETL, reporting
├── src/
│   └── pyhealth_enterprise/   ← Installable enterprise automation package
├── tests/
│   ├── unit/
│   └── integration/
└── docs/
    ├── data_access_guide.md
    ├── enterprise_architecture.md
    └── pyhealth_api_reference.md
```

## Getting Started

```powershell
# From this directory
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install the enterprise package in editable mode
pip install -e .

# Launch Jupyter
jupyter lab
```

Start with `notebooks/01_getting_started/01_installation_and_setup.ipynb`.

## Data Access

**No credentials needed**: All notebooks in `03_clinical_tasks/` through `06_enterprise_pipelines/` can run using synthetic data in `data/samples/`. Generate it first:

```powershell
python data/samples/generate_synthetic_data.py
```

**MIMIC-III/IV / OMOP**: Requires PhysioNet credentialing. See `docs/data_access_guide.md`. Copy `.env.example` to `.env` and fill in your credentials.

## Enterprise Package

The `src/pyhealth_enterprise/` package wraps PyHealth with production-ready modules:

```python
from pyhealth_enterprise.pipelines import BatchRiskScorer, DrugSafetyChecker
from pyhealth_enterprise.pipelines import EHRETL, ReportGenerator
from pyhealth_enterprise.evaluation.metrics import evaluate_binary_classifier
```

Install once with `pip install -e .`, then import from any notebook or script.

## Running Tests

```powershell
# Unit tests — no credentials needed
pytest tests/unit/ -v

# Integration tests — requires synthetic data generated
pytest tests/integration/ -v -m integration
```

## Author
Amalie Shi — amalie.hui.shi@gmail.com
