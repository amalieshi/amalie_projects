"""
End-to-end integration test: synthetic data -> task -> model -> batch risk scoring.
Runs with minimal epochs (2) for speed; requires synthetic CSVs to exist.
"""
import pytest


@pytest.mark.integration
@pytest.mark.slow
def test_batch_risk_pipeline_end_to_end(synthetic_dataset):
    from pyhealth_enterprise.models.registry import ModelName, get_model
    from pyhealth_enterprise.pipelines.batch_risk_scorer import BatchRiskScorer
    from pyhealth_enterprise.tasks.readmission import setup_readmission_task

    train, val, test, *_ = setup_readmission_task(
        synthetic_dataset.dataset, batch_size=16
    )
    task_dataset = synthetic_dataset.dataset.set_task(
        __import__(
            "pyhealth.tasks", fromlist=["readmission_prediction_mimic3_fn"]
        ).readmission_prediction_mimic3_fn
    )

    model = get_model(
        ModelName.RETAIN,
        task_dataset,
        feature_keys=["conditions", "drugs"],
        label_key="readmission",
        mode="binary",
    )

    scorer = BatchRiskScorer(model, model_name="retain_readmission_test")
    scorer.train(train, val, epochs=2, monitor="pr_auc")

    results = scorer.score_batch(test)
    assert len(results) > 0
    assert "risk_score" in results.columns
    assert "risk_label" in results.columns
