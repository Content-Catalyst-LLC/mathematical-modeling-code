from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from inverse_functions_interpretation.core import inverse_audit, inverse_audits


def test_forward_check_matches_target_output():
    row = inverse_audit(1.0)
    assert abs(row.residual) < 1e-10


def test_inverse_sensitivity_reciprocal_relationship():
    row = inverse_audit(1.0)
    assert abs(row.inverse_sensitivity - (1.0 / row.forward_derivative)) < 1e-12


def test_multiple_audits_created():
    rows = inverse_audits([0.0, 0.5, 1.0])
    assert len(rows) == 3
