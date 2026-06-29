from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))
from matrix_product_interactions.cli import build_audit, matmul, matrix_to_string, shape

def test_shape():
    assert shape([[1, 2], [3, 4], [5, 6]]) == (3, 2)

def test_matmul():
    A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    B = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    assert matmul(A, B) == [[4.0, 5.0], [10.0, 11.0]]

def test_matrix_to_string():
    assert matrix_to_string([[1.0, 2.5]]) == "1.000000,2.500000"

def test_build_audit():
    audit = build_audit()
    assert audit.left_shape == "2x3"
    assert audit.right_shape == "3x2"
    assert audit.product_shape == "2x2"
    assert audit.reverse_product_available is True
    assert "transformation order" in audit.noncommutative_warning
