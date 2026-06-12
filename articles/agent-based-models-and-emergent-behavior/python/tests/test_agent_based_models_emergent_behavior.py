from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from agent_based_models_emergent_behavior.core import (
    AgentRuleRecord,
    SimulationScenario,
    neighbors,
    rule_risk_score,
    run_replication,
    summarize_runs,
)


def test_neighbors_wrap_on_ring():
    assert neighbors(0, 10) == [8, 9, 1, 2]


def test_replication_outputs_all_steps():
    scenario = SimulationScenario("test", 20, 3, 0.1, 0.4, 5, 2)
    rows = run_replication(scenario, seed=1)
    assert rows[0]["step"] == 0
    assert rows[-1]["step"] == 5


def test_summary_has_scenario():
    scenario = SimulationScenario("test", 20, 3, 0.1, 0.4, 5, 2)
    rows = run_replication(scenario, seed=1) + run_replication(scenario, seed=2)
    summary = summarize_runs(rows)
    assert summary[0]["scenario"] == "test"
    assert summary[0]["replications"] == 2


def test_rule_risk_score_positive():
    record = AgentRuleRecord(
        "threshold_rule",
        "behavior_rule",
        "adopt if adopted_neighbors_share >= threshold",
        "Agents adopt when local exposure exceeds threshold.",
        "Are thresholds empirically grounded?",
        "review",
    )
    assert rule_risk_score(record) > 0
