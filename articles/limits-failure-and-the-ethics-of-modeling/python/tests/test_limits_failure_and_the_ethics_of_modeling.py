from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from limits_failure_and_the_ethics_of_modeling.core import (
    ModelFailureRecord,
    ModelRiskCase,
    build_model_ethics_governance_card,
    ethics_summary,
    evaluate_risk_case,
    failure_priority,
)


def test_evaluate_risk_case_has_review_class():
    case = ModelRiskCase("allocation", "Allocation", "scarce resources", 0.85, 0.55, 0.55, 0.65, 0.75, 0.70)
    row = evaluate_risk_case(case)
    assert "ethical_risk_score" in row
    assert "review_class" in row
    assert row["requires_use_limit_statement"] is True


def test_high_ethics_review_required():
    case = ModelRiskCase("auto", "Automated score", "institutional action", 0.90, 0.60, 0.70, 0.60, 0.80, 0.85)
    row = evaluate_risk_case(case)
    assert row["review_class"] == "high_ethics_review_required"


def test_ethics_summary_count():
    rows = [
        evaluate_risk_case(ModelRiskCase("a", "A", "learning", 0.35, 0.35, 0.25, 0.60, 0.30, 0.25)),
        evaluate_risk_case(ModelRiskCase("b", "B", "allocation", 0.85, 0.55, 0.55, 0.65, 0.75, 0.70)),
    ]
    summary = ethics_summary(rows)
    assert summary["case_count"] == 2
    assert "highest_risk_model" in summary


def test_failure_priority_positive():
    record = ModelFailureRecord(
        "validation_gap",
        "model used beyond tested domain",
        "validation",
        "unsupported decision authority",
        "scope creep or weak approval process",
        "review",
    )
    assert failure_priority(record) > 0


def test_governance_card_has_use_limit():
    failure_rows = [
        {
            "key": "validation_gap",
            "failure_mode": "model used beyond tested domain",
            "model_stage": "validation",
            "ethical_issue": "unsupported decision authority",
            "likely_cause": "scope creep or weak approval process",
            "review_status": "review",
            "failure_priority": 8.0,
        }
    ]
    risk_rows = [
        evaluate_risk_case(ModelRiskCase("a", "A", "learning", 0.35, 0.35, 0.25, 0.60, 0.30, 0.25))
    ]
    card = build_model_ethics_governance_card(failure_rows, risk_rows)
    assert "use_limit" in card
