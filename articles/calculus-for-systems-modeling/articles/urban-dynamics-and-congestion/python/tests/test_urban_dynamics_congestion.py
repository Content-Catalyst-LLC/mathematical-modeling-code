from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from urban_dynamics_congestion.cli import (
    traffic_flow, critical_density, queue_step, simulate_queue, bpr_travel_time,
    accessibility, induced_demand_step, distributional_delay_burden,
    curb_occupancy_step, build_scenarios, build_diagnostics
)

def test_traffic_flow_positive():
    assert traffic_flow(35, 60, 140) > 0

def test_critical_density():
    assert critical_density(140) == 70

def test_queue_step_positive_for_over_capacity():
    assert queue_step(0, 2300, 2000, 0.01) > 0

def test_simulate_queue_over_capacity():
    q, delay = simulate_queue(2300, 2000, 1, 0.01)
    assert q > 0 and delay > 0

def test_bpr_travel_time():
    assert bpr_travel_time(20, 2300, 2000) > 20

def test_accessibility():
    assert accessibility([1000, 500], [10, 25], 0.08) > 0

def test_induced_demand_step():
    assert induced_demand_step(2300, 2600, 0.15, 1) > 2300

def test_distributional_delay_burden():
    assert distributional_delay_burden([10, 20], [1, 2]) == 50

def test_curb_occupancy_step():
    assert curb_occupancy_step(18, 10, 6, 20, 0.25) <= 20

def test_scenarios_present():
    names = {record.scenario_name for record in build_scenarios()}
    assert "over_capacity_bottleneck" in names

def test_diagnostics_present():
    assert len(build_diagnostics()) == 5
