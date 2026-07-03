from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from latent_structure_and_signal_extraction.cli import latent_structure_audit


def test_latent_structure_audit_basic_fields():
    audit, scores, residuals = latent_structure_audit()
    assert audit.observations == 9
    assert audit.variables == 6
    assert audit.retained_rank == 2
    assert 0 < audit.retained_signal_ratio <= 1


def test_latent_scores_and_residuals_shapes():
    audit, scores, residuals = latent_structure_audit()
    assert len(scores) == 9
    assert len(scores[0]) == 2
    assert len(residuals) == 9


def test_residual_metrics_nonnegative():
    audit, scores, residuals = latent_structure_audit()
    assert audit.relative_reconstruction_error >= 0
    assert audit.maximum_observation_residual >= 0
