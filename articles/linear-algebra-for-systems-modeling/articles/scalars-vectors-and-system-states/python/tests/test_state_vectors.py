from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from state_vectors.cli import COMPONENTS, change_vector, euclidean_norm, l1_norm

def test_components_have_positions():
    assert [component.position for component in COMPONENTS] == [1, 2, 3, 4, 5]

def test_norms():
    assert l1_norm([1.0, -2.0, 3.0]) == 6.0
    assert round(euclidean_norm([3.0, 4.0]), 6) == 5.0

def test_change_vector():
    assert change_vector([2.0, 4.0], [1.0, 1.5]) == [1.0, 2.5]

def test_change_vector_dimension_check():
    try:
        change_vector([1.0], [1.0, 2.0])
    except ValueError as exc:
        assert "same dimension" in str(exc)
    else:
        raise AssertionError("dimension mismatch should raise ValueError")
