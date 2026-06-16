from pathlib import Path
import math
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from eulers_method.cli import (
    euler_audit,
    euler_step,
    exact_solution,
    logistic_step,
    rate_function,
    stability_multiplier,
    stability_status,
)

def test_rate_function():
    assert abs(rate_function(0.0, 100.0, 0.35) + 35.0) < 1e-12

def test_exact_solution_at_zero():
    assert abs(exact_solution(0.0, 100.0, 0.35) - 100.0) < 1e-12

def test_euler_step():
    assert abs(euler_step(0.0, 100.0, 0.1, 0.35) - 96.5) < 1e-12

def test_stability_multiplier():
    assert abs(stability_multiplier(0.1, 0.35) - 0.965) < 1e-12
    assert stability_status(0.1, 0.35) == "stable_for_simple_decay"

def test_logistic_step():
    assert logistic_step(10.0, 0.2, 100.0, 1.0) > 10.0

def test_euler_audit_length():
    records = euler_audit(100.0, 0.35, 0.1, 20.0)
    assert len(records) == 201
    assert records[-1].absolute_error >= 0.0
