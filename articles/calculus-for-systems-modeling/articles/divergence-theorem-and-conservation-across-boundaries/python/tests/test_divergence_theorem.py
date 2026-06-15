from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from divergence_theorem.cli import (
    audit_divergence_theorem,
    boundary_flux_unit_cube,
    divergence,
    vector_field,
    volume_divergence_unit_cube,
)

def test_vector_field():
    assert vector_field(1.0, 2.0, 3.0) == (1.0, 2.0, 3.0)

def test_divergence():
    assert divergence(1.0, 2.0, 3.0) == 3.0

def test_boundary_flux_unit_cube():
    assert abs(boundary_flux_unit_cube(4) - 3.0) < 1e-9

def test_volume_divergence_unit_cube():
    assert abs(volume_divergence_unit_cube(4) - 3.0) < 1e-9

def test_audit_gap():
    record = audit_divergence_theorem(16, "test")
    assert record.absolute_gap < 1e-9
