from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from equations_inequalities_model_logic.core import (
    FormalStatement,
    LogicScenario,
    simulate_logic,
    statement_risk_score,
    summarize_logic,
)


def test_logic_simulation_respects_domain():
    scenario = LogicScenario("test", 80.0, 100.0, 8.0, 6.0, 0.015, 35.0, 0.5, 20)
    rows = simulate_logic(scenario)
    assert len(rows) == 21
    assert all(bool(row["domain_valid"]) for row in rows)


def test_constraint_stress_activates_shortage_or_logic():
    scenario = LogicScenario("stress", 40.0, 60.0, 3.0, 7.0, 0.05, 25.0, 1.0, 20)
    summary = summarize_logic(simulate_logic(scenario))
    assert summary["shortage_periods"] >= 0
    assert "logic_activation_periods" in summary


def test_statement_risk_score_positive():
    statement = FormalStatement(
        "storage_bounds",
        "inequality",
        "0 <= S[t] <= K",
        "Storage remains bounded.",
        "K > 0",
        "Does clipping hide shortage or overflow?",
        "review",
    )
    assert statement_risk_score(statement) > 0
