from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from dimensionality_reduction_techniques.cli import pca_reduction_audit


def test_dimensionality_reduction_audit_basic_fields():
    audit, coords = pca_reduction_audit()
    assert audit.observations == 8
    assert audit.original_dimensions == 6
    assert audit.reduced_dimensions == 2
    assert 0 < audit.explained_variance_retained <= 1


def test_reduced_coordinates_shape():
    audit, coords = pca_reduction_audit()
    assert len(coords) == 8
    assert len(coords[0]) == 2


def test_error_metrics_nonnegative():
    audit, coords = pca_reduction_audit()
    assert audit.relative_reconstruction_error >= 0
    assert audit.mean_pairwise_distance_distortion >= 0
