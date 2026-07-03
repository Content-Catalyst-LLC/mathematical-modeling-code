from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from compression_noise_and_informational_tradeoffs.cli import compression_noise_audit


def test_compression_audit_basic_fields():
    audit, singular_values, row_residuals = compression_noise_audit()
    assert audit.rows == 9
    assert audit.columns == 6
    assert audit.retained_rank == 2
    assert 0 < audit.retained_energy_ratio <= 1


def test_energy_and_residual_outputs():
    audit, singular_values, row_residuals = compression_noise_audit()
    assert len(singular_values) > 0
    assert len(row_residuals) == 9


def test_error_metrics_nonnegative():
    audit, singular_values, row_residuals = compression_noise_audit()
    assert audit.relative_reconstruction_error >= 0
    assert audit.maximum_row_residual >= 0
