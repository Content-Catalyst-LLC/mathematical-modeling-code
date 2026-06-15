from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from nonlinear_dynamics.cli import (
    bistable_equilibria,
    bistable_rate,
    logistic_equilibria,
    logistic_rate,
    simulate_scalar,
)

def test_logistic_rate():
    assert logistic_rate(10.0, 0.6, 100.0) == 5.4

def test_logistic_equilibria():
    assert logistic_equilibria(100.0) == (0.0, 100.0)

def test_bistable_rate_at_threshold():
    assert bistable_rate(0.4, 0.4) == 0.0

def test_bistable_equilibria():
    assert bistable_equilibria(0.4) == (0.0, 0.4, 1.0)

def test_simulation_length():
    records = simulate_scalar("test", 10.0, 0.1, 10, lambda x: logistic_rate(x, 0.6, 100.0), (0.6, 100.0, 0.0), "warning")
    assert len(records) == 11
