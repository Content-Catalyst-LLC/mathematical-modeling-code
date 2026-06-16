from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from energy_balance_models.cli import (
    equilibrium_temperature, adjustment_time, one_layer_response, two_layer_response,
    absorbed_solar, linear_outgoing_radiation, surface_energy_partition,
    building_temperature_step, build_scenarios, build_diagnostics
)

def test_equilibrium_temperature(): assert equilibrium_temperature(3.7, 1.2) > 0
def test_adjustment_time(): assert adjustment_time(10, 1.2) > 0
def test_one_layer_response_positive(): assert one_layer_response(3.7, 1.2, 10, 0, 0.1, 100) > 0
def test_two_layer_response_tuple():
    upper, deep = two_layer_response(3.7, 1.2, 0.7, 10, 100, 0, 0, 0.1, 100)
    assert upper >= 0 and deep >= 0
def test_absorbed_solar(): assert absorbed_solar(1361, 0.30) > 0
def test_linear_outgoing_radiation(): assert linear_outgoing_radiation(200, 2, 10) == 220
def test_surface_partition(): assert surface_energy_partition(500, 120, 300, 40) == 40
def test_building_step(): assert building_temperature_step(20, 1000, 300, 150, 80, 420, 1) > 20
def test_scenarios_present():
    assert {"one_layer", "two_layer"}.issubset({r.model_type for r in build_scenarios()})
def test_diagnostics_present(): assert len(build_diagnostics()) == 3
