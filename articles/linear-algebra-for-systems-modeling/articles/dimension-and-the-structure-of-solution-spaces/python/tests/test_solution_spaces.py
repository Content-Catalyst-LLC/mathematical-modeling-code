from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from solution_spaces.cli import build_audit, matrix_rank


def test_rank_three_constraints_four_variables():
    matrix = [
        [1.0, 1.0, 0.0, 0.0],
        [0.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0, 1.0],
    ]
    assert matrix_rank(matrix) == 3


def test_rank_dependent_constraints():
    matrix = [
        [1.0, 2.0],
        [2.0, 4.0],
    ]
    assert matrix_rank(matrix) == 1


def test_build_audit_nullity():
    audit = build_audit()
    assert audit.variable_count == 4
    assert audit.rank == 3
    assert audit.nullity == 1
    assert "Positive-dimensional" in audit.likely_solution_structure
