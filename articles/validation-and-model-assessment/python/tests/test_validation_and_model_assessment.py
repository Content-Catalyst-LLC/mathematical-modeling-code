from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from validation_and_model_assessment.core import (
    ValidationObservation,
    ValidationRecord,
    classify_fitness,
    error_rows,
    metric_summary,
    scenario_summary,
    validation_risk_score,
)


def sample_data():
    return [
        ValidationObservation(1, 10.0, 9.5, "holdout"),
        ValidationObservation(2, 11.0, 10.0, "holdout"),
        ValidationObservation(3, 12.0, 11.0, "stress"),
    ]


def test_error_rows_contains_residuals():
    rows = error_rows(sample_data())
    assert rows[0]["residual"] == 0.5
    assert len(rows) == 3


def test_metric_summary_has_rmse():
    summary = metric_summary(error_rows(sample_data()))
    assert "rmse" in summary
    assert summary["rmse"] >= 0


def test_scenario_summary_groups_rows():
    summary = scenario_summary(error_rows(sample_data()))
    assert len(summary) == 2


def test_classify_fitness_returns_label():
    label = classify_fitness({"rmse": 1.0, "max_abs_error": 1.5})
    assert label == "adequate_for_scenario_screening"


def test_validation_risk_score_positive():
    record = ValidationRecord(
        "data_validation",
        "evidence",
        "Reviews observations and provenance.",
        "Are validation data reliable?",
        "review",
    )
    assert validation_risk_score(record) > 0
