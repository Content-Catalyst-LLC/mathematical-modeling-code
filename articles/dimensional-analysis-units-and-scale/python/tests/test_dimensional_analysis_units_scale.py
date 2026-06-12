from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from dimensional_analysis_units_scale.core import (
    ScaleScenario,
    UnitRecord,
    simulate_scale_scenario,
    summarize_scale_scenario,
    unit_risk_score,
)


def test_scale_scenario_runs_and_respects_domain():
    scenario = ScaleScenario("test", 80.0, 100.0, 8.0, 6.0, 0.015, 1.0, 20)
    rows = simulate_scale_scenario(scenario)
    assert len(rows) == 21
    assert all(bool(row["domain_valid"]) for row in rows)


def test_storage_fraction_is_bounded():
    scenario = ScaleScenario("test", 70.0, 75.0, 8.0, 6.0, 0.015, 1.0, 20)
    summary = summarize_scale_scenario(simulate_scale_scenario(scenario))
    assert 0 <= summary["min_storage_fraction"] <= 1
    assert 0 <= summary["max_storage_fraction"] <= 1


def test_unit_risk_score_positive():
    record = UnitRecord(
        "loss_rate",
        "rate",
        "1/day",
        "time^-1",
        "[0, 1]",
        "Does the loss-rate unit match the time step?",
        "review",
    )
    assert unit_risk_score(record) > 0
