from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from linear_systems.cli import augment, build_audit, classify_solution_behavior, matrix_rank


def test_matrix_rank_identity():
    assert matrix_rank([[1.0, 0.0], [0.0, 1.0]]) == 2


def test_augment():
    assert augment([[1.0, 2.0]], [3.0]) == [[1.0, 2.0, 3.0]]


def test_classify_unique_solution():
    A = [[1.0, 1.0], [1.0, -1.0]]
    b = [3.0, 1.0]
    consistent, behavior, rank_a, rank_aug = classify_solution_behavior(A, b)
    assert consistent is True
    assert behavior == "unique solution"
    assert rank_a == rank_aug == 2


def test_build_audit():
    audit = build_audit()
    assert audit.equation_count == 3
    assert audit.unknown_count == 3
    assert audit.consistent is True
    assert audit.solution_behavior == "unique solution"
