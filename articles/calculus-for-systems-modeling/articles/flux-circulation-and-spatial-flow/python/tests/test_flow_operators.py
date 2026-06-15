from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from flow_operators.cli import audit_circle_flow, circle_points, dot, vector_field

def test_vector_field():
    assert vector_field(2.0, 3.0) == (-3.0, 2.0)

def test_dot():
    assert dot((1.0, 2.0), (3.0, 4.0)) == 11.0

def test_circle_points_closed():
    points = circle_points(1.0, 8)
    assert len(points) == 9

def test_audit_circulation_positive():
    record = audit_circle_flow(1.0, 64, "test")
    assert record.approximate_circulation > 0

def test_audit_flux_near_zero():
    record = audit_circle_flow(1.0, 64, "test")
    assert abs(record.approximate_flux) < 1e-9
