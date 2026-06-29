from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from orthogonality_structure.cli import build_audit, dot, norm2, normalize, projection


def test_dot_zero_case():
    assert dot([3.0, 1.0, 2.0], [1.0, -1.0, -1.0]) == 0.0


def test_norm2():
    assert norm2([3.0, 4.0]) == 5.0


def test_normalize():
    v = normalize([3.0, 4.0])
    assert round(norm2(v), 6) == 1.0


def test_projection_zero_when_orthogonal():
    p = projection([3.0, 1.0, 2.0], [1.0, -1.0, -1.0])
    assert p == [0.0, -0.0, -0.0]


def test_build_audit():
    audit = build_audit()
    assert audit.dot_product == 0.0
    assert audit.orthogonal_under_tolerance is True
    assert audit.orthonormality_error == 0.0
