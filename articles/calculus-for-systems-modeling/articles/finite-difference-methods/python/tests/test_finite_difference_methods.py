from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from finite_difference_methods.cli import (
    central_difference,
    diffusion_ratio,
    forward_difference,
    initialize_field,
    second_central_difference,
    simulate_finite_difference_diffusion,
)

def test_difference_formulas():
    assert abs(forward_difference(1.0, 1.2, 0.1) - 2.0) < 1e-12
    assert abs(central_difference(1.0, 1.2, 0.1) - 1.0) < 1e-12
    assert abs(second_central_difference(1.0, 1.2, 1.4, 0.1)) < 1e-10

def test_diffusion_ratio():
    assert abs(diffusion_ratio(0.08, 0.2, 1.0) - 0.016) < 1e-12

def test_simulation_length():
    records = simulate_finite_difference_diffusion(61, 0.08, 1.0, 0.2, 120)
    assert len(records) == 121
    assert records[0].stability_status == "stable_for_basic_explicit_1d_diffusion"

def test_initialize_field():
    field = initialize_field(7)
    assert field[3] == 1.0
