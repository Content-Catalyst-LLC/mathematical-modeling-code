from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from climate_feedback_models.cli import (
    co2_forcing,
    one_box_temperature,
    simulate_two_box,
    carbon_feedback_forcing,
    equilibrium_sensitivity_lambda,
    build_scenarios,
    build_parameter_records,
)

def test_co2_forcing_positive_for_doubling():
    assert co2_forcing(560, 280) > 0

def test_one_box_approaches_equilibrium():
    value = one_box_temperature(3.7, 1.2, 8.0, 500)
    assert abs(value - (3.7/1.2)) < 0.01

def test_two_box_outputs_positive_temperatures():
    surface, deep = simulate_two_box(3.7, 1.2, 8.0, 100.0, 0.7, 0.25, 80)
    assert surface >= 0
    assert deep >= 0

def test_carbon_feedback_increases_forcing_when_positive():
    assert carbon_feedback_forcing(3.7, 2.0, 0.15) > 3.7

def test_equilibrium_sensitivity_negative_under_restoring_convention():
    assert equilibrium_sensitivity_lambda(3.7, 1.2) < 0

def test_scenarios_present():
    model_types = {record.model_type for record in build_scenarios()}
    assert {"one_box_energy_balance", "two_box_energy_balance", "carbon_feedback", "feedback_sweep", "threshold_feedback"}.issubset(model_types)

def test_parameters_present():
    names = {record.parameter_name for record in build_parameter_records()}
    assert {"F", "lambda", "C", "kappa", "beta_carbon"}.issubset(names)
