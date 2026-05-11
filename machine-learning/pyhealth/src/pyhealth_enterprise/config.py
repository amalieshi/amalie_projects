"""
Central configuration — reads from environment variables (.env file).
Usage: from pyhealth_enterprise.config import settings
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_ROOT = Path(__file__).parent.parent.parent


class Settings:
    PROJECT_ROOT: Path = _ROOT
    SYNTHETIC_DATA_PATH: Path = _ROOT / os.getenv("SYNTHETIC_DATA_PATH", "data/samples")
    MIMIC3_DATA_PATH: Path = _ROOT / os.getenv("MIMIC3_DATA_PATH", "data/raw/mimic3")
    MIMIC4_DATA_PATH: Path = _ROOT / os.getenv("MIMIC4_DATA_PATH", "data/raw/mimic4")
    OMOP_DATA_PATH: Path = _ROOT / os.getenv("OMOP_DATA_PATH", "data/raw/omop")
    PHYSIONET_USERNAME: str = os.getenv("PHYSIONET_USERNAME", "")
    PHYSIONET_PASSWORD: str = os.getenv("PHYSIONET_PASSWORD", "")

    def has_physionet_credentials(self) -> bool:
        return bool(self.PHYSIONET_USERNAME and self.PHYSIONET_PASSWORD)


settings = Settings()
