from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from limits_formal_basis.core import (
    central_difference,
    convergence_study,
    exact_derivative,
    forward_difference,
    richardson_extrapolation,
)


def test_central_difference_beats_forward_for_smooth_function():
    x = 5.0
    h = 0.1
    exact = exact_derivative(x)
    forward_error = abs(forward_difference(x, h) - exact)
    central_error = abs(central_difference(x, h) - exact)
    assert central_error < forward_error


def test_richardson_extrapolation_improves_central_estimate():
    x = 5.0
    h = 0.2
    exact = exact_derivative(x)
    cd = central_difference(x, h)
    cd_half = central_difference(x, h / 2.0)
    rich = richardson_extrapolation(cd, cd_half)
    assert abs(rich - exact) < abs(cd - exact)


def test_invalid_step_size_raises():
    try:
        forward_difference(5.0, 0.0)
    except ValueError:
        return
    raise AssertionError("Expected ValueError for zero step size.")


def test_convergence_study_has_three_methods():
    rows = convergence_study(5.0, [1.0, 0.5, 0.25])
    methods = {row.method for row in rows}
    assert methods == {"forward_difference", "central_difference", "richardson_central"}
