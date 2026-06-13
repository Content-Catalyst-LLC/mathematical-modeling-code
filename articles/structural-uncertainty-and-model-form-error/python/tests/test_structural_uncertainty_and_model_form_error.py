from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from structural_uncertainty_and_model_form_error.core import (
    ModelForm,
    StructuralRecord,
    comparison_rows,
    simulate_model,
    structural_risk_score,
    structural_summary,
)


def sample_forms():
    return [
        ModelForm("linear_decline", "algebraic", "Fixed decline.", "Does constant decline hide recovery?"),
        ModelForm("proportional_decline", "dynamic", "Proportional loss.", "Does proportional loss change behavior?"),
        ModelForm("logistic_recovery", "dynamic", "Recovery toward carrying capacity.", "Does recovery matter?"),
        ModelForm("threshold_shift", "piecewise", "Regime shift below threshold.", "Does threshold behavior matter?"),
    ]


def test_simulate_model_nonnegative():
    assert simulate_model("linear_decline") >= 0


def test_comparison_rows_count():
    rows = comparison_rows(sample_forms())
    assert len(rows) == 4


def test_structural_summary_has_spread():
    rows = comparison_rows(sample_forms())
    summary = structural_summary(rows)
    assert summary["structural_spread"] >= 0
    assert summary["model_count"] == 4


def test_unknown_model_form_raises():
    try:
        simulate_model("unknown")
    except ValueError:
        assert True
    else:
        assert False


def test_structural_risk_score_positive():
    record = StructuralRecord(
        "threshold_regime",
        "regime",
        "Reviews threshold behavior.",
        "Could regime shift invalidate the baseline structure?",
        "review",
    )
    assert structural_risk_score(record) > 0
