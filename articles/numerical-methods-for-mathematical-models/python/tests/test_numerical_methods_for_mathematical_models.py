from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from numerical_methods_for_mathematical_models.core import (
    NumericalRecord,
    SolverScenario,
    convergence_summary,
    derivative,
    numerical_risk_score,
    run_euler,
)


def test_derivative_returns_float():
    value = derivative(70.0, 0.18, 100.0, 6.0)
    assert isinstance(value, float)


def test_run_euler_outputs_expected_final_index():
    scenario = SolverScenario("test", 70.0, 0.18, 100.0, 6.0, 5.0, 0.5)
    rows = run_euler(scenario)
    assert rows[0]["index"] == 0
    assert rows[-1]["index"] == 10


def test_convergence_summary_contains_step_sizes():
    rows = []
    for h in [1.0, 0.5]:
        rows.extend(run_euler(SolverScenario("test", 70.0, 0.18, 100.0, 6.0, 5.0, h)))
    summary = convergence_summary(rows)
    assert len(summary) == 2
    assert "absolute_difference_from_finest_step" in summary[0]


def test_numerical_risk_score_positive():
    record = NumericalRecord(
        "step_size",
        "discretization",
        "h in {1.0 0.5 0.25 0.1}",
        "Step size controls time discretization.",
        "Does the conclusion depend on step size?",
        "review",
    )
    assert numerical_risk_score(record) > 0
