from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))
from row_reduction.cli import build_audit, classify_solution_behavior, rref

def test_rref_identity_like_system():
    reduced, pivots = rref([[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]])
    assert pivots == [0, 1]
    assert reduced == [[1.0, 0.0, 2.0], [0.0, 1.0, 3.0]]

def test_classify_solution_behavior():
    assert classify_solution_behavior(2, 3, 2) == (False, "no solution")
    assert classify_solution_behavior(2, 2, 2) == (True, "unique solution")
    assert classify_solution_behavior(1, 1, 2) == (True, "infinitely many solutions")

def test_build_audit():
    audit = build_audit()
    assert audit.equation_count == 3
    assert audit.unknown_count == 3
    assert audit.consistent is True
    assert audit.solution_behavior == "unique solution"
