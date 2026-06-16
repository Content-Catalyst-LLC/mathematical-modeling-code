from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from carbon_accumulation_pathways.cli import (
    linear_decline_emissions,
    exponential_decline_emissions,
    overshoot_pathway,
    cumulative_sum,
    atmospheric_burden_impulse,
    carbon_budget_exhaustion_year,
    sink_feedback_adjusted_burden,
    build_scenarios,
    build_budget_records,
)

def test_linear_decline_reaches_zero():
    path = linear_decline_emissions(40, 30)
    assert path[0] == 40
    assert path[-1] == 0

def test_exponential_decline_positive():
    path = exponential_decline_emissions(40, 0.08, 30)
    assert all(v > 0 for v in path)

def test_overshoot_has_negative_values():
    path = overshoot_pathway(40, 30, 20, 5)
    assert min(path) < 0

def test_cumulative_sum_positive_for_linear():
    assert cumulative_sum(linear_decline_emissions(40, 30)) > 0

def test_impulse_burden_computable():
    assert atmospheric_burden_impulse(linear_decline_emissions(40, 30)) > 0

def test_budget_exhaustion_year():
    assert carbon_budget_exhaustion_year([100, 100, 100], 250) == 2

def test_sink_feedback_adjusted_burden_increases_with_temperature_proxy():
    path = linear_decline_emissions(40, 30)
    base = sink_feedback_adjusted_burden(path, 0.45, 0.0, 0.05)
    warm = sink_feedback_adjusted_burden(path, 0.45, 2.0, 0.05)
    assert warm > base

def test_scenarios_present():
    types = {record.pathway_type for record in build_scenarios()}
    assert {"constant", "linear_decline", "exponential_decline", "net_zero", "overshoot"}.issubset(types)

def test_budget_records_present():
    assert len(build_budget_records()) >= 1
