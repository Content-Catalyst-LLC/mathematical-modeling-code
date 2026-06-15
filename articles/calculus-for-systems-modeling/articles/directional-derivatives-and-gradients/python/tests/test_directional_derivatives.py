from pathlib import Path
import sys
import math

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from directional_derivatives.cli import audit_direction, directional_derivative, feasible_direction, gradient, normalize

def test_gradient():
    assert gradient(4.0, 3.0) == (4.5, 4.0)

def test_normalize():
    ux, uy = normalize(3.0, 4.0)
    assert abs(math.sqrt(ux*ux + uy*uy) - 1.0) < 1e-12

def test_directional_derivative():
    ux, uy = normalize(1.0, 1.0)
    assert abs(directional_derivative(4.0, 3.0, ux, uy) - (8.5 / math.sqrt(2))) < 1e-12

def test_feasible_direction():
    ux, uy = normalize(1.0, 1.0)
    assert not feasible_direction(8.0, 1.0, ux, uy, 1.0)

def test_audit_error_nonnegative():
    record = audit_direction(4.0, 3.0, 1.0, 1.0, 0.25)
    assert record.absolute_error >= 0
