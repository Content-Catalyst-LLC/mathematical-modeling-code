from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from model_comparison_and_selection.core import (
    ModelCandidate,
    SelectionRecord,
    comparison_score,
    model_rows,
    overfit_gap,
    selection_risk_score,
)


def test_overfit_gap():
    model = ModelCandidate("m", "family", 1.0, 2.5, 2, 0.7, 0.6, 0.8)
    assert overfit_gap(model) == 1.5


def test_comparison_score_is_float():
    model = ModelCandidate("m", "family", 1.0, 2.5, 2, 0.7, 0.6, 0.8)
    assert isinstance(comparison_score(model), float)


def test_model_rows_sorted():
    models = [
        ModelCandidate("a", "baseline", 2.0, 3.0, 0, 0.9, 0.6, 0.5),
        ModelCandidate("b", "mechanistic", 1.0, 1.3, 3, 0.7, 0.8, 0.9),
    ]
    rows = model_rows(models)
    assert rows[0]["model_id"] == "b"


def test_overfit_flag():
    models = [ModelCandidate("flex", "flexible", 0.2, 2.0, 8, 0.3, 0.4, 0.5)]
    rows = model_rows(models)
    assert rows[0]["overfit_flag"] is True


def test_selection_risk_score_positive():
    record = SelectionRecord(
        "validation_error",
        "generalization",
        "Compares performance on validation data.",
        "Does the selected model generalize?",
        "active",
    )
    assert selection_risk_score(record) > 0
