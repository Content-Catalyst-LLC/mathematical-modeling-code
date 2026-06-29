from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from linear_dynamics.cli import build_audit, classify_discrete, eigenvalues_2x2, matvec, simulate


def test_matvec():
    A = [[0.82, 0.12], [0.18, 0.76]]
    x = [10.0, 4.0]
    y = matvec(A, x)
    assert round(y[0], 6) == 8.68
    assert round(y[1], 6) == 4.84


def test_eigenvalues():
    A = [[0.82, 0.12], [0.18, 0.76]]
    eigenvalues = eigenvalues_2x2(A)
    assert round(eigenvalues[0], 6) == 0.94
    assert round(eigenvalues[1], 6) == 0.64


def test_classification_and_audit():
    assert classify_discrete(0.94) == "asymptotically_stable_discrete_time"
    assert classify_discrete(1.0) == "boundary_or_marginal_discrete_time"
    assert classify_discrete(1.01) == "unstable_discrete_time"
    audit, trajectory = build_audit()
    assert audit.system_name == "two_state_linear_dynamics_audit"
    assert audit.spectral_radius == 0.94
    assert len(trajectory) == audit.horizon + 1
