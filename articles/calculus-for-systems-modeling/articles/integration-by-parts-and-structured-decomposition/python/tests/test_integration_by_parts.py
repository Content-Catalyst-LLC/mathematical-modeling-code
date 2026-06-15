from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from integration_by_parts.core import audit_integration_by_parts, grid, trapezoid_integral, u, u_prime


def test_grid_endpoint_count():
    points = grid(0.0, 4.0, 8)
    assert points[0] == 0.0
    assert points[-1] == 4.0
    assert len(points) == 9


def test_trapezoid_rejects_nonincreasing_points():
    try:
        trapezoid_integral([1, 2, 3], [0, 1, 1])
    except ValueError as exc:
        assert "strictly increasing" in str(exc)
    else:
        raise AssertionError("Expected ValueError for repeated grid point")


def test_u_prime_constant():
    assert u(2.0) == 3.0
    assert u_prime(2.0) == 1.0


def test_decomposition_residual_small():
    record = audit_integration_by_parts(0.0, 4.0, 1200)
    assert abs(record.decomposition_residual) < 1e-3
