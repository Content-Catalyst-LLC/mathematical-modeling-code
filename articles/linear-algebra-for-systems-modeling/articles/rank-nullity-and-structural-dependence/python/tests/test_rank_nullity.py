from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from rank_nullity.cli import build_audit, rref


def test_rref_full_rank():
    _, pivots = rref([[1.0, 0.0], [0.0, 1.0]])
    assert pivots == [0, 1]


def test_rref_rank_deficient():
    _, pivots = rref([[1.0, 2.0], [2.0, 4.0]])
    assert pivots == [0]


def test_build_audit():
    audit = build_audit()
    assert audit.row_count == 3
    assert audit.column_count == 3
    assert audit.rank == 3
    assert audit.nullity == 0
    assert audit.free_columns == "none"
