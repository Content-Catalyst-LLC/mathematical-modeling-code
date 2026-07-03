from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from optimization_gradients_and_matrix_structure.cli import optimization_audit


def test_optimization_audit_basic_fields():
    audit, weights, history, closed_form = optimization_audit()
    assert audit.observations == 10
    assert audit.features == 5
    assert audit.objective_final <= audit.objective_initial


def test_outputs_have_expected_lengths():
    audit, weights, history, closed_form = optimization_audit()
    assert len(weights) == 5
    assert len(closed_form) == 5
    assert len(history) > 2


def test_diagnostics_nonnegative():
    audit, weights, history, closed_form = optimization_audit()
    assert audit.gradient_norm_final >= 0
    assert audit.training_rmse >= 0
    assert audit.closed_form_gap_norm >= 0
