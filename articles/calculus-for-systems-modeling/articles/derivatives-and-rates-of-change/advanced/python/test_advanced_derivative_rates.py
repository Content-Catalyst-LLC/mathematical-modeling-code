from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_derivative_rates import central_difference, exact_derivative, forward_difference, invariant_review, rate_diagnostics


def test_central_difference_beats_forward():
    x = 5.0
    h = 0.1
    assert abs(central_difference(x, h) - exact_derivative(x)) < abs(forward_difference(x, h) - exact_derivative(x))


def test_rate_diagnostics_have_elasticity():
    rows = rate_diagnostics()
    assert all("elasticity" in row for row in rows)


def test_invariant_review_detects_failures():
    rows = invariant_review([-0.1, 0.0, 0.5, 1.0, 1.2])
    assert sum(not row.inside for row in rows) == 2


if __name__ == "__main__":
    test_central_difference_beats_forward()
    test_rate_diagnostics_have_elasticity()
    test_invariant_review_detects_failures()
    print("advanced derivative-rate checks passed")
