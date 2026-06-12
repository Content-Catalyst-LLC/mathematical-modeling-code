from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from optimization_models_objective_functions.core import (
    OptimizationRecord,
    OptimizationScenario,
    Program,
    best_feasible,
    enumerate_choices,
    optimization_risk_score,
)


def test_enumeration_finds_feasible_choices():
    programs = [
        Program("a", 10.0, 5.0, 0, 2),
        Program("b", 9.0, 4.0, 0, 2),
    ]
    scenario = OptimizationScenario("test", 10.0, 0)
    rows = enumerate_choices(programs, scenario)
    assert len(rows) == 9
    assert any(bool(row["feasible"]) for row in rows)


def test_best_feasible_returns_solution_status():
    programs = [
        Program("a", 10.0, 5.0, 0, 2),
        Program("b", 9.0, 4.0, 0, 2),
    ]
    rows = enumerate_choices(programs, OptimizationScenario("test", 10.0, 0))
    best = best_feasible(rows)
    assert best["status"] == "optimal_in_enumerated_feasible_set"
    assert best["total_benefit"] >= 0


def test_optimization_risk_score_positive():
    record = OptimizationRecord(
        "objective_function",
        "objective_function",
        "maximize benefit",
        "The model maximizes benefit.",
        "Does the objective hide distributional concerns?",
        "review",
    )
    assert optimization_risk_score(record) > 0
