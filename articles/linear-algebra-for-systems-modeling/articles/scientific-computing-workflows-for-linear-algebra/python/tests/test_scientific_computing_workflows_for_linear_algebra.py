from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from scientific_computing_workflows_for_linear_algebra.cli import build_audit


def test_audit_passes_residual_tolerance():
    audit = build_audit()
    assert audit.reproducibility_status == "pass_residual_tolerance"
    assert audit.relative_residual <= audit.tolerance


def test_audit_records_workflow_context():
    audit = build_audit()
    assert audit.matrix_shape == "3x3"
    assert "dense" in audit.representation
    assert "solver" in audit.solver_choice


def test_condition_proxy_positive():
    audit = build_audit()
    assert audit.condition_number_proxy > 0
