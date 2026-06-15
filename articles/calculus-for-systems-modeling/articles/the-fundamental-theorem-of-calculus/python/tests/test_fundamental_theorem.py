from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from fundamental_theorem.core import audit, rate, state, trapezoid_integral


def test_rate_is_derivative_of_state_at_zero():
    assert abs(rate(0.0) - 5.0) < 1e-12
    assert abs(state(0.0) - 50.0) < 1e-12


def test_times_must_be_increasing():
    try:
        trapezoid_integral([0, 1, 1])
    except ValueError as exc:
        assert "strictly increasing" in str(exc)
    else:
        raise AssertionError("Expected ValueError for repeated time point")


def test_audit_reports_residual():
    record = audit([0, 0.25, 0.5, 0.75, 1.0])
    assert isinstance(record.residual, float)


def test_refined_grid_has_small_residual():
    times = [i / 100 for i in range(201)]
    record = audit(times)
    assert abs(record.residual) < 1e-3
