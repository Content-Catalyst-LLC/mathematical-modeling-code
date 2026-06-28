from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from inverse_recovery.cli import build_audit, determinant_3x3, inverse_3x3, matvec


def test_determinant_3x3():
    A = [[1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0]]
    assert determinant_3x3(A) == 2.0


def test_inverse_recovery_solution():
    A = [[1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0]]
    b = [100.0, 80.0, 90.0]
    recovered = matvec(inverse_3x3(A), b)
    assert [round(x, 6) for x in recovered] == [55.0, 45.0, 35.0]


def test_build_audit():
    audit = build_audit()
    assert audit.invertible is True
    assert audit.recovered_solution == "55.000000,45.000000,35.000000"
    assert audit.residual_norm == 0.0
