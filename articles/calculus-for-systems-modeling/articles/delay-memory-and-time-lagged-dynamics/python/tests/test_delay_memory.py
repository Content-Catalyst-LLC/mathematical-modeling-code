from pathlib import Path
import math
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from delay_memory.cli import (
    delay_steps,
    delayed_lookup,
    history_function,
    memory_kernel_exponential,
    simulate_delayed_adjustment,
)

def test_delay_steps():
    assert delay_steps(5.0, 0.1) == 50

def test_history_function():
    assert history_function(-1.0, 80.0) == 80.0

def test_delayed_lookup_uses_history():
    assert delayed_lookup([80.0], 0, 50, 80.0) == 80.0

def test_memory_kernel():
    assert abs(memory_kernel_exponential(0.0, 0.5) - 1.0) < 1e-12
    assert memory_kernel_exponential(2.0, 0.5) < 1.0

def test_simulation_length_and_values():
    records = simulate_delayed_adjustment(80.0, 100.0, 0.2, 5.0, 0.1, 30)
    assert len(records) == 31
    assert records[0].current_state == 80.0
    assert records[0].delayed_state == 80.0
    assert math.isfinite(records[-1].current_state)
