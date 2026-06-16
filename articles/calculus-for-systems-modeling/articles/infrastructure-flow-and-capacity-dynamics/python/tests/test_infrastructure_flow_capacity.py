from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from infrastructure_flow_capacity.cli import (
    utilization,
    delay_function,
    simulate_queue,
    effective_capacity,
    bottleneck_stage,
    simulate_buffer,
    capacity_after_decay,
    service_resilience_ratio,
    build_scenarios,
    build_bottleneck_records,
)

def test_utilization_ratio():
    assert utilization(95, 100) == 0.95

def test_delay_increases_near_capacity():
    assert delay_function(0.95) > delay_function(0.75)

def test_queue_grows_when_over_capacity():
    q, u, d = simulate_queue(115, 100, 0.1, 10)
    assert q > 0
    assert u > 1

def test_effective_capacity_minimum():
    assert effective_capacity([140, 120, 90, 130]) == 90

def test_bottleneck_stage():
    assert bottleneck_stage([140, 120, 90, 130]) == 3

def test_buffer_saturation():
    final_buffer, saturated = simulate_buffer(120, 100, 10, 1, 2)
    assert saturated is True
    assert final_buffer == 10

def test_capacity_decay():
    assert capacity_after_decay(100, 0, 0.03, 1, 10) < 100

def test_resilience_ratio():
    assert service_resilience_ratio(80, 100) == 0.8

def test_scenarios_present():
    types = {record.system_type for record in build_scenarios()}
    assert {"queue_capacity", "network_bottleneck", "maintenance_capacity", "peak_load_capacity"}.issubset(types)

def test_bottleneck_records_present():
    assert len(build_bottleneck_records()) == 1
