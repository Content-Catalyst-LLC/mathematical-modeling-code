from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from communicating_model_uncertainty.core import (
    CommunicationRecord,
    UncertaintyMessage,
    build_communication_card,
    communication_priority,
)


def test_priority_positive():
    record = CommunicationRecord(
        "threshold_risk",
        "decision_threshold",
        "decision_maker",
        "Explain whether uncertainty could reverse action.",
        "Some plausible runs cross the action threshold.",
        "review",
    )
    assert communication_priority(record) > 0


def test_build_card_contains_use_limit():
    records = [
        CommunicationRecord(
            "central_result",
            "result",
            "decision_maker",
            "State the baseline result.",
            "The model result is conditional on assumptions.",
            "active",
        )
    ]
    messages = [
        UncertaintyMessage(
            "scenario_uncertainty",
            "scenario",
            "Outputs differ across named future conditions.",
            "These are possible futures, not guaranteed forecasts.",
            "Test the decision across scenarios.",
        )
    ]
    card = build_communication_card(records, messages)
    assert "use_limit_statement" in card
    assert len(card["communication_records"]) == 1
    assert len(card["uncertainty_messages"]) == 1
