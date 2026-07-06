from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from case_study_linear_structure_ml_pipelines.cli import build_audit


def test_ml_pipeline_audit_structure():
    audit = build_audit()
    assert audit.observation_count == 10
    assert audit.feature_count == 4
    assert audit.train_count == 7
    assert audit.test_count == 3


def test_ml_pipeline_audit_metrics_are_plausible():
    audit = build_audit()
    assert audit.model_family == "ridge_regression_linear_baseline"
    assert audit.regularization_strength == 0.25
    assert 0.0 <= audit.test_rmse <= 0.2
    assert 0.0 <= audit.max_absolute_residual <= 0.25


def test_leakage_and_interpretation_warnings_attached():
    audit = build_audit()
    assert "training rows only" in audit.preprocessing_summary
    assert "leak" in audit.leakage_warning.lower()
    assert "not automatic causal explanations" in audit.interpretation_warning
