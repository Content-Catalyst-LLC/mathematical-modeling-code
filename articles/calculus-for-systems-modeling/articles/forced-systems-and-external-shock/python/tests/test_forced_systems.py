from pathlib import Path
import math
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from forced_systems.cli import (
    impulse_shock,
    periodic_forcing,
    restoring_rate,
    simulate_forced_system,
    shock_summary,
    step_forcing,
)

def test_restoring_rate():
    assert restoring_rate(90.0, 100.0, 0.15) == 1.5

def test_impulse_shock():
    assert impulse_shock(10.0, 10.0, -30.0) == -30.0
    assert impulse_shock(9.9, 10.0, -30.0) == 0.0

def test_step_forcing():
    assert step_forcing(9.0, 10.0, 5.0) == 0.0
    assert step_forcing(10.0, 10.0, 5.0) == 5.0

def test_periodic_forcing():
    assert abs(periodic_forcing(0.0, 2.0, 1.0, 0.0)) < 1e-12
    assert abs(periodic_forcing(math.pi / 2, 2.0, 1.0, 0.0) - 2.0) < 1e-12

def test_simulation_length_and_summary():
    records = simulate_forced_system(100.0, 100.0, 0.15, 1.0, -30.0, 0.1, 30)
    assert len(records) == 31
    summary = shock_summary(records, 0.1, 1.0, -30.0, 0.15)
    assert summary["max_deviation"] > 0
