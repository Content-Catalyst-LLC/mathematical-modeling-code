from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from convergence.core import audit_geometric, audit_harmonic, audit_p_series, geometric_terms, harmonic_terms


def test_geometric_reference_value():
    audit = audit_geometric(10.0, 0.6, 25)
    assert abs(audit.reference_value - 25.0) < 1e-12
    assert audit.convergence_classification == "convergent geometric series"


def test_geometric_divergence_warning():
    audit = audit_geometric(10.0, 1.1, 10)
    assert "does not support" in audit.warning


def test_harmonic_warning():
    audit = audit_harmonic(1000)
    assert "small last term" in audit.warning


def test_p_series_classification():
    assert audit_p_series(1.25, 100).convergence_classification == "convergent p-series"
    assert audit_p_series(1.0, 100).convergence_classification == "divergent p-series"


def test_rejects_nonpositive_term_count():
    try:
        geometric_terms(1.0, 0.5, 0)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

    try:
        harmonic_terms(0)
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
