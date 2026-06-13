from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from sensitivity_analysis_and_robustness.core import (
    Parameter,
    SensitivityRecord,
    baseline_output,
    resource_projection,
    sensitivity_risk_score,
    sensitivity_summary,
    sweep_rows,
)


def sample_params():
    return [
        Parameter("initial_stock", 80.0, 72.0, 88.0, "measurement"),
        Parameter("growth_rate", 0.08, 0.04, 0.12, "parameter"),
        Parameter("carrying_capacity", 120.0, 100.0, 140.0, "structural"),
        Parameter("extraction_rate", 0.12, 0.08, 0.18, "policy"),
        Parameter("shock_intensity", 0.03, 0.00, 0.08, "scenario"),
    ]


def test_resource_projection_positive():
    value = resource_projection(80.0, 0.08, 120.0, 0.12, 0.03)
    assert value >= 0


def test_baseline_output_float():
    assert isinstance(baseline_output(sample_params()), float)


def test_sweep_rows_count():
    rows = sweep_rows(sample_params())
    assert len(rows) == 15


def test_sensitivity_summary_sorted():
    rows = sweep_rows(sample_params())
    summary = sensitivity_summary(rows)
    assert summary[0]["range_width"] >= summary[-1]["range_width"]


def test_sensitivity_risk_score_positive():
    record = SensitivityRecord(
        "threshold_fragility",
        "decision_support",
        "Reviews whether outputs cross threshold.",
        "Can plausible variation reverse the decision?",
        "review",
    )
    assert sensitivity_risk_score(record) > 0
