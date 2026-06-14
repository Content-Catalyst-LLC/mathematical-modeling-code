from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mathematical_modeling_in_science.core import (
    PopulationScenario,
    ScientificModelRecord,
    build_scientific_model_evidence_card,
    evidence_summary,
    logistic_population,
    scenario_summary,
    scientific_priority,
)


def test_logistic_population_length():
    trajectory = logistic_population(40.0, 0.28, 500.0, 20)
    assert len(trajectory) == 21
    assert trajectory[0]["population"] == 40.0


def test_scenario_summary_contains_final_population():
    scenario = PopulationScenario("baseline", 0.28, 500.0, 40.0, 20, 0.03)
    row = scenario_summary(scenario)
    assert row["final_population"] > 0
    assert row["trajectory_points"] == 21


def test_evidence_summary_count():
    rows = [
        scenario_summary(PopulationScenario("a", 0.28, 500.0, 40.0, 20, 0.03)),
        scenario_summary(PopulationScenario("b", 0.18, 500.0, 40.0, 20, 0.03)),
    ]
    summary = evidence_summary(rows)
    assert summary["scenario_count"] == 2
    assert summary["scenario_spread"] >= 0


def test_scientific_priority_positive():
    record = ScientificModelRecord(
        "uncertainty_model",
        "scientific_computing",
        "uncertainty_quantification",
        "sensitivity_analysis",
        "Which assumptions most affect scientific conclusions?",
        "review",
    )
    assert scientific_priority(record) > 0


def test_evidence_card_has_use_limit():
    register_rows = [
        {
            "key": "mechanism_model",
            "scientific_domain": "ecology",
            "model_role": "explanation",
            "model_family": "differential_equation",
            "evidence_question": "Can resource limitation explain observed slowing growth?",
            "status": "active",
            "scientific_priority": 2.0,
        }
    ]
    scenario_rows = [
        scenario_summary(PopulationScenario("baseline", 0.28, 500.0, 40.0, 20, 0.03))
    ]
    card = build_scientific_model_evidence_card(register_rows, scenario_rows)
    assert "use_limit" in card
