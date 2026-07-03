from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from principal_component_analysis.cli import pca_audit


def test_pca_audit_basic_fields():
    audit, scores, loadings = pca_audit()
    assert audit.observations == 8
    assert audit.variables == 5
    assert audit.retained_components == 2
    assert 0 < audit.cumulative_explained_variance <= 1


def test_scores_and_loadings_shapes():
    audit, scores, loadings = pca_audit()
    assert len(scores) == 8
    assert len(scores[0]) == 2
    assert len(loadings) == 5
    assert len(loadings[0]) == 2


def test_reconstruction_error_nonnegative():
    audit, scores, loadings = pca_audit()
    assert audit.relative_reconstruction_error >= 0
