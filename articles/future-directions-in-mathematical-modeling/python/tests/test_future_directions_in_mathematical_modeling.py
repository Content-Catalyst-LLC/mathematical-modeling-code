from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from future_directions_in_mathematical_modeling.core import FutureModelingDirection, build_future_modeling_review_card, direction_priority, portfolio_summary


def test_direction_priority_has_review_class():
    row = FutureModelingDirection("ai_assistance", "AI-assisted modeling", "computational_workflow", 0.82, 0.78, 0.90, 0.76, 0.92)
    scored = direction_priority(row)
    assert scored["review_class"] == "governance_priority"
    assert scored["requires_governance_plan"] is True


def test_uncertainty_workflow_flags_uncertainty():
    row = FutureModelingDirection("uncertainty_workflows", "Uncertainty-aware modeling", "uncertainty_analysis", 0.90, 0.72, 0.82, 0.92, 0.86)
    scored = direction_priority(row)
    assert scored["requires_uncertainty_brief"] is True
    assert scored["requires_human_judgment_protocol"] is True


def test_portfolio_summary_and_card():
    rows = [direction_priority(FutureModelingDirection("a", "A", "area", 0.80, 0.70, 0.80, 0.70, 0.80))]
    assert portfolio_summary(rows)["direction_count"] == 1
    assert "use_limit" in build_future_modeling_review_card(rows)
