from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from uncertainty_in_mathematical_models.core import (
    UncertainParameter,
    UncertaintyRecord,
    output_summary,
    propagation_rows,
    projection,
    quantile,
    sample_parameters,
    uncertainty_risk_score,
)


def sample_params():
    return [
        UncertainParameter("initial_stock", 72.0, 80.0, 88.0, "measurement", "Starting stock estimate."),
        UncertainParameter("growth_rate", 0.04, 0.08, 0.12, "parameter", "Dynamic replenishment rate."),
        UncertainParameter("carrying_capacity", 100.0, 120.0, 140.0, "structural", "System boundary assumption."),
        UncertainParameter("extraction_rate", 0.08, 0.12, 0.18, "scenario", "Policy and behavior driver."),
        UncertainParameter("shock_intensity", 0.00, 0.03, 0.08, "aleatory", "Stress and disturbance term."),
    ]


def test_projection_nonnegative():
    assert projection(80.0, 0.08, 120.0, 0.12, 0.03) >= 0


def test_sample_parameters_count():
    assert len(sample_parameters(sample_params(), n=12)) == 12


def test_propagation_rows_count():
    assert len(propagation_rows(sample_params())) == 1000


def test_output_summary_has_threshold_probability():
    summary = output_summary(propagation_rows(sample_params()))
    assert "threshold_probability" in summary
    assert summary["n"] == 1000


def test_quantile_ordered():
    assert quantile([1, 2, 3, 4, 5], 0.5) == 3


def test_uncertainty_risk_score_positive():
    record = UncertaintyRecord(
        "decision_uncertainty",
        "decision_support",
        "Connects uncertainty to thresholds and action.",
        "Could uncertainty reverse the decision?",
        "review",
    )
    assert uncertainty_risk_score(record) > 0
