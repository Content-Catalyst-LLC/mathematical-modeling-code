from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from eigenstructure_modes.cli import build_audit, determinant_2x2, eigenvalues_2x2, trace_2x2


def test_trace_and_determinant():
    A = [[0.82, 0.12], [0.18, 0.76]]
    assert round(trace_2x2(A), 6) == 1.58
    assert round(determinant_2x2(A), 6) == 0.6016


def test_eigenvalues():
    A = [[0.82, 0.12], [0.18, 0.76]]
    values = eigenvalues_2x2(A)
    assert round(values[0], 6) == 0.94
    assert round(values[1], 6) == 0.64


def test_build_audit():
    audit = build_audit()
    assert audit.system_name == "two_sector_mode_audit"
    assert audit.spectral_radius == 0.94
    assert audit.stability_classification == "asymptotically_damped_discrete_time"
