from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from pde_intro.cli import diffusion_step, initialize_field, simulate_diffusion, stability_ratio

def test_stability_ratio():
    assert abs(stability_ratio(0.1, 0.25, 1.0) - 0.025) < 1e-12

def test_initialize_field():
    field = initialize_field(51)
    assert len(field) == 51
    assert field[25] == 1.0

def test_diffusion_step_boundary():
    field = initialize_field(5)
    updated = diffusion_step(field, 0.1)
    assert updated[0] == 0.0
    assert updated[-1] == 0.0
    assert updated[2] < 1.0

def test_simulation_length():
    records = simulate_diffusion(51, 0.1, 1.0, 0.25, 100)
    assert len(records) == 101
    assert records[0].stability_ratio == 0.025
