from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mathematical_modeling_in_policy_and_public_systems.core import (
    PolicyModelRecord,
    PolicyOption,
    build_policy_decision_support_card,
    evaluate_policy_option,
    policy_priority,
    policy_summary,
)


def test_evaluate_policy_option_contains_review_class():
    option = PolicyOption("adaptive_pathway", "Adaptive pathway", 73.0, 38.0, 0.70, 0.82, 16.0, 0.24)
    row = evaluate_policy_option(option)
    assert "review_class" in row
    assert row["budget_violation"] is False


def test_policy_summary_count():
    rows = [
        evaluate_policy_option(PolicyOption("a", "A", 42.0, 18.0, 0.86, 0.52, 18.0, 0.42)),
        evaluate_policy_option(PolicyOption("b", "B", 73.0, 38.0, 0.70, 0.82, 16.0, 0.24)),
    ]
    summary = policy_summary(rows)
    assert summary["option_count"] == 2
    assert "best_scored_option" in summary


def test_policy_priority_positive():
    record = PolicyModelRecord(
        "equity_model",
        "public_accountability",
        "distributional_review",
        "equity_diagnostic",
        "How are benefits and burdens distributed across groups or places?",
        "review",
    )
    assert policy_priority(record) > 0


def test_review_card_has_use_limit():
    register_rows = [
        {
            "key": "equity_model",
            "policy_domain": "public_accountability",
            "model_role": "distributional_review",
            "model_family": "equity_diagnostic",
            "public_question": "How are benefits and burdens distributed?",
            "status": "review",
            "policy_priority": 8.0,
        }
    ]
    option_rows = [
        evaluate_policy_option(PolicyOption("b", "B", 73.0, 38.0, 0.70, 0.82, 16.0, 0.24))
    ]
    card = build_policy_decision_support_card(register_rows, option_rows)
    assert "use_limit" in card
