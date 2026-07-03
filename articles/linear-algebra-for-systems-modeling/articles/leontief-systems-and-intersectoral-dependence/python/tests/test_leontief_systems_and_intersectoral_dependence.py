from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from leontief_systems_and_intersectoral_dependence.cli import leontief_audit


def test_leontief_audit_basic_fields():
    audit, A, L, shock = leontief_audit()
    assert audit.sectors == 4
    assert audit.productive_system_flag is True
    assert audit.spectral_radius < 1


def test_matrix_shapes():
    audit, A, L, shock = leontief_audit()
    assert len(A) == 4
    assert len(A[0]) == 4
    assert len(L) == 4
    assert len(shock) == 4


def test_diagnostics_positive():
    audit, A, L, shock = leontief_audit()
    assert audit.condition_number > 0
    assert audit.maximum_output_multiplier > 1
    assert audit.total_output_required > 0
