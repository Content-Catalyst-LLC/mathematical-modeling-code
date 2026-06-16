from pathlib import Path
import sys
import math
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from financial_dynamics_compounding.cli import (
    continuous_future_value,
    continuous_present_value,
    discrete_compound_value,
    continuous_equivalent_rate,
    real_rate,
    net_present_value,
    simulate_debt,
    geometric_mean_return,
    leverage_ratio,
    rate_sensitivity,
    build_scenarios,
    build_rate_records,
)

def test_continuous_future_value_increases():
    assert continuous_future_value(1000, 0.05, 30) > 1000

def test_present_value_less_than_future_value():
    assert continuous_present_value(5000, 0.05, 30) < 5000

def test_discrete_compound_value():
    assert discrete_compound_value(1000, 0.05, 12, 30) > 1000

def test_continuous_equivalent_rate():
    assert math.isclose(continuous_equivalent_rate(0.05), math.log(1.05))

def test_real_rate():
    assert real_rate(0.06, 0.025) < 0.06

def test_npv_returns_number():
    assert isinstance(net_present_value([(0, -1000), (1, 1100)], 0.05), float)

def test_debt_nonnegative():
    assert simulate_debt(2000, 0.07, 120, 0.1, 10) >= 0

def test_geometric_mean_return():
    assert geometric_mean_return([0.1, -0.1]) < 0.01

def test_leverage_ratio():
    assert leverage_ratio(5000, 1000) == 5

def test_rate_sensitivity_positive():
    assert rate_sensitivity(1000, 0.05, 30) > 0

def test_scenarios_present():
    types = {record.model_type for record in build_scenarios()}
    assert {"future_value", "discrete_compounding", "present_value", "net_present_value", "debt_balance", "inflation_adjusted_growth", "portfolio_compounding", "leverage_ratio", "sensitivity"}.issubset(types)

def test_rate_records_present():
    assert len(build_rate_records()) == 2
