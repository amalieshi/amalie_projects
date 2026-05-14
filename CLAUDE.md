# Claude Code — Project Guide

## Repository Overview
`amalie_projects` is a personal learning monorepo organized by language/domain:
- `machine-learning/` — ML, deep learning, health informatics projects
- `python/` — Web frameworks (Django, FastAPI), automation, utilities
- `csharp/` — C# projects
- `frontend/` — Frontend projects
- `shared/` — Shared resources and templates

## Conventions

### Naming
- Folders: `snake_case` for Python packages, `kebab-case` for standalone apps
- Python packages: snake_case
- Files: snake_case

### Python Projects
- Dependency management: `requirements.txt` (pip) + `pyproject.toml` for installable packages
- Environment: `venv` per project (never commit `venv/`)
- Installable packages use `src/` layout (`tool.setuptools.package-dir = {"" = "src"}`)
- Code style: Black (line-length 88), mypy strict, pytest
- Author: Amalie Shi / amalie.hui.shi@gmail.com

### ML Projects Standard Structure
```
project_name/
├── data/         # raw/, processed/, samples/ (never commit PHI or large files)
├── notebooks/    # Jupyter notebooks, numbered by learning progression
├── src/          # Python package source
├── tests/        # unit/ and integration/ subdirectories
├── docs/
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Active Projects

### machine-learning/pyhealth/
PyHealth learning and enterprise health informatics automation toolkit.
- **Purpose**: Learn PyHealth API + build enterprise-grade EHR prediction pipelines
- **Package**: `pyhealth_enterprise` (installable via `pip install -e .`)
- **Data tiers**: `data/samples/` (synthetic, no credentials) | `data/raw/` (MIMIC/OMOP, gitignored)
- **Notebooks**: Numbered 01–06, progressing from setup → datasets → tasks → models → evaluation → enterprise pipelines
- **Setup**: `python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && pip install -e .`
- **Tests**: `pytest tests/unit/` (no credentials needed); `pytest tests/integration/ -m integration` (requires data)
- **Key PyHealth pipeline**: Dataset → `.set_task()` → `split_by_patient` → `get_dataloader` → Model → `Trainer`

### machine-learning/learning_health_system_for_medical_imaging/
Medical imaging pipeline using MIMIC-CXR and X-raydar CV models.
- Chest X-ray phenotype extraction, knowledge encoding, and recommendation
- External dependency: x-raydar-cv (clone separately)

## Data Access Notes
- MIMIC-III/IV and eICU require PhysioNet credentialing — store credentials in `.env` (gitignored)
- All `data/raw/` and `data/processed/` directories are gitignored
- Synthetic demo data in `data/samples/` can be generated without credentials
