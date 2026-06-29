from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from projection_reflection_geometry.cli import build_audit, dot, norm2, outer, matvec


def test_dot():
    assert dot([1.0, 2.0], [3.0, 4.0]) == 11.0


def test_norm2():
    assert norm2([3.0, 4.0]) == 5.0


def test_outer_and_matvec():
    P = outer([1.0, 0.0], [1.0, 0.0])
    assert matvec(P, [4.0, 3.0]) == [4.0, 0.0]


def test_build_audit():
    audit = build_audit()
    assert audit.original_vector == "4.000000,3.000000"
    assert audit.projection_idempotence_error == 0.0
    assert audit.reflection_involution_error == 0.0
