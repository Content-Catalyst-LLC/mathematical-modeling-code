from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mathematical_modeling_in_ecology_and_sustainability.core import (
    EcologyModelRecord,
    ResourceScenario,
    build_sustainability_review_card,
    ecology_priority,
    evaluate_scenario,
    simulate_resource,
    sustainability_summary,
)


def test_simulate_resource_length():
    scenario = ResourceScenario("baseline", "Baseline", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0)
    trajectory = simulate_resource(scenario)
    assert len(trajectory) == 26
    assert trajectory[0]["stock"] == 420.0


def test_evaluate_scenario_contains_margin():
    scenario = ResourceScenario("baseline", "Baseline", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0)
    row = evaluate_scenario(scenario)
    assert "minimum_resilience_margin" in row
    assert "review_class" in row


def test_sustainability_summary_count():
    rows = [
        evaluate_scenario(ResourceScenario("a", "A", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0)),
        evaluate_scenario(ResourceScenario("b", "B", 420.0, 0.24, 800.0, 64.0, 0.04, 25, 250.0)),
    ]
    summary = sustainability_summary(rows)
    assert summary["scenario_count"] == 2
    assert "best_resilience_scenario" in summary


def test_ecology_priority_positive():
    record = EcologyModelRecord(
        "resilience_model",
        "ecosystem_resilience",
        "threshold_review",
        "resilience_margin_model",
        "How close is the system to a minimum ecological threshold?",
        "review",
    )
    assert ecology_priority(record) > 0


def test_review_card_has_use_limit():
    register_rows = [
        {
            "key": "resilience_model",
            "domain": "ecosystem_resilience",
            "model_role": "threshold_review",
            "model_family": "resilience_margin_model",
            "sustainability_question": "How close is the system to a minimum ecological threshold?",
            "status": "review",
            "ecology_priority": 8.0,
        }
    ]
    scenario_rows = [
        evaluate_scenario(ResourceScenario("a", "A", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0))
    ]
    card = build_sustainability_review_card(register_rows, scenario_rows)
    assert "use_limit" in card
