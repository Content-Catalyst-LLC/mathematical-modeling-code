from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from overfitting_underfitting_generalization.core import (
    GeneralizationModel,
    GeneralizationRecord,
    classify_model,
    generalization_risk_score,
    generalization_score,
    model_rows,
    overfit_gap,
)


def test_overfit_gap():
    model = GeneralizationModel("m", "family", 0.5, 2.0, 6, 0.9, 0.4)
    assert overfit_gap(model) == 1.5


def test_likely_overfit_classification():
    model = GeneralizationModel("m", "family", 0.5, 2.0, 6, 0.9, 0.4)
    assert classify_model(model) == "likely_overfit"


def test_likely_underfit_classification():
    model = GeneralizationModel("m", "baseline", 3.2, 3.5, 0, 0.1, 0.9)
    assert classify_model(model) == "likely_underfit"


def test_model_rows_sorted():
    models = [
        GeneralizationModel("bad", "flexible", 0.2, 3.0, 10, 0.9, 0.2),
        GeneralizationModel("good", "mechanistic", 1.0, 1.2, 3, 0.4, 0.8),
    ]
    assert model_rows(models)[0]["model_id"] == "good"


def test_generalization_score_float():
    model = GeneralizationModel("m", "family", 1.0, 1.4, 3, 0.5, 0.8)
    assert isinstance(generalization_score(model), float)


def test_generalization_risk_score_positive():
    record = GeneralizationRecord(
        "overfit_gap",
        "diagnostics",
        "Compares validation error against training error.",
        "Is the model learning noise?",
        "review",
    )
    assert generalization_risk_score(record) > 0
