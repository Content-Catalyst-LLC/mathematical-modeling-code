from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from diagonalization_modes.cli import build_audit, inverse_2x2, matmul, frobenius, subtract


def test_inverse_2x2_identity_check():
    P = [[1.0, 1.0], [1.0, -2.0]]
    Pinv = inverse_2x2(P)
    I = matmul(P, Pinv)
    assert round(I[0][0], 6) == 1.0
    assert round(I[0][1], 6) == 0.0
    assert round(I[1][0], 6) == 0.0
    assert round(I[1][1], 6) == 1.0


def test_audit():
    audit = build_audit()
    assert audit.system_name == "two_mode_diagonalization_audit"
    assert audit.spectral_radius == 0.92
    assert audit.stability_classification == "all_modes_decay_discrete_time"


def test_frobenius_zero():
    A = [[1.0, 2.0], [3.0, 4.0]]
    assert frobenius(subtract(A, A)) == 0.0
