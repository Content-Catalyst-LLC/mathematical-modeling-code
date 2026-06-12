from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from spatial_models_geometric_representation.core import (
    Location,
    SpatialRecord,
    accessibility_rows,
    euclidean_distance,
    spatial_risk_score,
)


def test_euclidean_distance():
    a = Location("a", "demand", 0.0, 0.0, 1.0)
    b = Location("b", "service", 3.0, 4.0, 1.0)
    assert euclidean_distance(a, b) == 5.0


def test_accessibility_rows():
    locations = [
        Location("a", "demand", 0.0, 0.0, 100.0),
        Location("clinic", "service", 1.0, 0.0, 50.0),
    ]
    rows = accessibility_rows(locations)
    assert rows[0]["nearest_service"] == "clinic"
    assert rows[0]["accessibility_score"] > 0


def test_spatial_risk_score_positive():
    record = SpatialRecord(
        "euclidean_distance",
        "distance_metric",
        "sqrt((x_i-x_j)^2+(y_i-y_j)^2)",
        "Straight-line distance is used as a transparent baseline.",
        "Should network distance replace straight-line distance?",
        "review",
    )
    assert spatial_risk_score(record) > 0
