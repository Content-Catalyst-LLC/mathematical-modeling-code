from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from pivot_structure.cli import (
    augmented_rank_from_rref,
    build_audit,
    classify_solution_behavior,
    rank_from_rref,
    rref,
)


def test_rref_pivots():
    reduced, pivots = rref([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]])
    assert pivots == [0, 1]
    assert reduced == [[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]]


def test_rank_and_augmented_rank():
    reduced = [[1.0, 0.0, 2.0], [0.0, 0.0, 0.0]]
    assert rank_from_rref(reduced, coefficient_columns=2) == 1
    assert augmented_rank_from_rref(reduced) == 1


def test_classify_solution_behavior():
    assert classify_solution_behavior(2, 3, 2) == (False, "no solution")
    assert classify_solution_behavior(2, 2, 2) == (True, "unique solution")
    assert classify_solution_behavior(1, 1, 2) == (True, "infinitely many solutions")


def test_build_audit():
    audit = build_audit()
    assert audit.pivot_columns == "0,1,2"
    assert audit.free_columns == "none"
    assert audit.solution_behavior == "unique solution"
