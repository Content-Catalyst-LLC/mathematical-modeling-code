from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))
from modeling_population_dynamics.cli import exponential, logistic, simulate, allee_derivative, harvest_derivative, stochastic_logistic, two_patch, leslie_project, diffusion_step, calibration_grid, scenarios

def test_logistic_bounded():
    assert 0 < logistic(100, 0.08, 1000, 40) < 1000

def test_allee_can_decline_below_threshold():
    assert simulate(50, allee_derivative(0.08, 1000, 75), 0.1, 50) < 50

def test_harvesting_changes_outcome():
    assert simulate(100, harvest_derivative(0.08, 1000, 12), 0.1, 400) < logistic(100, 0.08, 1000, 40)

def test_stochastic_nonnegative():
    assert stochastic_logistic(100, 0.08, 1000, 0.12, 0.1, 20) >= 0

def test_two_patch_total_positive():
    n1, n2 = two_patch(100, 400, 0.08, 1000, 0.04, 0.1, 20)
    assert n1 + n2 > 0

def test_leslie_projection_positive():
    assert sum(leslie_project([80, 40, 20], [[0,1.2,1.8],[.55,0,0],[0,.65,.30]], 5)) > 0

def test_diffusion_nonnegative():
    assert min(diffusion_step([20, 40, 300, 40, 20], 0.03, 0.1, 1.0)) >= 0

def test_calibration_grid_returns_candidates():
    assert len(calibration_grid([(0,100),(10,180)], 100)) > 0

def test_scenarios_include_advanced():
    model_types = {row.model_type for row in scenarios()}
    assert {"allee_effect", "harvesting", "stochastic", "metapopulation", "leslie_matrix"}.issubset(model_types)
