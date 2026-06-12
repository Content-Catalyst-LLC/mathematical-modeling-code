from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from assumptions_model_design.core import (
    ModelAssumption,
    ResourceScenario,
    assumption_risk_score,
    bounded_update,
    simulate_resource,
    summarize_resource,
)


def test_bounded_update_respects_capacity():
    assert bounded_update(95.0, 20.0, 1.0, 1.0, 100.0) == 100.0


def test_bounded_update_respects_zero():
    assert bounded_update(2.0, 0.0, 10.0, 1.0, 100.0) == 0.0


def test_resource_simulation_stays_within_bounds():
    scenario = ResourceScenario("test", 80.0, 100.0, 8.0, 6.0, 0.015, 20)
    rows = simulate_resource(scenario)
    assert len(rows) == 21
    assert all(0 <= float(row["stock"]) <= 100 for row in rows)


def test_summary_contains_shortage_risk():
    scenario = ResourceScenario("stress", 10.0, 100.0, 1.0, 10.0, 0.02, 10)
    summary = summarize_resource(simulate_resource(scenario))
    assert "shortage_risk" in summary


def test_assumption_risk_score_is_positive():
    assumption = ModelAssumption(
        "aggregate_stock",
        "The system is aggregate.",
        "abstraction",
        "Keeps first model transparent.",
        "Spatial variation may be hidden.",
        "Compare disaggregated model.",
        "review",
    )
    assert assumption_risk_score(assumption) > 0
