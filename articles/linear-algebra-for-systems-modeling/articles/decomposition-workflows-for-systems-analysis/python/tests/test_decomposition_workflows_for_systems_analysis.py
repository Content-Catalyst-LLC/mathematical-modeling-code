from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from decomposition_workflows_for_systems_analysis.cli import decomposition_audit


def test_decomposition_audit_basic_fields():
    audit = decomposition_audit()
    assert audit.matrix_shape == "4x3"
    assert audit.estimated_rank == 3
    assert audit.solve_residual_norm < 1e-8


def test_singular_values_are_ordered():
    audit = decomposition_audit()
    assert audit.singular_value_1 >= audit.singular_value_2 >= audit.singular_value_3


def test_workflow_recommends_qr_or_svd():
    audit = decomposition_audit()
    assert "QR" in audit.recommended_workflow
    assert "SVD" in audit.recommended_workflow
