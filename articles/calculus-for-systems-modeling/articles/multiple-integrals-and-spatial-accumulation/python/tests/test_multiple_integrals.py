from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from multiple_integrals.cli import compute_spatial_accumulation, exposure_field, in_region, population_density

def test_exposure_field():
    assert exposure_field(0.0, 0.0) == 10.0

def test_population_density_positive():
    assert population_density(0.0, 0.0) == 100.0

def test_region_center_inside():
    assert in_region(0.0, 0.0) is True

def test_region_corner_outside():
    assert in_region(3.0, 3.0) is False

def test_spatial_accumulation_positive():
    record = compute_spatial_accumulation(1.0, "test")
    assert record.cells_in_region > 0
    assert record.total_density_accumulation > 0
    assert record.population_weighted_average_exposure > 0
