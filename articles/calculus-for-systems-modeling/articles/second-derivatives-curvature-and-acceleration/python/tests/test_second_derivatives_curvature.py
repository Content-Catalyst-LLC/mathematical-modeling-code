from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from second_derivatives_curvature.core import audit_point, second_derivative_audits


def test_inflection_candidate_at_zero():
    row = audit_point(0.0)
    assert abs(row.second_derivative) < 1e-8
    assert "inflection" in row.warning


def test_finite_difference_matches_analytic_away_from_inflection():
    row = audit_point(1.0)
    assert row.absolute_error < 1e-5


def test_multiple_audits_created():
    rows = second_derivative_audits([-1.0, 0.0, 1.0])
    assert len(rows) == 3
