from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from spatial_dynamics.cli import (
    diffusion_ratio,
    initialize_field,
    simulate_spatial_dynamics,
    transport_ratio,
    update_advection_diffusion,
)

def test_ratios():
    assert abs(diffusion_ratio(0.08, 0.2, 1.0) - 0.016) < 1e-12
    assert abs(transport_ratio(0.4, 0.2, 1.0) - 0.08) < 1e-12

def test_initialize_field():
    field = initialize_field(61)
    assert len(field) == 61
    assert field[30] == 1.0

def test_update_boundary():
    field = initialize_field(5)
    updated = update_advection_diffusion(field, 0.016, 0.08)
    assert updated[0] == 0.0
    assert updated[-1] == 0.0

def test_simulation_length():
    records = simulate_spatial_dynamics(61, 0.08, 0.4, 1.0, 0.2, 120)
    assert len(records) == 121
    assert records[0].diffusion_ratio == 0.016
