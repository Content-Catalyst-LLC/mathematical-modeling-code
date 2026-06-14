from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from model_governance_and_accountability.core import (
    GovernanceRiskCase,
    ModelGovernanceRecord,
    build_model_governance_card,
    evaluate_governance_risk,
    governance_priority,
    governance_summary,
)


def test_governance_priority_increases_for_unapproved_critical_model():
    record = ModelGovernanceRecord(
        "ai_triage_support",
        "AI-assisted triage support model",
        "decision support under clinical review",
        "critical",
        "review_required",
        "not_approved",
        "pending",
        "clinical analytics team",
        "clinical governance board",
    )
    assert governance_priority(record) > 10


def test_evaluate_governance_risk_flags_reviews():
    case = GovernanceRiskCase("ai", "AI model", 0.62, 0.72, 0.95, 0.70, 0.55)
    row = evaluate_governance_risk(case)
    assert row["requires_uncertainty_brief"] is True
    assert row["requires_use_limit_review"] is True
    assert row["requires_accountability_review"] is True


def test_governance_summary_count():
    rows = [
        evaluate_governance_risk(GovernanceRiskCase("a", "A", 0.38, 0.56, 0.82, 0.42, 0.24)),
        evaluate_governance_risk(GovernanceRiskCase("b", "B", 0.62, 0.72, 0.95, 0.70, 0.55)),
    ]
    summary = governance_summary(rows)
    assert summary["case_count"] == 2
    assert "highest_risk_model" in summary


def test_governance_card_has_use_limit():
    register_rows = [
        {
            "key": "a",
            "model_name": "A",
            "model_purpose": "Planning",
            "risk_tier": "high",
            "validation_status": "review_required",
            "use_limit_status": "draft",
            "monitoring_status": "pending",
            "model_owner": "owner",
            "decision_owner": "decision owner",
            "governance_priority": 11.5,
        }
    ]
    risk_rows = [
        evaluate_governance_risk(GovernanceRiskCase("a", "A", 0.38, 0.56, 0.82, 0.42, 0.24))
    ]
    card = build_model_governance_card(register_rows, risk_rows)
    assert "use_limit" in card
    assert "diagnostic_checks" in card
