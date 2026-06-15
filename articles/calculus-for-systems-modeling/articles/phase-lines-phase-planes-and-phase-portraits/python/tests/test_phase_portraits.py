from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from phase_portraits.cli import (
    build_phase_grid,
    coexistence_equilibrium,
    phase_speed,
    predator_prey_rates,
)

def test_predator_prey_rates():
    dxdt, dydt = predator_prey_rates(40.0, 9.0, 0.7, 0.05, 0.02, 0.5)
    assert abs(dxdt - 10.0) < 1e-12
    assert abs(dydt - 2.7) < 1e-12

def test_coexistence_equilibrium():
    x_star, y_star = coexistence_equilibrium(0.7, 0.05, 0.02, 0.5)
    assert x_star == 25.0
    assert abs(y_star - 14.0) < 1e-12

def test_phase_speed():
    assert phase_speed(3.0, 4.0) == 5.0

def test_grid_count():
    assert len(build_phase_grid()) == 13 * 11
