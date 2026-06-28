from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from least_squares_thinking.cli import build_audit, matvec, norm2, solve_2x2


def test_solve_2x2():
    solution = solve_2x2([[4.0, 10.0], [10.0, 30.0]], [14.1, 40.4])
    assert [round(x, 6) for x in solution] == [0.85, 1.04]


def test_matvec():
    assert matvec([[1.0, 2.0], [3.0, 4.0]], [2.0, 1.0]) == [4.0, 10.0]


def test_norm2():
    assert norm2([3.0, 4.0]) == 5.0


def test_build_audit():
    audit = build_audit()
    assert audit.overdetermined is True
    assert audit.row_count == 4
    assert audit.column_count == 2
    assert audit.rank == 2
    assert audit.residual_norm > 0.0
