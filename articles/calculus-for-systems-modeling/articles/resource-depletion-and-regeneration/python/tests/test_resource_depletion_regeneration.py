from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from resource_depletion_regeneration.cli import (
    logistic_regeneration,
    threshold_regeneration,
    maximum_sustainable_yield,
    simulate_resource,
    simulate_nonrenewable,
    efficiency_adjusted_extraction,
    build_scenarios,
    build_yield_records,
)

def test_logistic_regeneration_positive_midstock():
    assert logistic_regeneration(500, 0.18, 1000) > 0

def test_logistic_regeneration_zero_at_capacity():
    assert abs(logistic_regeneration(1000, 0.18, 1000)) < 1e-9

def test_threshold_regeneration_negative_below_threshold():
    assert threshold_regeneration(100, 0.18, 1000, 180) < 0

def test_msy_formula():
    assert maximum_sustainable_yield(0.18, 1000) == 45.0

def test_simulate_resource_nonnegative():
    stock, extraction = simulate_resource(600, lambda s: logistic_regeneration(s, 0.18, 1000), 35, 0.1, 10)
    assert stock >= 0
    assert extraction >= 0

def test_nonrenewable_drawdown():
    stock, extraction = simulate_nonrenewable(100, 30, 1, 10)
    assert stock == 0
    assert extraction == 100

def test_efficiency_with_rebound():
    assert efficiency_adjusted_extraction(100, 0.2, 0.5) == 90

def test_scenarios_present():
    types = {record.resource_type for record in build_scenarios()}
    assert {"renewable_logistic", "threshold_regeneration", "nonrenewable", "efficiency_rebound"}.issubset(types)

def test_yield_records_present():
    assert len(build_yield_records()) == 1
