from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from improper_integrals.core import (
    audit_infinite_cutoffs,
    audit_singular_epsilons,
    exact_tail_reference,
    p_tail_classification,
    trapezoid_function,
    tail_function,
)


def test_tail_reference():
    assert abs(exact_tail_reference() - 2.5) < 1e-12


def test_trapezoid_rejects_bad_bounds():
    try:
        trapezoid_function(tail_function, 2.0, 1.0)
    except ValueError as exc:
        assert "Upper bound" in str(exc)
    else:
        raise AssertionError("Expected ValueError for bad bounds")


def test_tail_error_decreases_with_cutoff():
    rows = audit_infinite_cutoffs([2, 20])
    assert rows[-1].tail_error < rows[0].tail_error


def test_singular_endpoint_error_decreases_with_epsilon():
    rows = audit_singular_epsilons([0.1, 0.001])
    assert abs(rows[-1].excluded_endpoint_error) < abs(rows[0].excluded_endpoint_error)


def test_p_tail_classification():
    assert p_tail_classification(2.0) == "convergent tail"
    assert "divergent" in p_tail_classification(1.0)
    assert "divergent" in p_tail_classification(0.5)
