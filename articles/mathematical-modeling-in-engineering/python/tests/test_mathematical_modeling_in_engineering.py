from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from mathematical_modeling_in_engineering.core import (
    BeamDesign,
    EngineeringModelRecord,
    build_engineering_design_review_card,
    design_summary,
    engineering_priority,
    evaluate_beam,
)


def test_evaluate_beam_contains_safety_factor():
    design = BeamDesign("balanced_design", 0.10, 0.18, 3.0, 4200.0, 145_000_000.0, 7850.0)
    row = evaluate_beam(design)
    assert row["safety_factor"] > 0
    assert "passes_stress_constraint" in row


def test_design_summary_count():
    rows = [
        evaluate_beam(BeamDesign("a", 0.10, 0.18, 3.0, 4200.0, 145_000_000.0, 7850.0)),
        evaluate_beam(BeamDesign("b", 0.12, 0.22, 3.0, 4200.0, 145_000_000.0, 7850.0)),
    ]
    summary = design_summary(rows)
    assert summary["design_count"] == 2
    assert summary["min_safety_factor"] > 0


def test_engineering_priority_positive():
    record = EngineeringModelRecord(
        "safety_model",
        "structural_engineering",
        "safety_review",
        "limit_state_model",
        "Does the design maintain positive stress margin?",
        "review",
    )
    assert engineering_priority(record) > 0


def test_review_card_has_use_limit():
    register_rows = [
        {
            "key": "safety_model",
            "engineering_domain": "structural_engineering",
            "model_role": "safety_review",
            "model_family": "limit_state_model",
            "design_question": "Does the design maintain positive stress margin?",
            "status": "review",
            "engineering_priority": 7.0,
        }
    ]
    design_rows = [
        evaluate_beam(BeamDesign("balanced_design", 0.10, 0.18, 3.0, 4200.0, 145_000_000.0, 7850.0))
    ]
    card = build_engineering_design_review_card(register_rows, design_rows)
    assert "use_limit" in card
