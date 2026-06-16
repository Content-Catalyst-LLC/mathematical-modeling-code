from pathlib import Path
import math
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from numerical_differentiation.cli import (
    backward_difference,
    central_difference,
    finite_difference_audit,
    forward_difference,
    second_central_difference,
    signal,
    true_derivative,
)

def test_difference_formulas():
    assert abs(forward_difference(1.0, 1.1, 0.1) - 1.0) < 1e-12
    assert abs(backward_difference(1.1, 1.0, 0.1) - 1.0) < 1e-12
    assert abs(central_difference(1.2, 1.0, 0.1) - 1.0) < 1e-12

def test_second_difference_for_square():
    assert abs(second_central_difference(1.21, 1.0, 0.81, 0.1) - 2.0) < 1e-10

def test_signal_and_true_derivative_are_finite():
    assert math.isfinite(signal(1.0))
    assert math.isfinite(true_derivative(1.0))

def test_audit_length_and_boundary_nones():
    records = finite_difference_audit(0.0, 10.0, 0.1)
    assert len(records) == 101
    assert records[0].central_difference is None
    assert records[-1].central_difference is None
    assert records[1].central_difference is not None
