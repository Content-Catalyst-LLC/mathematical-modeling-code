from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from case_study_dimensionality_reduction.cli import build_audit


def test_dimensionality_reduction_audit_structure():
    audit = build_audit()
    assert audit.observation_count == 8
    assert audit.feature_count == 5
    assert audit.retained_components == 2


def test_explained_variance_and_reconstruction_are_plausible():
    audit = build_audit()
    assert 0.95 <= audit.cumulative_explained_variance <= 1.0
    assert 0.0 <= audit.reconstruction_rmse <= 0.5


def test_interpretation_warning_attached():
    audit = build_audit()
    assert "not automatically causal" in audit.interpretation_warning
    assert audit.dominant_component_feature in {"load", "temperature", "vibration", "pressure", "latency"}
