from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from constrained_optimization.cli import audit_solution, constraint, objective, solve_budget_constraint

def test_objective_value():
    assert objective(8.0, 4.0) == 96.0

def test_constraint_value():
    assert constraint(8.0, 4.0) == 12.0

def test_solution_target_12():
    x, y, lam = solve_budget_constraint(12.0)
    assert abs(x - 8.0) < 1e-12
    assert abs(y - 4.0) < 1e-12
    assert abs(lam - 16.0) < 1e-12

def test_audit_feasible():
    record = audit_solution(12.0)
    assert record.feasible is True
    assert record.stationarity_residual_norm < 1e-10

def test_warning_mentions_multiplier():
    record = audit_solution(12.0)
    assert "Multiplier" in record.warning
