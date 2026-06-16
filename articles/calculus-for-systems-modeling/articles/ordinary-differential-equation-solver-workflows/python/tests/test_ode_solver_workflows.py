from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from ode_solver_workflows.cli import (
    exact_solution,
    rate_function,
    rk4_step,
    solver_audit,
    step_size_comparison,
    stiffness_indicator,
    tolerance_threshold,
)

def test_rate_and_exact():
    assert abs(rate_function(0.0, 100.0, 0.35) + 35.0) < 1e-12
    assert abs(exact_solution(0.0, 100.0, 0.35) - 100.0) < 1e-12

def test_rk4_step_positive():
    assert rk4_step(0.0, 100.0, 0.5, 0.35) > 0.0

def test_solver_audit_length():
    records = solver_audit(100.0, 0.35, 0.5, 20.0)
    assert len(records) == 41
    assert records[-1].absolute_error >= 0.0

def test_tolerance_threshold():
    assert abs(tolerance_threshold(1e-8, 1e-6, 100.0) - 0.00010001) < 1e-12

def test_stiffness_indicator():
    assert stiffness_indicator(100.0, 1.0) == 100.0

def test_step_size_comparison():
    rows = step_size_comparison(100.0, 0.35, 20.0)
    assert len(rows) == 4
    assert rows[-1]["step_size"] == 0.1
