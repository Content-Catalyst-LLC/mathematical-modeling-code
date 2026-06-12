from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from differential_equations_dynamic_models.core import (
    DynamicModelRecord,
    DynamicScenario,
    derivative,
    dynamic_risk_score,
    simulate_euler,
    summarize_trajectory,
)


def test_dynamic_scenario_runs_and_respects_domain():
    scenario = DynamicScenario("test", 80.0, 100.0, 8.0, 6.0, 0.015, 0.25, 10.0)
    rows = simulate_euler(scenario)
    assert len(rows) == 41
    assert all(bool(row["domain_valid"]) for row in rows)


def test_derivative_matches_stock_flow_formula():
    scenario = DynamicScenario("test", 80.0, 100.0, 8.0, 6.0, 0.015, 0.25, 10.0)
    assert abs(derivative(80.0, scenario) - 0.8) < 1e-9


def test_summary_contains_dynamic_behavior():
    scenario = DynamicScenario("test", 80.0, 100.0, 8.0, 6.0, 0.015, 0.25, 10.0)
    summary = summarize_trajectory(simulate_euler(scenario))
    assert "mean_rate_of_change" in summary
    assert summary["max_storage"] <= 100.0


def test_dynamic_risk_score_positive():
    record = DynamicModelRecord(
        "time_step",
        "numerical_setting",
        "dt",
        "Integration time step.",
        "positive_time_increment",
        "Do conclusions change under smaller dt?",
        "review",
    )
    assert dynamic_risk_score(record) > 0
