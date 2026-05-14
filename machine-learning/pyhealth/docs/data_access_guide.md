# Data Access Guide

## Synthetic Data (No Credentials Required)

All experiments can run on synthetic data located in `data/samples/`. Generate it once:

```powershell
python data/samples/generate_synthetic_data.py
```

This produces ~500 patients and ~1500 visits with realistic ICD-9 and ATC codes.

## MIMIC-III / MIMIC-IV (PhysioNet Access Required)

MIMIC datasets are deidentified clinical databases from Beth Israel Deaconess Medical Center.

### Getting Access

1. Complete the CITI "Data or Specimens Only Research" course
2. Register at PhysioNet: https://physionet.org/register/
3. Apply for access to MIMIC-III: https://physionet.org/content/mimiciii/
4. Apply for access to MIMIC-IV: https://physionet.org/content/mimiciv/

Access is typically granted within 1–2 weeks.

### Downloading

```bash
# MIMIC-III
wget -r -N -c -np --user YOUR_USERNAME --ask-password \
  https://physionet.org/files/mimiciii/1.4/ -P data/raw/mimic3

# MIMIC-IV
wget -r -N -c -np --user YOUR_USERNAME --ask-password \
  https://physionet.org/files/mimiciv/2.2/ -P data/raw/mimic4
```

### Configuration

Copy `.env.example` to `.env` and fill in:

```
PHYSIONET_USERNAME=your_username
PHYSIONET_PASSWORD=your_password
MIMIC3_DATA_PATH=data/raw/mimic3
MIMIC4_DATA_PATH=data/raw/mimic4
```

### PyHealth MIMIC Loading

```python
from pyhealth.datasets import MIMIC3
dataset = MIMIC3(
    root="data/raw/mimic3",
    tables=["DIAGNOSES_ICD", "PRESCRIPTIONS", "PROCEDURES_ICD", "ADMISSIONS"],
    code_mapping={"DIAGNOSES_ICD": "ICD9CM", "PRESCRIPTIONS": "ATC"},
    dev=True,   # start with dev=True (1000 patients); remove for full dataset
)
dataset.stat()
```

## OMOP CDM

OMOP (Observational Medical Outcomes Partnership) Common Data Model is used by many health systems and research networks.

### Sources

- **SynPUF**: CMS synthetic public-use files (free, no credentials)
- **Hospital data**: Many NHS and US hospital systems expose OMOP-formatted exports
- **ATLAS/OHDSI**: The OHDSI network provides OMOP CDM tooling

### PyHealth OMOP Loading

```python
from pyhealth.datasets import OMOP
dataset = OMOP(
    root="data/raw/omop",
    tables=["condition_occurrence", "drug_exposure", "measurement"],
    code_mapping={"condition_occurrence": "ICD10CM", "drug_exposure": "ATC"},
    dev=True,
)
```

## eICU Collaborative Research Database

ICU data from ~200 US hospitals. Requires separate PhysioNet access:
https://physionet.org/content/eicu-crd/

```python
from pyhealth.datasets import eICU
dataset = eICU(
    root="data/raw/eicu",
    tables=["patient", "diagnosis", "medication"],
    dev=True,
)
```
