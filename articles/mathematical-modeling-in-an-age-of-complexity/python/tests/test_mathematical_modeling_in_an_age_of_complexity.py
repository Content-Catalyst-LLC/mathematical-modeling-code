from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mathematical_modeling_in_an_age_of_complexity.core import (
    ComplexityModelRecord,
    ComplexityScenario,
    build_complexity_model_review_card,
    complexity_summary,
    evaluate_scenario,
    model_priority,
)


def test_evaluate_scenario_has_review_class():
    scenario = ComplexityScenario("compound", "Compound", 0.78, 0.70, 0.72, 0.48, 0.52, 0.55)
    row = evaluate_scenario(scenario)
    assert "fragility_score" in row
    assert "robust_value" in row
    assert "review_class" in row


def test_high_complexity_or_review_flag():
    scenario = ComplexityScenario("cascade", "Cascade", 0.88, 0.86, 0.75, 0.32, 0.40, 0.42)
    row = evaluate_scenario(scenario)
    assert row["requires_adaptive_trigger"] is True
    assert row["requires_interdependence_review"] is True
    assert row["requires_equity_review"] is True


def test_complexity_summary_count():
    rows = [
        evaluate_scenario(ComplexityScenario("a", "A", 0.35, 0.45, 0.40, 0.72, 0.68, 0.65)),
        evaluate_scenario(ComplexityScenario("b", "B", 0.78, 0.70, 0.72, 0.48, 0.52, 0.55)),
    ]
    summary = complexity_summary(rows)
    assert summary["scenario_count"] == 2
    assert "highest_fragility_scenario" in summary


def test_model_priority_positive():
    record = ComplexityModelRecord(
        "network_model",
        "interdependence_analysis",
        "network_model",
        "cascading_dependency",
        "identifying systemic risk and fragile bridges",
        "review",
    )
    assert model_priority(record) > 0


def test_review_card_has_use_limit():
    model_rows = [
        {
            "key": "network_model",
            "model_role": "interdependence_analysis",
            "model_family": "network_model",
            "complexity_feature": "cascading_dependency",
            "decision_context": "identifying systemic risk and fragile bridges",
            "status": "review",
            "model_priority": 8.0,
        }
    ]
    scenario_rows = [
        evaluate_scenario(ComplexityScenario("a", "A", 0.35, 0.45, 0.40, 0.72, 0.68, 0.65))
    ]
    card = build_complexity_model_review_card(model_rows, scenario_rows)
    assert "use_limit" in card
