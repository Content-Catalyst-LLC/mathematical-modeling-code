from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mathematical_modeling_in_artificial_intelligence_and_data_systems.core import (
    AIModelRecord,
    ModelCandidate,
    build_ai_model_governance_card,
    deployment_summary,
    evaluate_candidate,
    model_priority,
)


def test_evaluate_candidate_has_review_class():
    candidate = ModelCandidate("constrained", "Constrained", 0.81, 0.035, 0.060, 0.100, 0.780, 0.090, 0.66)
    row = evaluate_candidate(candidate)
    assert "governance_score" in row
    assert "review_class" in row


def test_high_stakes_review_flag():
    candidate = ModelCandidate("neural", "Neural", 0.86, 0.095, 0.190, 0.240, 0.380, 0.180, 0.82)
    row = evaluate_candidate(candidate)
    assert row["requires_review"] is True
    assert row["review_class"] == "high_stakes_review_required"


def test_deployment_summary_count():
    rows = [
        evaluate_candidate(ModelCandidate("a", "A", 0.76, 0.050, 0.080, 0.120, 0.920, 0.080, 0.62)),
        evaluate_candidate(ModelCandidate("b", "B", 0.81, 0.035, 0.060, 0.100, 0.780, 0.090, 0.66)),
    ]
    summary = deployment_summary(rows)
    assert summary["candidate_count"] == 2
    assert "best_governed_candidate" in summary


def test_model_priority_positive():
    record = AIModelRecord(
        "governance_model",
        "governance",
        "model_card_and_audit_register",
        "model_lifecycle_records",
        "accountability and review",
        "review",
    )
    assert model_priority(record) > 0


def test_governance_card_has_use_limit():
    register_rows = [
        {
            "key": "governance_model",
            "model_role": "governance",
            "model_family": "model_card_and_audit_register",
            "data_domain": "model_lifecycle_records",
            "decision_context": "accountability and review",
            "status": "review",
            "model_priority": 8.0,
        }
    ]
    candidate_rows = [
        evaluate_candidate(ModelCandidate("a", "A", 0.76, 0.050, 0.080, 0.120, 0.920, 0.080, 0.62))
    ]
    card = build_ai_model_governance_card(register_rows, candidate_rows)
    assert "use_limit" in card
