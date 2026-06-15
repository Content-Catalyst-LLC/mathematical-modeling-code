from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from convergence_tests.core import (
    audit_alternating_harmonic,
    audit_geometric,
    audit_harmonic,
    audit_p_series,
    geometric_terms,
)


def test_geometric_convergent_error_small():
    audit = audit_geometric(10.0, 0.6, 25)
    assert audit.test_result == "converges by geometric-series test"
    assert audit.estimated_error is not None
    assert audit.estimated_error > 0


def test_geometric_nonconvergent_warns():
    audit = audit_geometric(10.0, 1.05, 25)
    assert "not below one" in audit.warning


def test_harmonic_diverges():
    audit = audit_harmonic(1000)
    assert audit.test_result == "diverges"


def test_p_series_classification():
    assert audit_p_series(1.25, 1000).test_result == "converges"
    assert audit_p_series(0.75, 1000).test_result == "diverges"


def test_alternating_has_error_bound():
    audit = audit_alternating_harmonic(1000)
    assert audit.estimated_error is not None
    assert "conditionally" in audit.test_result


def test_rejects_nonpositive_terms():
    try:
        geometric_terms(1.0, 0.5, 0)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
