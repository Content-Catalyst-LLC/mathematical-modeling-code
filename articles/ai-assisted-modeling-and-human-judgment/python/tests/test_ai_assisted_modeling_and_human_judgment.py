from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from ai_assisted_modeling_and_human_judgment.core import (
    AIAssistanceRecord,
    HumanJudgmentCase,
    build_ai_assisted_modeling_governance_card,
    evaluate_judgment_case,
    judgment_summary,
    review_priority,
)


def test_review_priority_positive():
    record = AIAssistanceRecord("code", "computation", "code_assistant", "model_script", True, True, "review")
    assert review_priority(record) > 0


def test_evaluate_judgment_case_flags_review():
    case = HumanJudgmentCase("model_use", "approved use decision", "moving from exploratory to decision support", 0.68, 0.70, 0.88, 0.72, 0.55)
    row = evaluate_judgment_case(case)
    assert "judgment_risk_score" in row
    assert row["requires_use_limit_statement"] is True
    assert row["requires_uncertainty_brief"] is True
    assert row["requires_accountability_owner"] is True


def test_judgment_summary_count():
    rows = [
        evaluate_judgment_case(HumanJudgmentCase("a", "problem framing", "test", 0.72, 0.58, 0.80, 0.45, 0.70)),
        evaluate_judgment_case(HumanJudgmentCase("b", "data fitness", "test", 0.62, 0.66, 0.75, 0.50, 0.65)),
    ]
    summary = judgment_summary(rows)
    assert summary["case_count"] == 2
    assert "highest_risk_judgment_point" in summary


def test_governance_card_has_use_limit():
    assistance_rows = [
        {
            "key": "code_generation",
            "modeling_stage": "computation",
            "ai_role": "code_assistant",
            "artifact_type": "model_script",
            "provenance_required": True,
            "human_review_required": True,
            "status": "review",
            "review_priority": 8.0,
        }
    ]
    judgment_rows = [
        evaluate_judgment_case(HumanJudgmentCase("a", "problem framing", "test", 0.72, 0.58, 0.80, 0.45, 0.70))
    ]
    card = build_ai_assisted_modeling_governance_card(assistance_rows, judgment_rows)
    assert "use_limit" in card
    assert "diagnostic_checks" in card
