"""
Generates synthetic EHR demo data for PyHealth experimentation.
No credentials or external dependencies beyond pandas and numpy.

Run: python generate_synthetic_data.py
"""
import random
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_PATIENTS = 500
MIN_VISITS_PER_PATIENT = 1
MAX_VISITS_PER_PATIENT = 6
OUTPUT_DIR = Path(__file__).parent

# Realistic ICD-9 diagnosis codes (common conditions)
ICD9_CODES = [
    "428.0",  # Congestive heart failure
    "410.9",  # Acute myocardial infarction
    "486",    # Pneumonia
    "250.00", # Diabetes mellitus type 2
    "401.9",  # Essential hypertension
    "414.01", # Coronary artery disease
    "496",    # COPD
    "585.3",  # Chronic kidney disease stage 3
    "276.1",  # Hyposmolality
    "272.4",  # Hyperlipidemia
    "427.31", # Atrial fibrillation
    "584.9",  # Acute kidney failure
    "507.0",  # Aspiration pneumonia
    "518.81", # Acute respiratory failure
    "038.9",  # Septicemia
    "486",    # Pneumonia
    "305.1",  # Tobacco use
    "311",    # Depressive disorder
    "V58.61", # Anticoagulant therapy
    "599.0",  # UTI
]

# ATC medication codes (common drug classes)
ATC_CODES = [
    "A02BC01",  # Omeprazole (PPI)
    "B01AC06",  # Aspirin
    "C07AB03",  # Atenolol (beta-blocker)
    "C09AA02",  # Enalapril (ACE inhibitor)
    "C10AA01",  # Simvastatin (statin)
    "J01CA04",  # Amoxicillin
    "J01FA09",  # Clarithromycin
    "N02BE01",  # Paracetamol
    "C03CA01",  # Furosemide (loop diuretic)
    "A10BA02",  # Metformin
    "B01AA03",  # Warfarin
    "C08CA01",  # Amlodipine (calcium channel blocker)
    "H03AA01",  # Levothyroxine
    "J01DD04",  # Ceftriaxone
    "N05BA01",  # Diazepam
    "R03AC02",  # Salbutamol (beta-2 agonist)
    "C01DA02",  # Glyceryl trinitrate
    "A12BA01",  # Potassium chloride
    "B05BA01",  # Normal saline
    "N02AX02",  # Tramadol
]

LAB_TESTS = [
    ("Creatinine", 0.6, 4.0, "mg/dL"),
    ("Glucose", 70, 400, "mg/dL"),
    ("Hemoglobin", 7.0, 17.0, "g/dL"),
    ("WBC", 2.0, 20.0, "K/uL"),
    ("Sodium", 130, 150, "mEq/L"),
    ("Potassium", 2.5, 6.0, "mEq/L"),
    ("BUN", 5, 100, "mg/dL"),
    ("Troponin", 0.01, 5.0, "ng/mL"),
]

GENDERS = ["M", "F"]
ETHNICITIES = ["WHITE", "BLACK", "HISPANIC", "ASIAN", "OTHER"]
VISIT_TYPES = ["EMERGENCY", "ELECTIVE", "URGENT"]


def generate_patients(n: int) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    return pd.DataFrame(
        {
            "patient_id": [f"P{i:05d}" for i in range(n)],
            "gender": rng.choice(GENDERS, n),
            "age": rng.integers(18, 95, n),
            "ethnicity": rng.choice(ETHNICITIES, n),
        }
    )


def generate_visits(patients: pd.DataFrame) -> pd.DataFrame:
    rng = random.Random(SEED)
    rows = []
    visit_id = 0
    base_date = pd.Timestamp("2020-01-01")

    for _, patient in patients.iterrows():
        n_visits = rng.randint(MIN_VISITS_PER_PATIENT, MAX_VISITS_PER_PATIENT)
        current_date = base_date + pd.Timedelta(days=rng.randint(0, 365))

        for _ in range(n_visits):
            los_days = rng.randint(1, 14)
            admission = current_date
            discharge = current_date + pd.Timedelta(days=los_days)
            rows.append(
                {
                    "visit_id": f"V{visit_id:06d}",
                    "patient_id": patient["patient_id"],
                    "admission_time": admission.strftime("%Y-%m-%d"),
                    "discharge_time": discharge.strftime("%Y-%m-%d"),
                    "visit_type": rng.choice(VISIT_TYPES),
                }
            )
            visit_id += 1
            current_date = discharge + pd.Timedelta(days=rng.randint(30, 365))

    return pd.DataFrame(rows)


def generate_diagnoses(visits: pd.DataFrame) -> pd.DataFrame:
    rng = random.Random(SEED + 1)
    rows = []
    for _, visit in visits.iterrows():
        n_codes = rng.randint(1, 5)
        codes = rng.sample(ICD9_CODES, min(n_codes, len(ICD9_CODES)))
        for seq, code in enumerate(codes):
            rows.append(
                {
                    "visit_id": visit["visit_id"],
                    "patient_id": visit["patient_id"],
                    "icd_code": code,
                    "icd_version": 9,
                    "sequence": seq + 1,
                }
            )
    return pd.DataFrame(rows)


def generate_medications(visits: pd.DataFrame) -> pd.DataFrame:
    rng = random.Random(SEED + 2)
    rows = []
    for _, visit in visits.iterrows():
        n_meds = rng.randint(1, 6)
        meds = rng.sample(ATC_CODES, min(n_meds, len(ATC_CODES)))
        for med in meds:
            rows.append(
                {
                    "visit_id": visit["visit_id"],
                    "patient_id": visit["patient_id"],
                    "drug_code": med,
                    "drug_name": med,
                    "dose": f"{rng.randint(1, 500)} mg",
                    "route": rng.choice(["PO", "IV", "SC", "IM"]),
                }
            )
    return pd.DataFrame(rows)


def generate_labs(visits: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED + 3)
    rows = []
    for _, visit in visits.iterrows():
        for lab_name, lo, hi, unit in rng.choice(LAB_TESTS, size=rng.integers(2, 6)):
            value = float(rng.uniform(float(lo), float(hi)))
            rows.append(
                {
                    "visit_id": visit["visit_id"],
                    "patient_id": visit["patient_id"],
                    "lab_name": lab_name,
                    "value": round(value, 2),
                    "unit": unit,
                    "flag": "H" if value > float(hi) * 0.85 else ("L" if value < float(lo) * 1.15 else "N"),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    print("Generating synthetic EHR data...")

    patients = generate_patients(N_PATIENTS)
    visits = generate_visits(patients)
    diagnoses = generate_diagnoses(visits)
    medications = generate_medications(visits)
    labs = generate_labs(visits)

    patients.to_csv(OUTPUT_DIR / "synthetic_patients.csv", index=False)
    visits.to_csv(OUTPUT_DIR / "synthetic_visits.csv", index=False)
    diagnoses.to_csv(OUTPUT_DIR / "synthetic_diagnoses.csv", index=False)
    medications.to_csv(OUTPUT_DIR / "synthetic_medications.csv", index=False)
    labs.to_csv(OUTPUT_DIR / "synthetic_labs.csv", index=False)

    print(f"  Patients  : {len(patients):,}")
    print(f"  Visits    : {len(visits):,}")
    print(f"  Diagnoses : {len(diagnoses):,}")
    print(f"  Medications: {len(medications):,}")
    print(f"  Lab results: {len(labs):,}")
    print(f"\nFiles written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
