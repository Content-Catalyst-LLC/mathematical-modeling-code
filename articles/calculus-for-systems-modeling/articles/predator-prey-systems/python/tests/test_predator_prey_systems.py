from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from predator_prey_systems.cli import (
    build_scenarios,
    build_nullcline_records,
    build_stability_records,
    lotka_volterra_derivative,
    simulate_pair,
    stability_status,
)

def test_scenarios_include_advanced_models():
    model_types = {record.model_type for record in build_scenarios()}
    assert {"lotka_volterra", "logistic_prey", "saturating_predation", "harvesting", "stochastic"}.issubset(model_types)

def test_nullcline_records_present():
    names = {record.nullcline_name for record in build_nullcline_records()}
    assert "prey_nullcline" in names
    assert "predator_nullcline" in names

def test_stability_records_present():
    assert len(build_stability_records()) >= 1

def test_simulation_nonnegative():
    derivative = lotka_volterra_derivative(0.6, 0.02, 0.5, 0.01)
    x, y = simulate_pair(40.0, 9.0, derivative, 0.02, 50)
    assert x >= 0 and y >= 0

def test_stability_status_center():
    assert stability_status(0.0, 0.3) == "center_or_neutral_linearization"
