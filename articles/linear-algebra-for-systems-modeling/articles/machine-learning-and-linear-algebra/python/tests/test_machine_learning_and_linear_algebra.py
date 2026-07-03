from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from machine_learning_and_linear_algebra.cli import ml_linear_algebra_audit


def test_ml_linear_algebra_audit_basic_fields():
    audit, weights, residuals, singular_values = ml_linear_algebra_audit()
    assert audit.observations == 10
    assert audit.features == 5
    assert audit.numerical_rank > 0


def test_outputs_have_expected_lengths():
    audit, weights, residuals, singular_values = ml_linear_algebra_audit()
    assert len(weights) == 5
    assert len(residuals) == 10
    assert len(singular_values) == 5


def test_diagnostics_nonnegative():
    audit, weights, residuals, singular_values = ml_linear_algebra_audit()
    assert audit.training_rmse >= 0
    assert audit.maximum_absolute_residual >= 0
    assert audit.first_two_component_energy > 0
