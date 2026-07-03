from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from economic_input_output_models.cli import input_output_audit


def test_input_output_audit_basic_fields():
    audit, A, L, shock = input_output_audit()
    assert audit.sectors == 4
    assert audit.maximum_output_multiplier > 1
    assert audit.total_baseline_output > 0


def test_matrix_shapes():
    audit, A, L, shock = input_output_audit()
    assert len(A) == 4
    assert len(A[0]) == 4
    assert len(L) == 4
    assert len(shock) == 4


def test_diagnostics_positive():
    audit, A, L, shock = input_output_audit()
    assert audit.condition_number > 0
    assert audit.total_shock_output_change > 0
