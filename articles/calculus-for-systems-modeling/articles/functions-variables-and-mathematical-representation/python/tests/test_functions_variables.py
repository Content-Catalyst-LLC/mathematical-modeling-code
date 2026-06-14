from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from functions_variables_mathematical_representation.core import (
    evaluate_models,
    linear_model,
    logistic_model,
    summarize_results,
)


def test_linear_model():
    assert linear_model(2.0, 10.0, 2.0) == 14.0


def test_logistic_model_positive():
    assert logistic_model(5.0) > 0


def test_evaluate_models_four_rows_per_x():
    rows = evaluate_models([0.0, 1.0])
    assert len(rows) == 8


def test_summary_has_four_models():
    summary = summarize_results(evaluate_models([0.0, 1.0, 2.0]))
    assert len(summary) == 4
