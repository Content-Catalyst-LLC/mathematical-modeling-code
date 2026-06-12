from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from functional_relationships_structure.core import (
    RelationshipRecord,
    StructureScenario,
    simulate_structure,
    structure_risk_score,
    summarize_structure,
)


def test_linear_structure_runs():
    scenario = StructureScenario("test", "linear", 80.0, 100.0, 8.0, 6.0, 0.015, 0.0, 10)
    rows = simulate_structure(scenario)
    assert len(rows) == 11
    assert rows[0]["structure"] == "linear"


def test_constrained_structure_respects_capacity():
    scenario = StructureScenario("test", "constrained", 95.0, 100.0, 20.0, 1.0, 0.0, 0.0, 10)
    rows = simulate_structure(scenario)
    assert all(0 <= float(row["next_stock"]) <= 100 for row in rows)


def test_feedback_structure_runs_and_summarizes():
    scenario = StructureScenario("test", "feedback", 40.0, 60.0, 3.0, 7.0, 0.05, 0.2, 10)
    summary = summarize_structure(simulate_structure(scenario))
    assert summary["structure"] == "feedback"
    assert "total_shortage" in summary


def test_structure_risk_score_is_positive():
    record = RelationshipRecord(
        "feedback_demand",
        "feedback",
        "D[t+1] = max(0, D[t] - alpha*shortage[t])",
        "Demand adapts after shortage.",
        "Feedback is immediate.",
        "Is demand response delayed?",
        "review",
    )
    assert structure_risk_score(record) > 0
