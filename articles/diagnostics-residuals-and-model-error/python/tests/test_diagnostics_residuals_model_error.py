from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from diagnostics_residuals_model_error.core import (
    DiagnosticObservation,
    DiagnosticRecord,
    diagnostic_risk_score,
    error_summary,
    flag_outliers,
    group_summary,
    residual_rows,
)


def sample_data():
    return [
        DiagnosticObservation(1, "baseline", 10.0, 9.0, 8.0),
        DiagnosticObservation(2, "baseline", 12.0, 11.0, 8.0),
        DiagnosticObservation(3, "stress", 6.0, 9.5, 8.0),
    ]


def test_residual_rows():
    rows = residual_rows(sample_data())
    assert rows[0]["residual"] == 1.0
    assert rows[2]["decision_disagreement"] is True


def test_error_summary():
    summary = error_summary(residual_rows(sample_data()))
    assert "rmse" in summary
    assert summary["n"] == 3


def test_group_summary():
    summary = group_summary(residual_rows(sample_data()))
    assert len(summary) == 2


def test_outlier_flags_return_list():
    flagged = flag_outliers(residual_rows(sample_data()))
    assert isinstance(flagged, list)


def test_diagnostic_risk_score_positive():
    record = DiagnosticRecord(
        "threshold_error",
        "decision_support",
        "Reviews residuals near action thresholds.",
        "Could residual error change the decision?",
        "review",
    )
    assert diagnostic_risk_score(record) > 0
