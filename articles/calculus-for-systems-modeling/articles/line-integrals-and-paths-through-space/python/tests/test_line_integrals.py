from pathlib import Path
import sys
import math

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from line_integrals.cli import audit_line_integral, distance, dot, path, scalar_field, vector_field

def test_path_origin():
    assert path(0.0) == (0.0, 0.0)

def test_scalar_field_minimum_origin():
    assert scalar_field(0.0, 0.0) == 1.0

def test_vector_field_origin():
    assert vector_field(0.0, 0.0) == (1.0, 0.0)

def test_distance_3_4_5():
    assert distance((0.0, 0.0), (3.0, 4.0)) == 5.0

def test_dot_product():
    assert dot((1.0, 2.0), (3.0, 4.0)) == 11.0

def test_audit_positive_values():
    record = audit_line_integral(0.5, "test")
    assert record.path_length > 0
    assert record.scalar_line_integral > 0
