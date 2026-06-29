from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from change_of_basis.cli import build_audit, det2, inv2, matvec, matmul


def test_det2():
    assert det2([[2.0, 1.0], [1.0, 2.0]]) == 3.0


def test_inv2_identity_recovery():
    P = [[2.0, 1.0], [1.0, 2.0]]
    Pinv = inv2(P)
    I = matmul(Pinv, P)
    assert round(I[0][0], 6) == 1.0
    assert round(I[1][1], 6) == 1.0


def test_matvec():
    assert matvec([[2.0, 1.0], [1.0, 2.0]], [2.0, 1.5]) == [5.5, 5.0]


def test_build_audit():
    audit = build_audit()
    assert audit.basis_shape == "2x2"
    assert audit.basis_rank == 2
    assert audit.basis_determinant == 3.0
    assert audit.reconstruction_error == 0.0
