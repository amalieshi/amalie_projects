from pyhealth_enterprise.tasks.readmission import setup_readmission_task
from pyhealth_enterprise.tasks.mortality import setup_mortality_task
from pyhealth_enterprise.tasks.length_of_stay import setup_los_task
from pyhealth_enterprise.tasks.drug_recommendation import setup_drug_recommendation_task

__all__ = [
    "setup_readmission_task",
    "setup_mortality_task",
    "setup_los_task",
    "setup_drug_recommendation_task",
]
