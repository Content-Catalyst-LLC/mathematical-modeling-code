from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from linear_first_order.cli import (
    analytical_solution,
    equilibrium,
    rate_law,
    simulate_linear_input_loss,
)

def test_equilibrium():
    assert equilibrium(12.0, 0.4) == 30.0

def test_rate_law():
    assert rate_law(20.0, 12.0, 0.4) == 4.0

def test_analytical_initial():
    assert analytical_solution(0.0, 20.0, 12.0, 0.4) == 20.0

def test_simulation_length():
    assert len(simulate_linear_input_loss(20.0, 12.0, 0.4, 0.1, 10)) == 11

def test_record_warning():
    record = simulate_linear_input_loss(20.0, 12.0, 0.4, 0.1, 1)[0]
    assert "constant input" in record.warning
