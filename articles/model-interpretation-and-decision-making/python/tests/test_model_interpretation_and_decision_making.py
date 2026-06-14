from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from model_interpretation_and_decision_making.core import (
    DecisionOption,
    InterpretationRecord,
    build_decision_support_review_card,
    decision_summary,
    evaluate_option,
    interpretation_priority,
)


def test_evaluate_option_has_threshold_flag():
    option = DecisionOption(
        "monitoring",
        "Formal monitoring",
        54.0,
        42.0,
        68.0,
        3.0,
        6.0,
        "Increase measurement.",
    )
    row = evaluate_option(option)
    assert row["crosses_threshold_under_uncertainty"] is True
    assert row["robustness_class"] == "fragile"


def test_decision_summary_best_option():
    rows = [
        evaluate_option(DecisionOption("a", "A", 50.0, 40.0, 60.0, 1.0, 9.0, "A")),
        evaluate_option(DecisionOption("b", "B", 62.0, 50.0, 72.0, 5.0, 3.0, "B")),
    ]
    summary = decision_summary(rows)
    assert summary["option_count"] == 2
    assert "best_scored_option" in summary


def test_interpretation_priority_positive():
    record = InterpretationRecord(
        "threshold_review",
        "decision_threshold",
        "Reviews proximity to action boundary.",
        "Does the result cross or approach the threshold?",
        "review",
    )
    assert interpretation_priority(record) > 0


def test_review_card_has_use_limit():
    records = [
        {
            "key": "output_meaning",
            "interpretation_layer": "result",
            "model_role": "Explains output.",
            "decision_question": "What claim is being made?",
            "status": "active",
            "interpretation_priority": 1.0,
        }
    ]
    options = [
        evaluate_option(DecisionOption("b", "B", 62.0, 50.0, 72.0, 5.0, 3.0, "B"))
    ]
    card = build_decision_support_review_card(records, options)
    assert "use_limit" in card
