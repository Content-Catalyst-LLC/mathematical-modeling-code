from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from singular_value_decomposition.cli import svd_diagnostic_audit


def test_svd_audit_basic_fields():
    audit = svd_diagnostic_audit()
    assert audit.rows == 6
    assert audit.columns == 4
    assert audit.numerical_rank >= 2
    assert audit.condition_number > 1.0


def test_retained_rank_and_energy():
    audit = svd_diagnostic_audit(retained_rank=2)
    assert audit.retained_rank == 2
    assert 0 < audit.explained_energy_retained <= 1


def test_reconstruction_error_nonnegative():
    audit = svd_diagnostic_audit()
    assert audit.relative_reconstruction_error >= 0
