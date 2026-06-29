from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from matrix_differential_equations.cli import (
    build_audit,
    classify_continuous,
    eigenvalues_2x2_real,
    matvec,
)


def test_matvec():
    A = [[-0.28, 0.08], [0.12, -0.34]]
    x = [10.0, 4.0]
    dx = matvec(A, x)
    assert round(dx[0], 6) == -2.48
    assert round(dx[1], 6) == -0.16


def test_eigenvalues_real_parts():
    A = [[-0.28, 0.08], [0.12, -0.34]]
    eigenvalues = eigenvalues_2x2_real(A)
    assert round(eigenvalues[0], 6) == -0.2
    assert round(eigenvalues[1], 6) == -0.42


def test_classification_and_audit():
    assert classify_continuous(-0.2) == "asymptotically_stable_continuous_time"
    assert classify_continuous(0.0) == "boundary_or_marginal_continuous_time"
    assert classify_continuous(0.01) == "unstable_continuous_time"
    audit, trajectory, dt = build_audit()
    assert audit.system_name == "two_state_matrix_differential_equation_audit"
    assert audit.max_real_part == -0.2
    assert len(trajectory) == int(round(audit.time_horizon / dt)) + 1
