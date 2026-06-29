from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from stability_eigenvalues.cli import build_audit, classify_continuous, classify_discrete, determinant_2x2, eigenvalues_2x2


def test_eigenvalues_and_determinant():
    A = [[0.82, 0.12], [0.18, 0.76]]
    assert round(determinant_2x2(A), 6) == 0.6016
    eigenvalues = eigenvalues_2x2(A)
    assert round(eigenvalues[0], 6) == 0.94
    assert round(eigenvalues[1], 6) == 0.64


def test_stability_classifiers():
    assert classify_discrete((0.94, 0.64)) == "asymptotically_stable_discrete_time"
    assert classify_discrete((1.01, 0.64)) == "unstable_discrete_time"
    assert classify_continuous((-0.2, -1.1)) == "asymptotically_stable_continuous_time"
    assert classify_continuous((0.94, 0.64)) == "unstable_continuous_time"


def test_build_audit():
    audit = build_audit()
    assert audit.system_name == "two_mode_stability_audit"
    assert audit.spectral_radius == 0.94
    assert audit.discrete_time_classification == "asymptotically_stable_discrete_time"
