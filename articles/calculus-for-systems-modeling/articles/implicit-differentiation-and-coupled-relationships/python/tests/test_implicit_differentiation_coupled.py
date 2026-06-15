from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from implicit_differentiation_coupled.core import audit_parameter, implicit_audits


def test_constraint_residual_near_zero():
    row = audit_parameter(1.0)
    assert abs(row.constraint_value) < 1e-10


def test_implicit_derivative_matches_finite_difference():
    row = audit_parameter(0.0)
    assert row.absolute_error < 1e-5


def test_multiple_audits_created():
    rows = implicit_audits([-1.0, 0.0, 1.0])
    assert len(rows) == 3
