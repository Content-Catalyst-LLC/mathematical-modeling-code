from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from substitution_accumulation.core import audit_substitution, g, g_prime, grid, trapezoid_integral


def test_transformation_increases_on_interval():
    assert g_prime(1.0) > 0
    assert g(3.0) > g(1.0)


def test_grid_has_requested_endpoints():
    points = grid(1.0, 3.0, 4)
    assert points[0] == 1.0
    assert points[-1] == 3.0
    assert len(points) == 5


def test_trapezoid_rejects_nonincreasing_points():
    try:
        trapezoid_integral([1, 2, 3], [0, 1, 1])
    except ValueError as exc:
        assert "strictly increasing" in str(exc)
    else:
        raise AssertionError("Expected ValueError for repeated grid point")


def test_direct_and_transformed_integrals_match():
    record = audit_substitution(1.0, 3.0, 800)
    assert abs(record.residual) < 1e-3
