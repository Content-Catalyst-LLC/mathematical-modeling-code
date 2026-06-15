from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from surface_integrals.cli import audit_surface, dot, graph_normal_area_vector, height, scalar_field, vector_norm

def test_height_origin():
    assert height(0.0, 0.0) == 0.0

def test_scalar_field_origin():
    assert scalar_field(0.0, 0.0, 0.0) == 1.0

def test_dot_product():
    assert dot((1.0, 2.0, 3.0), (4.0, 5.0, 6.0)) == 32.0

def test_normal_area_vector_origin():
    assert graph_normal_area_vector(0.0, 0.0, 1.0, 1.0) == (-0.0, -0.0, 1.0)

def test_norm_positive():
    assert vector_norm((0.0, 0.0, 2.0)) == 2.0

def test_audit_positive_area():
    record = audit_surface(0.5, "test")
    assert record.approximate_surface_area > 0
    assert record.scalar_surface_integral > 0
