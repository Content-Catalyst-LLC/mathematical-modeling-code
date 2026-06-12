from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from boundary_scale_scope.core import (
    BoundaryChoice,
    ResourceScenario,
    boundary_risk_score,
    bounded_update,
    simulate_resource,
    summarize_resource,
)


def test_bounded_update_respects_capacity():
    assert bounded_update(95.0, 20.0, 1.0, 1.0, 100.0) == 100.0


def test_bounded_update_respects_zero():
    assert bounded_update(2.0, 0.0, 10.0, 1.0, 100.0) == 0.0


def test_resource_simulation_stays_within_bounds():
    scenario = ResourceScenario("test", "narrow", 80.0, 100.0, 8.0, 6.0, 0.015, 0.0, 20)
    rows = simulate_resource(scenario)
    assert len(rows) == 21
    assert all(0 <= float(row["stock"]) <= 100 for row in rows)


def test_summary_contains_boundary_version():
    scenario = ResourceScenario("test", "narrow", 80.0, 100.0, 8.0, 6.0, 0.015, 0.0, 20)
    summary = summarize_resource(simulate_resource(scenario))
    assert summary["boundary_version"] == "narrow"


def test_boundary_risk_score_is_positive():
    boundary = BoundaryChoice(
        "population_boundary",
        "population",
        "aggregate users",
        "vulnerable populations",
        "Distributional effects may be hidden.",
        "Are subgroup outputs needed?",
        "review",
    )
    assert boundary_risk_score(boundary) > 0
