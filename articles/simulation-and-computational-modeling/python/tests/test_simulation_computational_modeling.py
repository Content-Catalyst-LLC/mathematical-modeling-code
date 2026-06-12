from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from simulation_computational_modeling.core import (
    Scenario,
    SimulationRecord,
    simulate,
    summarize,
    simulation_risk_score,
)


def test_simulate_outputs_all_steps():
    scenario = Scenario("test", 70.0, 0.18, 100.0, 6.0, 0.0, 0.0, 5, 2)
    rows = simulate(scenario, seed=1)
    assert rows[0]["step"] == 0
    assert rows[-1]["step"] == 5


def test_summarize_has_replications():
    scenario = Scenario("test", 70.0, 0.18, 100.0, 6.0, 0.0, 0.0, 5, 2)
    rows = simulate(scenario, seed=1) + simulate(scenario, seed=2)
    summary = summarize(rows)
    assert summary[0]["scenario"] == "test"
    assert summary[0]["replications"] == 2


def test_simulation_risk_score_positive():
    record = SimulationRecord(
        "update_rule",
        "update_rule",
        "R_next = R + growth - extraction - shock",
        "Stock changes through regeneration extraction and stochastic shocks.",
        "Does the update rule match the conceptual model?",
        "review",
    )
    assert simulation_risk_score(record) > 0
