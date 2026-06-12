from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from discrete_models_recurrence_relations.core import (
    RecurrenceRecord,
    RecurrenceScenario,
    recurrence_risk_score,
    simulate_recurrence,
    summarize_trajectory,
)


def test_recurrence_scenario_runs_and_respects_domain():
    scenario = RecurrenceScenario("test", 80.0, 7.0, 100.0, 6.0, 0.015, 0.0, 20, False)
    rows = simulate_recurrence(scenario)
    assert len(rows) == 21
    assert all(bool(row["domain_valid"]) for row in rows)


def test_adaptive_demand_can_change_final_demand():
    scenario = RecurrenceScenario("adaptive", 45.0, 10.0, 80.0, 4.0, 0.020, 0.2, 20, True)
    summary = summarize_trajectory(simulate_recurrence(scenario))
    assert "final_demand" in summary
    assert summary["final_demand"] <= 10.0


def test_recurrence_risk_score_positive():
    record = RecurrenceRecord(
        "shortage",
        "output_diagnostic",
        "Q[t] = max(0, -raw_next_storage)",
        "Shortage before clipping.",
        "reported_each_period",
        "Is shortage accumulated, reported, or clipped away?",
        "review",
    )
    assert recurrence_risk_score(record) > 0
