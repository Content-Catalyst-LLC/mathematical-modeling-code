from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from span_basis.cli import build_audit, matrix_rank


def test_rank_full_three_dimensional_basis_candidate():
    matrix = [
        [1.0, 0.0, 0.5],
        [0.0, 1.0, 0.5],
        [0.0, 0.0, 1.0],
    ]
    assert matrix_rank(matrix) == 3


def test_rank_dependent_vectors():
    matrix = [
        [1.0, 2.0],
        [2.0, 4.0],
    ]
    assert matrix_rank(matrix) == 1


def test_build_audit_identifies_basis():
    audit = build_audit()
    assert audit.ambient_dimension == 3
    assert audit.vector_count == 3
    assert audit.rank == 3
    assert audit.spans_ambient_space is True
    assert audit.linearly_independent is True
    assert audit.is_basis_for_ambient_space is True
