from pathlib import Path
import math
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from stokes_theorem.cli import (
    audit_stokes,
    boundary_circulation_circle,
    curl_field,
    surface_curl_flux_disk,
    vector_field,
)

def test_vector_field():
    assert vector_field(2.0, 3.0) == (-3.0, 2.0, 0.0)

def test_curl_field():
    assert curl_field(1.0, 2.0) == (0.0, 0.0, 2.0)

def test_surface_curl_flux_disk():
    assert abs(surface_curl_flux_disk(1.0, 8) - 2.0*math.pi) < 1e-9

def test_boundary_circulation_converges():
    assert abs(boundary_circulation_circle(1.0, 2048) - 2.0*math.pi) < 1e-3

def test_audit_gap_small_for_fine():
    record = audit_stokes(1.0, 4096, 128, "test")
    assert record.absolute_gap < 1e-4
