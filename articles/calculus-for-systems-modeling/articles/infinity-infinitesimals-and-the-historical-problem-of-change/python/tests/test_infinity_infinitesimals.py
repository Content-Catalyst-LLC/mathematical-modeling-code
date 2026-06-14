from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from infinity_infinitesimals_change.core import (
    difference_quotient,
    exact_derivative,
    run_approximations,
)


def test_difference_quotient_positive():
    assert difference_quotient(5.0, 0.1) > 0


def test_small_h_improves_against_large_h_for_smooth_example():
    exact = exact_derivative(5.0)
    large_error = abs(difference_quotient(5.0, 1.0) - exact)
    small_error = abs(difference_quotient(5.0, 0.001) - exact)
    assert small_error < large_error


def test_run_approximations_returns_records():
    records = run_approximations(5.0, [1.0, 0.1, 0.01])
    assert len(records) == 3
