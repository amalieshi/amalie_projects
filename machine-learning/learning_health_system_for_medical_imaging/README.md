# Learning Health System Prototype for Medical Imaging

This project is a prototype pipeline for extracting structured diagnostic information from medical imaging (e.g., chest X-rays) using open-source tools and UK-relevant use cases.

## Project Goals
- Use MIMIC-CXR and X-raydar CV models to extract structured phenotypes from imaging data
- Encode phenotypes as versioned knowledge objects
- Combine with patient factors to generate recommendations
- Evaluate technical validity and usability using imaging databases

## Project Structure
- `data/` — Raw and processed datasets
- `notebooks/` — Jupyter notebooks for exploration and prototyping
- `src/` — Source code
    - `ingestion/` — Data loading and access
    - `preprocessing/` — Data cleaning and preparation
    - `phenotype_extraction/` — Imaging feature extraction and phenotype structuring
    - `knowledge_encoding/` — Versioned knowledge object creation
    - `recommendation/` — Recommendation logic
    - `evaluation/` — Technical and usability evaluation
- `tests/` — Unit and integration tests
- `docs/` — Documentation

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Clone and install the external [x-raydar-cv](https://github.com/x-raydar/x-raydar-cv) project:
    - `git clone https://github.com/x-raydar/x-raydar-cv.git external/x-raydar-cv`
    - `pip install -r external/x-raydar-cv/requirements.txt`
    - Add `external/x-raydar-cv` to your `PYTHONPATH` if needed
3. Download and prepare MIMIC-CXR data (see docs/)
4. Run notebooks or scripts in `src/`

## Notes
*Note: The x-raydar computer vision library is an external GitHub project and must be cloned and installed separately as described above.*

This is a prototype for research and development, not for clinical use.
Contributions welcome!
```bash
