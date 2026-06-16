from pathlib import Path
import sys
import math
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from continuous_time_epidemiology.cli import (
    basic_reproduction_number,
    effective_reproduction_number,
    doubling_time,
    herd_immunity_threshold,
    force_of_infection,
    incidence,
    simulate_sir,
    simulate_seir,
    vaccination_waning_step,
    build_scenarios,
    build_threshold_records,
)

def test_basic_reproduction_number():
    assert basic_reproduction_number(0.32, 0.10) == 3.1999999999999997

def test_effective_reproduction_number():
    assert effective_reproduction_number(0.32, 0.10, 50000, 100000) < basic_reproduction_number(0.32, 0.10)

def test_doubling_time_positive():
    assert doubling_time(0.22) > 0

def test_herd_threshold_between_zero_and_one():
    h = herd_immunity_threshold(3.2)
    assert 0 < h < 1

def test_force_of_infection_positive():
    assert force_of_infection(0.32, 100, 100000) > 0

def test_incidence_positive():
    assert incidence(0.32, 99900, 100, 100000) > 0

def test_sir_simulation_nonnegative():
    s, i, r, peak = simulate_sir(100000, 99900, 100, 0, 0.32, 0.10, 0.1, 10)
    assert s >= 0 and i >= 0 and r >= 0 and peak >= 100

def test_seir_simulation_nonnegative():
    s, e, i, r, peak = simulate_seir(100000, 99850, 50, 100, 0, 0.32, 0.20, 0.10, 0.1, 10)
    assert s >= 0 and e >= 0 and i >= 0 and r >= 0

def test_vaccination_waning_step():
    s, v = vaccination_waning_step(90000, 10000, 0.005, 0.001, 1)
    assert s < 90000 and v > 10000

def test_scenarios_present():
    types = {record.model_type for record in build_scenarios()}
    assert {"SIR", "SEIR", "SIR_vaccination"}.issubset(types)

def test_thresholds_present():
    assert len(build_threshold_records()) == 1
