"""
download_mimic_cxr.py

Script to help automate downloading MIMIC-CXR or other PhysioNet datasets without wget.
Prompts for PhysioNet credentials and downloads files using Python requests.

Instructions:
1. Register and get credentialed for MIMIC-CXR at https://physionet.org/content/mimic-cxr/
2. Run this script and enter your PhysioNet username and password when prompted.
3. Edit BASE_URL and FILES as needed for your dataset.
"""

import os
import requests
from getpass import getpass

# Set these paths as needed
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/raw/mimic-cxr'))
BASE_URL = "https://physionet.org/files/mimic-cxr/2.0.0/"

# List of files or folders to download (examples)
FILES = [
    "mimic-cxr-2.0.0-metadata.csv.gz",
    "mimic-cxr-2.0.0-split.csv.gz",
    # Add more files or folders as needed
]

os.makedirs(DATA_DIR, exist_ok=True)

username = input("PhysioNet username: ")
password = getpass("PhysioNet password: ")

session = requests.Session()
session.auth = (username, password)

for fname in FILES:
    url = BASE_URL + fname
    dest = os.path.join(DATA_DIR, fname)
    print(f"Downloading {fname} to {dest} ...")
    with session.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

print("Download complete. For DICOM images or recursive download, see PhysioNet instructions or extend this script.")
