from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from matrix_arithmetic.cli import add, build_audit, linear_combination, same_shape, shape, subtract


def test_same_shape():
    assert same_shape([[1, 2]], [[3, 4]]) is True
    assert same_shape([[1, 2]], [[3], [4]]) is False


def test_add_and_subtract():
    A = [[1.0, 2.0], [3.0, 4.0]]
    B = [[0.5, 0.5], [1.0, 1.0]]
    assert add(A, B) == [[1.5, 2.5], [4.0, 5.0]]
    assert subtract(A, B) == [[0.5, 1.5], [2.0, 3.0]]


def test_linear_combination():
    A = [[1.0, 2.0]]
    B = [[10.0, 20.0]]
    assert linear_combination(2.0, A, 0.5, B) == [[7.0, 14.0]]


def test_build_audit():
    audit = build_audit()
    assert audit.matrix_shape == "3x3"
    assert audit.compatible_shape is True
    assert "shape-compatible" in audit.interpretation_warning
