from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from monte_carlo_uncertainty_propagation.core import (
    MonteCarloRecord,
    MonteCarloScenario,
    convergence_rows,
    monte_carlo_risk_score,
    quantile,
    run_monte_carlo,
    summarize,
)


def test_quantile_median():
    assert quantile([1, 2, 3], 0.5) == 2


def test_run_monte_carlo_replication_count():
    scenario = MonteCarloScenario(
        "test", 65.0, 75.0, 0.14, 0.22, 5.0, 8.0,
        0.02, 0.08, 0.12, 100.0, 10, 25, 10.0, 123
    )
    rows = run_monte_carlo(scenario)
    assert len(rows) == 25
    assert "final_stock" in rows[0]


def test_summarize_has_probability():
    scenario = MonteCarloScenario(
        "test", 65.0, 75.0, 0.14, 0.22, 5.0, 8.0,
        0.02, 0.08, 0.12, 100.0, 10, 25, 10.0, 123
    )
    summary = summarize(run_monte_carlo(scenario))
    assert "depletion_probability" in summary[0]


def test_convergence_rows():
    scenario = MonteCarloScenario(
        "test", 65.0, 75.0, 0.14, 0.22, 5.0, 8.0,
        0.02, 0.08, 0.12, 100.0, 10, 25, 10.0, 123
    )
    rows = convergence_rows(run_monte_carlo(scenario), [5, 10, 25])
    assert len(rows) == 3


def test_monte_carlo_risk_score_positive():
    record = MonteCarloRecord(
        "input_distributions",
        "input_uncertainty",
        "uniform ranges",
        "Uncertain inputs are represented by bounded distributions.",
        "Are input ranges evidence-based?",
        "review",
    )
    assert monte_carlo_risk_score(record) > 0
