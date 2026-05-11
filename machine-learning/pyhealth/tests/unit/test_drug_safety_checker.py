import pytest


def test_checker_instantiates():
    from pyhealth_enterprise.pipelines.drug_safety_checker import DrugSafetyChecker

    checker = DrugSafetyChecker()
    assert checker is not None


def test_empty_drug_list_returns_empty():
    from pyhealth_enterprise.pipelines.drug_safety_checker import DrugSafetyChecker

    checker = DrugSafetyChecker()
    result = checker.check_interactions([])
    assert len(result) == 0


def test_single_drug_returns_empty():
    from pyhealth_enterprise.pipelines.drug_safety_checker import DrugSafetyChecker

    checker = DrugSafetyChecker()
    result = checker.check_interactions(["A02BC01"])
    assert len(result) == 0


def test_two_drugs_returns_one_pair():
    from pyhealth_enterprise.pipelines.drug_safety_checker import DrugSafetyChecker

    checker = DrugSafetyChecker()
    result = checker.check_interactions(["A02BC01", "B01AC06"])
    assert len(result) == 1
    assert result.iloc[0]["drug_a"] == "A02BC01"
    assert result.iloc[0]["drug_b"] == "B01AC06"


def test_no_ddi_adj_returns_empty_flags():
    from pyhealth_enterprise.pipelines.drug_safety_checker import DrugSafetyChecker

    checker = DrugSafetyChecker()
    result = checker.flag_high_risk_combinations(["A02BC01", "B01AC06"])
    assert result == []
