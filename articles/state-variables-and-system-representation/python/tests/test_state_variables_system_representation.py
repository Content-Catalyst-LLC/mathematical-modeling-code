from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from state_variables_system_representation.core import (
    RepresentationScenario,
    StateVariable,
    simulate_representation,
    state_risk_score,
    summarize_representation,
)


def test_storage_only_scenario_runs_and_respects_domain():
    scenario = RepresentationScenario("test", "storage_only", 80.0, 7.0, 1.0, 100.0, 6.0, 0.015, 0.0, 0.0, 20)
    rows = simulate_representation(scenario)
    assert len(rows) == 21
    assert all(bool(row["domain_valid"]) for row in rows)


def test_condition_aware_scenario_includes_condition():
    scenario = RepresentationScenario("test", "condition_aware", 45.0, 8.0, 0.85, 80.0, 4.0, 0.02, 0.2, 0.002, 20)
    summary = summarize_representation(simulate_representation(scenario))
    assert "final_condition" in summary
    assert 0 <= summary["final_condition"] <= 1


def test_state_risk_score_positive():
    record = StateVariable(
        "infrastructure_condition",
        "latent_condition",
        "dimensionless_index",
        "Infrastructure condition.",
        "Affects effective loss.",
        "proxy_observed",
        "Is the condition index validated or only assumed?",
        "review",
    )
    assert state_risk_score(record) > 0
