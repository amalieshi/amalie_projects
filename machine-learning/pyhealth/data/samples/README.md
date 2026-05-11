# Synthetic Sample Data

Synthetic EHR data generated for learning and testing without requiring PhysioNet credentials or access to real patient data.

## Generate

```powershell
python generate_synthetic_data.py
```

This produces ~500 patients and ~1500 visits with realistic ICD-9 diagnosis codes and ATC medication codes.

## Files

| File | Description |
|---|---|
| `synthetic_patients.csv` | Patient demographics (id, gender, age, ethnicity) |
| `synthetic_visits.csv` | Hospital visits (id, patient, admission/discharge dates, type) |
| `synthetic_diagnoses.csv` | ICD-9 diagnosis codes per visit |
| `synthetic_medications.csv` | ATC medication codes per visit |
| `synthetic_labs.csv` | Lab results per visit |

## Notes

- All data is randomly generated — no real patient information
- ICD-9 codes drawn from a realistic distribution of common diagnoses
- ATC codes drawn from a realistic distribution of common medications
- Designed to match the schema expected by `pyhealth.datasets.SampleDataset`
