from __future__ import annotations

from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_calculus_checks import (
    central_difference,
    check_interval_invariant,
    convergence_study,
    exact_derivative,
    forward_difference,
    richardson_extrapolation,
    system_response,
)


def test_central_difference_beats_forward_difference_on_smooth_function() -> None:
    x = 5.0
    h = 0.1
    exact = exact_derivative(x)
    forward_error = abs(forward_difference(system_response, x, h) - exact)
    central_error = abs(central_difference(system_response, x, h) - exact)
    assert central_error < forward_error


def test_richardson_improves_central_difference_on_smooth_function() -> None:
    x = 5.0
    h = 0.2
    exact = exact_derivative(x)
    central_h = central_difference(system_response, x, h)
    central_h2 = central_difference(system_response, x, h / 2.0)
    rich = richardson_extrapolation(central_h, central_h2, order=2)
    assert abs(rich - exact) < abs(central_h - exact)


def test_invalid_step_size_raises() -> None:
    try:
        forward_difference(system_response, 5.0, 0.0)
    except ValueError:
        return
    raise AssertionError("Expected ValueError for zero step size.")


def test_convergence_study_contains_multiple_methods() -> None:
    rows = convergence_study()
    methods = {row.method for row in rows}
    assert "forward_difference" in methods
    assert "central_difference" in methods
    assert "richardson_central" in methods


def test_invariant_check_detects_boundary_violations() -> None:
    reviews = check_interval_invariant([0.0, 0.5, 1.0, -0.1, 1.1], 0.0, 1.0)
    failures = [item for item in reviews if not item.inside]
    assert len(failures) == 2


if __name__ == "__main__":
    test_central_difference_beats_forward_difference_on_smooth_function()
    test_richardson_improves_central_difference_on_smooth_function()
    test_invalid_step_size_raises()
    test_convergence_study_contains_multiple_methods()
    test_invariant_check_detects_boundary_violations()
    print("advanced calculus checks passed")
