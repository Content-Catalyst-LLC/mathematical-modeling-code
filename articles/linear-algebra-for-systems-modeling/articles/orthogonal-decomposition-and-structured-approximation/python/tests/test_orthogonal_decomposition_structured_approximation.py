from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from orthogonal_decomposition_structured_approximation.cli import build_audit


def test_orthogonal_approximation_audit():
    audit, x, fitted, residual = build_audit()
    assert audit.rows == 6
    assert audit.columns == 3
    assert audit.numerical_rank == 3
    assert audit.residual_norm >= 0
    assert audit.relative_residual_norm >= 0


def test_orthogonality_error_small():
    audit, x, fitted, residual = build_audit()
    assert audit.orthogonality_error < 1e-10


def test_outputs_have_expected_lengths():
    audit, x, fitted, residual = build_audit()
    assert len(x) == 3
    assert len(fitted) == 6
    assert len(residual) == 6
