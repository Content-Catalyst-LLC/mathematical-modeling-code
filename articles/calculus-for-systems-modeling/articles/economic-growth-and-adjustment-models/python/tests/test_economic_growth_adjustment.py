from pathlib import Path
import sys
import math
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from economic_growth_adjustment.cli import (
    exponential_output,
    doubling_time,
    logistic_output,
    simulate_capital,
    simulate_adjustment,
    cobb_douglas,
    growth_accounting,
    build_scenarios,
    build_growth_records,
)

def test_exponential_growth_increases():
    assert exponential_output(100, 0.025, 40) > 100

def test_doubling_time_positive():
    assert doubling_time(0.025) > 0

def test_logistic_under_capacity():
    value = logistic_output(100, 0.06, 240, 0.1, 400)
    assert value <= 240.0001

def test_capital_simulation_nonnegative():
    output, capital = simulate_capital(300, 100, 0.22, 0.05, 0.012, 0.1, 20)
    assert output > 0
    assert capital >= 0

def test_adjustment_moves_toward_target():
    x = simulate_adjustment(100, 160, 0.35, 0, 1000, 0.1, 100)
    assert x > 100

def test_cobb_douglas_positive():
    assert cobb_douglas(1.2, 450, 180, 0.35) > 0

def test_growth_accounting():
    assert math.isclose(growth_accounting(0.01, 0.03, 0.02, 0.35), 0.01 + 0.35*0.03 + 0.65*0.02)

def test_scenarios_present():
    types = {record.model_type for record in build_scenarios()}
    assert {"exponential_growth", "logistic_constraint", "capital_stock_flow", "target_adjustment", "cobb_douglas"}.issubset(types)

def test_growth_records_present():
    assert len(build_growth_records()) == 3
