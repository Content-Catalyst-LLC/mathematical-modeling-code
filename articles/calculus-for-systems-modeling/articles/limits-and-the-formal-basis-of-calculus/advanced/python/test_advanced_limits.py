from __future__ import annotations

from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_limits import (
    central_difference,
    convergence_study,
    exact_derivative,
    f,
    forward_difference,
    invariant_review,
    richardson_extrapolation,
)


def test_central_difference_is_better_than_forward_for_smooth_function() -> None:
    x = 5.0
    h = 0.1
    exact = exact_derivative(x)
    assert abs(central_difference(f, x, h) - exact) < abs(forward_difference(f, x, h) - exact)


def test_richardson_improves_central_estimate() -> None:
    x = 5.0
    h = 0.2
    exact = exact_derivative(x)
    central_h = central_difference(f, x, h)
    central_h2 = central_difference(f, x, h / 2.0)
    rich = richardson_extrapolation(central_h, central_h2)
    assert abs(rich - exact) < abs(central_h - exact)


def test_zero_step_rejected() -> None:
    try:
        forward_difference(f, 5.0, 0.0)
    except ValueError:
        return
    raise AssertionError("Expected ValueError for zero step size.")


def test_convergence_study_has_advanced_methods() -> None:
    rows = convergence_study()
    methods = {row.method for row in rows}
    assert {"forward_difference", "central_difference", "richardson_central"}.issubset(methods)


def test_invariant_review_detects_invalid_values() -> None:
    reviews = invariant_review([0.0, 0.5, 1.0, -0.1, 1.2], 0.0, 1.0)
    failures = [item for item in reviews if not item.inside]
    assert len(failures) == 2


if __name__ == "__main__":
    test_central_difference_is_better_than_forward_for_smooth_function()
    test_richardson_improves_central_estimate()
    test_zero_step_rejected()
    test_convergence_study_has_advanced_methods()
    test_invariant_review_detects_invalid_values()
    print("advanced limits checks passed")
