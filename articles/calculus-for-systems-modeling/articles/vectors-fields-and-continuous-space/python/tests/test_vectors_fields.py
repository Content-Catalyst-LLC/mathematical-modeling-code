from pathlib import Path
import sys
import math

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from vectors_fields.cli import audit_field, scalar_field, vector_field, vector_magnitude

def test_vector_magnitude():
    assert vector_magnitude(3.0, 4.0) == 5.0

def test_scalar_field_origin():
    assert scalar_field(0.0, 0.0) == 20.0

def test_vector_field_rotation():
    assert vector_field(2.0, 3.0) == (-3.0, 2.0)

def test_audit_positive_points():
    record = audit_field(1.0, "test")
    assert record.point_count > 0

def test_vector_magnitude_maximum_positive():
    record = audit_field(1.0, "test")
    assert record.vector_magnitude_maximum > 0
