from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from robustness_fragility_and_model_dependence.core import (
    ModelScenario,
    RobustnessRecord,
    robustness_risk_score,
    robustness_rows,
    robustness_summary,
    simulate,
)


def sample_scenarios():
    return [
        ModelScenario("linear_baseline", "linear_decline", "baseline", 1.0, 0.00, "baseline"),
        ModelScenario("linear_stress", "linear_decline", "stress", 1.25, 0.05, "stress"),
        ModelScenario("dynamic_baseline", "logistic_recovery", "baseline", 1.0, 0.00, "baseline"),
        ModelScenario("dynamic_stress", "logistic_recovery", "stress", 1.25, 0.05, "stress"),
        ModelScenario("threshold_baseline", "threshold_shift", "baseline", 1.0, 0.00, "baseline"),
        ModelScenario("threshold_stress", "threshold_shift", "stress", 1.25, 0.05, "stress"),
    ]


def test_simulate_nonnegative():
    assert simulate("linear_decline", 1.0, 0.0) >= 0


def test_robustness_rows_count():
    rows = robustness_rows(sample_scenarios())
    assert len(rows) == 6


def test_summary_has_spread():
    summary = robustness_summary(robustness_rows(sample_scenarios()))
    assert summary["robustness_spread"] >= 0
    assert summary["scenario_count"] == 6


def test_unknown_model_form_raises():
    try:
        simulate("unknown", 1.0, 0.0)
    except ValueError:
        assert True
    else:
        assert False


def test_risk_score_positive():
    record = RobustnessRecord(
        "threshold_fragility",
        "decision_threshold",
        "Measures whether small changes reverse action.",
        "How close is the output to decision reversal?",
        "review",
    )
    assert robustness_risk_score(record) > 0
