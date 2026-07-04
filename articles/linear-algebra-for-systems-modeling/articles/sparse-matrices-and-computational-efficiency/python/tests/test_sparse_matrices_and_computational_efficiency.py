from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from sparse_matrices_and_computational_efficiency.cli import sparse_efficiency_audit


def test_sparse_audit_basic_fields():
    audit, residuals, product_vector = sparse_efficiency_audit()
    assert audit.matrix_dimension == 250
    assert audit.nonzero_entries > 0
    assert audit.density > 0


def test_sparse_storage_savings():
    audit, residuals, product_vector = sparse_efficiency_audit()
    assert audit.storage_reduction_factor > 1
    assert audit.coordinate_storage_mb_estimate < audit.dense_storage_mb


def test_residuals_decrease():
    audit, residuals, product_vector = sparse_efficiency_audit()
    assert len(residuals) == 61
    assert audit.iterative_residual_final < audit.iterative_residual_initial
