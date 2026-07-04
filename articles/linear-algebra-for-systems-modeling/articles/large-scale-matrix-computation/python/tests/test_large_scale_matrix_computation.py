from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from large_scale_matrix_computation.cli import computation_audit


def test_large_scale_audit_basic_fields():
    audit, residuals, product_vector = computation_audit()
    assert audit.matrix_dimension == 200
    assert audit.nonzero_entries > 0
    assert audit.density > 0


def test_residuals_decrease():
    audit, residuals, product_vector = computation_audit()
    assert len(residuals) == 81
    assert audit.iterative_residual_final < audit.iterative_residual_initial


def test_matrix_vector_product_sample():
    audit, residuals, product_vector = computation_audit()
    assert len(product_vector) == audit.matrix_dimension
    assert audit.matrix_vector_product_norm > 0
