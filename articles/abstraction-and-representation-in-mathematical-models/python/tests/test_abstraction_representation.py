from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from abstraction_representation.core import (
    RepresentationChoice,
    StockFlowScenario,
    bounded_update,
    representation_risk_score,
    simulate_stock_flow,
    summarize_stock_flow,
)


def test_bounded_update_respects_capacity():
    assert bounded_update(95.0, 20.0, 1.0, 1.0, 100.0) == 100.0


def test_bounded_update_respects_zero():
    assert bounded_update(2.0, 0.0, 10.0, 1.0, 100.0) == 0.0


def test_simulation_stays_within_bounds():
    scenario = StockFlowScenario("test", 80.0, 100.0, 8.0, 6.0, 0.015, 20)
    rows = simulate_stock_flow(scenario)
    assert len(rows) == 21
    assert all(0 <= float(row["stock"]) <= 100 for row in rows)


def test_summary_contains_total_shortage():
    scenario = StockFlowScenario("stress", 10.0, 100.0, 1.0, 10.0, 0.02, 10)
    rows = simulate_stock_flow(scenario)
    summary = summarize_stock_flow(rows)
    assert "total_shortage" in summary


def test_representation_risk_score_is_positive():
    choice = RepresentationChoice(
        "Stored resource",
        "Aggregate stock",
        "S_t",
        "Accumulation",
        "Spatial distribution quality access",
        "Does this matter?",
        "review",
    )
    assert representation_risk_score(choice) > 0
