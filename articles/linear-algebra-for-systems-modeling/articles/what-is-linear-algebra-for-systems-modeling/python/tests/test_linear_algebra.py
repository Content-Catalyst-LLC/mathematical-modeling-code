from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from linear_algebra.cli import determinant_2x2, eigenvalues_2x2, rank_2x2, build_record

def test_determinant_2x2():
    assert round(determinant_2x2([[1, 2], [3, 4]]), 6) == -2

def test_rank_2x2_full_and_dependent():
    assert rank_2x2([[1, 2], [3, 4]]) == 2
    assert rank_2x2([[1, 2], [2, 4]]) == 1

def test_eigenvalues_2x2_diagonal():
    values = eigenvalues_2x2([[2, 0], [0, 3]])
    assert set(round(v, 6) for v in values) == {2, 3}

def test_record_has_warning():
    record = build_record()
    assert record.rank == 2
    assert "Matrix interpretation depends" in record.interpretation_warning
