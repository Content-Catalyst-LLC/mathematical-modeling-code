from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from when_linear_models_clarify_and_when_they_distort.cli import build_audit


def test_linearity_audit_has_expected_slope():
    audit = build_audit()
    assert abs(audit.fitted_slope - 2.1) < 1e-10


def test_residuals_flag_curvature():
    audit = build_audit()
    assert audit.residual_sign_pattern == "+--0+"
    assert "curvature" in audit.curvature_warning.lower()


def test_interpretation_warning_mentions_assumptions():
    audit = build_audit()
    assert "assumptions" in audit.interpretation_warning
