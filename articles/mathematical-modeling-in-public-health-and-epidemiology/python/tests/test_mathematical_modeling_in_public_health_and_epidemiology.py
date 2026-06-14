from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mathematical_modeling_in_public_health_and_epidemiology.core import (
    EpidemicScenario,
    PublicHealthModelRecord,
    build_public_health_model_review_card,
    epidemic_summary,
    evaluate_scenario,
    public_health_priority,
    simulate_sir,
)


def test_simulate_sir_length():
    scenario = EpidemicScenario("baseline", "Baseline", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045)
    trajectory = simulate_sir(scenario)
    assert len(trajectory) == 121
    assert trajectory[0]["infectious"] == 120.0


def test_evaluate_scenario_contains_capacity_margin():
    scenario = EpidemicScenario("baseline", "Baseline", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045)
    row = evaluate_scenario(scenario)
    assert "capacity_margin" in row
    assert row["r0_simple"] > 0


def test_epidemic_summary_count():
    rows = [
        evaluate_scenario(EpidemicScenario("a", "A", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045)),
        evaluate_scenario(EpidemicScenario("b", "B", 100000.0, 120.0, 4000.0, 0.18, 0.12, 120, 850.0, 0.045)),
    ]
    summary = epidemic_summary(rows)
    assert summary["scenario_count"] == 2
    assert "lowest_peak_hospital_demand_scenario" in summary


def test_public_health_priority_positive():
    record = PublicHealthModelRecord(
        "capacity_model",
        "health_system_planning",
        "capacity_review",
        "hospital_demand_model",
        "Could projected severe cases exceed healthcare capacity?",
        "review",
    )
    assert public_health_priority(record) > 0


def test_review_card_has_use_limit():
    register_rows = [
        {
            "key": "capacity_model",
            "domain": "health_system_planning",
            "model_role": "capacity_review",
            "model_family": "hospital_demand_model",
            "public_health_question": "Could projected severe cases exceed healthcare capacity?",
            "status": "review",
            "public_health_priority": 8.0,
        }
    ]
    scenario_rows = [
        evaluate_scenario(EpidemicScenario("a", "A", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045))
    ]
    card = build_public_health_model_review_card(register_rows, scenario_rows)
    assert "use_limit" in card
