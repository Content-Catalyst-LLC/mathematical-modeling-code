from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from dynamic_systems.cli import (
    exponential_rate,
    logistic_rate,
    simulate_exponential,
    simulate_logistic,
)

def test_exponential_rate():
    assert exponential_rate(10.0, 0.35) == 3.5

def test_logistic_rate():
    assert abs(logistic_rate(10.0, 0.35, 100.0) - 3.15) < 1e-12

def test_simulate_exponential_length():
    assert len(simulate_exponential(10.0, 0.35, 0.1, 10)) == 11

def test_simulate_logistic_capacity_warning():
    records = simulate_logistic(10.0, 0.35, 100.0, 0.1, 2)
    assert records[0].carrying_capacity == 100.0
    assert "fixed carrying capacity" in records[0].warning
