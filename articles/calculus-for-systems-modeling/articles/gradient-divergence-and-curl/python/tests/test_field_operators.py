from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from field_operators.cli import audit_field_operators, curl_2d, divergence, gradient, scalar_field, vector_field

def test_scalar_field_origin():
    assert scalar_field(0.0, 0.0) == 0.0

def test_vector_field():
    assert vector_field(2.0, 3.0) == (-3.0, 2.0)

def test_gradient():
    assert gradient(2.0, -3.0) == (4.0, -6.0)

def test_divergence():
    assert divergence(0.0, 0.0) == 0.0

def test_curl():
    assert curl_2d(0.0, 0.0) == 2.0

def test_audit_positive_points():
    record = audit_field_operators(0.5, "test")
    assert record.point_count > 0
    assert record.maximum_gradient_magnitude > 0
