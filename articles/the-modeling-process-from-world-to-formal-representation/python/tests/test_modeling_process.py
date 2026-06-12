from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from modeling_process.core import ReservoirScenario, simulate_reservoir, summarize_scenario, bounded_storage_update


def test_bounded_storage_update_respects_capacity():
    assert bounded_storage_update(95, 20, 1, 1, 100) == 100


def test_bounded_storage_update_respects_zero():
    assert bounded_storage_update(2, 0, 10, 1, 100) == 0


def test_reservoir_simulation_has_expected_rows():
    scenario = ReservoirScenario("test", 80, 100, 8, 6, 0.01, 0.015, 10)
    rows = simulate_reservoir(scenario)
    assert len(rows) == 11
    assert all(0 <= float(row["storage"]) <= 100 for row in rows)


def test_scenario_summary_contains_shortage_risk():
    scenario = ReservoirScenario("test", 20, 100, 1, 10, 0.01, 0.015, 10)
    rows = simulate_reservoir(scenario)
    summary = summarize_scenario(rows)
    assert "shortage_risk" in summary
    assert float(summary["shortage_risk"]) >= 0
