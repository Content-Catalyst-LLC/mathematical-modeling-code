from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from model_purpose.core import (
    PurposeRecord,
    ResourceScenario,
    bounded_update,
    purpose_risk_score,
    simulate_resource,
    summarize_resource,
)


def test_bounded_update_respects_capacity():
    assert bounded_update(95.0, 20.0, 1.0, 1.0, 100.0) == 100.0


def test_bounded_update_respects_zero():
    assert bounded_update(2.0, 0.0, 10.0, 1.0, 100.0) == 0.0


def test_resource_simulation_stays_within_bounds():
    scenario = ResourceScenario("test", "explanation", 80.0, 100.0, 8.0, 6.0, 0.015, 0.0, 20)
    rows = simulate_resource(scenario)
    assert len(rows) == 21
    assert all(0 <= float(row["stock"]) <= 100 for row in rows)


def test_summary_contains_purpose():
    scenario = ResourceScenario("test", "control", 80.0, 100.0, 8.0, 6.0, 0.015, 1.0, 20)
    summary = summarize_resource(simulate_resource(scenario))
    assert summary["purpose"] == "control"


def test_purpose_risk_score_is_positive():
    record = PurposeRecord(
        "decision_support",
        "Which alternative should be considered?",
        "Alternatives consequences uncertainty",
        "Decision-context review",
        "Scenario matrix",
        "Decision support becomes decision substitution",
        "review",
    )
    assert purpose_risk_score(record) > 0
