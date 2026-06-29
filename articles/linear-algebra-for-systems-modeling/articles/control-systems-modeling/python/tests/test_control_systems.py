from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from control_systems.cli import build_audit, eigenvalues_2x2_real, matmul, rank_2x2, subtract


def test_closed_loop_matrix():
    A = [[0.10, 1.00], [0.00, 0.20]]
    B = [[0.00], [1.00]]
    K = [[0.50, 1.40]]
    A_closed = subtract(A, matmul(B, K))
    assert A_closed == [[0.10, 1.00], [-0.50, -1.20]]


def test_rank_diagnostics():
    assert rank_2x2([[0.0, 1.0], [1.0, 0.2]]) == 2
    assert rank_2x2([[1.0, 0.0], [0.1, 1.0]]) == 2


def test_eigenvalues_and_audit():
    closed = [[0.10, 1.00], [-0.50, -1.20]]
    eigs = eigenvalues_2x2_real(closed)
    assert round(eigs[0], 6) == -0.6
    assert round(eigs[1], 6) == -0.5
    audit = build_audit()
    assert audit.system_name == "two_state_control_system_audit"
    assert audit.controllability_rank == 2
    assert audit.observability_rank == 2
    assert audit.closed_loop_max_real_part < 0.0
