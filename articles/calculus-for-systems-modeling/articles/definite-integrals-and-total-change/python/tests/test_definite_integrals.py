from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from definite_integrals.core import audit_integral, rectangle_integral, signed_values, trapezoid_integral


def test_times_must_be_increasing():
    try:
        trapezoid_integral([1, 2, 3], [0, 1, 1])
    except ValueError as exc:
        assert "strictly increasing" in str(exc)
    else:
        raise AssertionError("Expected ValueError for repeated time point")


def test_trapezoid_integral_returns_float():
    times = [0, 0.5, 1.0]
    values = signed_values(times)
    assert isinstance(trapezoid_integral(values, times), float)


def test_audit_reports_interval():
    audit = audit_integral([0, 0.5, 1.0, 1.5, 2.0])
    assert audit.interval_start == 0
    assert audit.interval_end == 2.0


def test_rectangle_and_trapezoid_can_differ():
    times = [0, 0.5, 1.0, 1.5]
    values = signed_values(times)
    assert rectangle_integral(values, times) != trapezoid_integral(values, times)
