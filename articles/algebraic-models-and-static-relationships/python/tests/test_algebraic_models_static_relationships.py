from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from algebraic_models_static_relationships.core import (
    AlgebraicRelationship,
    AllocationScenario,
    evaluate_scenario,
    relationship_risk_score,
)


def test_feasible_scenario_is_feasible():
    scenario = AllocationScenario("test", 100.0, 4.0, 5.0, 8.0, 11.0, 10.0, 8.0, 20.0, 15.0)
    row = evaluate_scenario(scenario)
    assert row["feasible"] is True
    assert row["budget_slack"] >= 0


def test_capacity_violation_is_detected():
    scenario = AllocationScenario("bad", 120.0, 4.0, 5.0, 8.0, 11.0, 25.0, 5.0, 20.0, 15.0)
    row = evaluate_scenario(scenario)
    assert row["feasible"] is False
    assert row["constraint_status"] == "constraint violation"


def test_relationship_risk_score_positive():
    relationship = AlgebraicRelationship(
        "budget_constraint",
        "inequality",
        "c_a*x_a + c_b*x_b <= B",
        "Total cost must not exceed budget.",
        "B > 0",
        "Is the budget a hard constraint or a policy assumption?",
        "review",
    )
    assert relationship_risk_score(relationship) > 0
