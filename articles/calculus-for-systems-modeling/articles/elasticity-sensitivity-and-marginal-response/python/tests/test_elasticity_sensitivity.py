from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from elasticity_sensitivity.core import audit_point, audits


def test_zero_input_reports_warning():
    row = audit_point(0.0)
    assert row.elasticity is None
    assert "zero" in row.warning


def test_positive_input_has_defined_elasticity():
    row = audit_point(4.0)
    assert row.elasticity is not None
    assert row.elasticity > 0


def test_finite_difference_matches_analytic_derivative():
    row = audit_point(9.0)
    assert row.absolute_error < 1e-5


def test_multiple_audits_created():
    rows = audits([0.0, 1.0, 4.0])
    assert len(rows) == 3
