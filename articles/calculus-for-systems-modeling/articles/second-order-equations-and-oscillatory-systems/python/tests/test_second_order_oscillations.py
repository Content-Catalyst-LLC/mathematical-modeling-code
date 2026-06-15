from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from second_order_oscillations.cli import (
    acceleration,
    classify_damping,
    forcing_function,
    simulate_oscillator,
)

def test_forcing_function_zero_amplitude():
    assert forcing_function(10.0, 0.0, 1.0) == 0.0

def test_acceleration_unforced_initial():
    assert acceleration(1.0, 0.0, 0.0, 0.2, 1.0, 0.0, 1.0) == -1.0

def test_damping_classification():
    assert classify_damping(0.0) == "undamped"
    assert classify_damping(0.2) == "underdamped"
    assert classify_damping(1.0) == "critically_damped"
    assert classify_damping(2.0) == "overdamped"

def test_simulation_length():
    assert len(simulate_oscillator("test", 1.0, 0.0, 0.2, 1.0, 0.0, 1.0, 0.02, 10)) == 11

def test_record_warning():
    record = simulate_oscillator("test", 1.0, 0.0, 0.2, 1.0, 0.0, 1.0, 0.02, 1)[0]
    assert "step size" in record.warning
