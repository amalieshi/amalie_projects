# Notebooks

Numbered learning progression. Start with `01_getting_started/` and work through to `06_enterprise_pipelines/`.

| Folder | Topic |
|---|---|
| `01_getting_started/` | Installation, PyHealth overview, the 4-step pipeline |
| `02_datasets/` | Loading synthetic, MIMIC-III, OMOP CDM, and custom CSV data |
| `03_clinical_tasks/` | Readmission, mortality, LOS, and drug recommendation |
| `04_models/` | RETAIN, Transformer, GRASP, SafeDrug deep dives |
| `05_evaluation/` | Metrics, model comparison, DDI safety evaluation |
| `06_enterprise_pipelines/` | Batch scoring, drug safety, ETL, and automated reporting |

## Prerequisites

```powershell
# Install dependencies
pip install -r requirements.txt
pip install -e .

# Generate synthetic data (for notebooks that don't need MIMIC)
python ../data/samples/generate_synthetic_data.py

# Launch Jupyter
jupyter lab
```

## Notes on dev=True

All MIMIC/OMOP notebooks load with `dev=True` (1000 patients) by default.
Remove or set `dev=False` for full-dataset runs.
