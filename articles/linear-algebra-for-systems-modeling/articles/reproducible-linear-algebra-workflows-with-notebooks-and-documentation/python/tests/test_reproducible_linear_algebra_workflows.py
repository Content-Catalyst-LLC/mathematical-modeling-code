from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from reproducible_linear_algebra_workflows.cli import build_audit


def test_reproducibility_score_is_complete_for_reference_case():
    audit = build_audit()
    assert audit.reproducibility_score == 100


def test_reference_residual_passes():
    audit = build_audit()
    assert audit.residual_norm < 1e-10
    assert audit.relative_residual < 1e-10


def test_audit_contains_documentation_status():
    audit = build_audit()
    assert "readme" in audit.documentation_status
    assert audit.matrix_shape == "2x2"
