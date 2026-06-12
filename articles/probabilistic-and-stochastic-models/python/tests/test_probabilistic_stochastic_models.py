from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from probabilistic_stochastic_models.core import (
    ProbabilityModelRecord,
    RiskScenario,
    probability_risk_score,
    quantile,
    simulate_risk,
)


def test_quantile_selects_ordered_value():
    values = [10.0, 0.0, 5.0, 20.0]
    assert quantile(values, 0.50) in {5.0, 10.0}


def test_simulation_runs_and_reports_probability():
    scenario = RiskScenario("test", 4.5, 0.25, 95.0, 8.0, 5.0, 250, 101)
    rows, summary = simulate_risk(scenario)
    assert len(rows) == 250
    assert 0.0 <= summary["shortage_probability"] <= 1.0
    assert "shortage_q95" in summary


def test_probability_risk_score_positive():
    record = ProbabilityModelRecord(
        "tail_risk",
        "risk_measure",
        "quantile(Q, 0.95)",
        "Tail shortage risk.",
        "Is tail risk used alongside expected shortage?",
        "active",
    )
    assert probability_risk_score(record) > 0
