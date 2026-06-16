from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from runge_kutta_methods.cli import (
    euler_step,
    exact_solution,
    heun_step,
    midpoint_step,
    rate_function,
    rk4_stage_values,
    rk4_step,
    rk_audit,
)

def test_rate_and_exact():
    assert abs(rate_function(0.0, 100.0, 0.35) + 35.0) < 1e-12
    assert abs(exact_solution(0.0, 100.0, 0.35) - 100.0) < 1e-12

def test_steps_are_finite():
    euler = euler_step(0.0, 100.0, 0.5, 0.35)
    midpoint = midpoint_step(0.0, 100.0, 0.5, 0.35)
    heun = heun_step(0.0, 100.0, 0.5, 0.35)
    rk4 = rk4_step(0.0, 100.0, 0.5, 0.35)
    assert euler > 0
    assert midpoint > 0
    assert heun > 0
    assert rk4 > 0

def test_stage_values():
    stages = rk4_stage_values(0.0, 100.0, 0.5, 0.35)
    assert set(stages) == {"k1", "k2", "k3", "k4"}

def test_rk4_more_accurate_than_euler_on_decay():
    records = rk_audit(100.0, 0.35, 0.5, 20.0)
    assert len(records) == 41
    assert records[-1].rk4_absolute_error < records[-1].euler_absolute_error
