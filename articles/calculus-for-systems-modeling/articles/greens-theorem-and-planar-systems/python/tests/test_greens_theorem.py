from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from greens_theorem.cli import (
    audit_greens_theorem,
    boundary_circulation_square,
    boundary_flux_square,
    interior_integral,
    planar_curl,
    planar_divergence,
)

def test_boundary_circulation_square():
    assert abs(boundary_circulation_square(16) - 8.0) < 1e-9

def test_boundary_flux_square():
    assert abs(boundary_flux_square(16) - 8.0) < 1e-9

def test_interior_curl():
    assert abs(interior_integral(0.5, planar_curl) - 8.0) < 1e-9

def test_interior_divergence():
    assert abs(interior_integral(0.5, planar_divergence) - 8.0) < 1e-9

def test_audit_gaps():
    record = audit_greens_theorem(32, 0.25, "test")
    assert record.circulation_gap < 1e-9
    assert record.flux_gap < 1e-9
