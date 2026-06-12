from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from calibration_estimation_parameter_fitting.core import (
    CalibrationRecord,
    Observation,
    ParameterCandidate,
    calibration_risk_score,
    candidate_grid,
    fit_model,
    score_candidate,
    simulate,
)


def sample_data():
    return [
        Observation(0, 70.0, 5.5),
        Observation(1, 72.8, 5.8),
        Observation(2, 74.1, 6.2),
    ]


def test_simulate_has_residuals():
    rows = simulate(ParameterCandidate(0.18, 100.0), sample_data())
    assert "residual" in rows[0]
    assert len(rows) == 3


def test_score_candidate_has_sse():
    score = score_candidate(ParameterCandidate(0.18, 100.0), sample_data())
    assert "sse" in score
    assert score["sse"] >= 0


def test_candidate_grid_count():
    grid = {
        "growth_rate_min": 0.10,
        "growth_rate_max": 0.12,
        "growth_rate_step": 0.01,
        "carrying_capacity_min": 90.0,
        "carrying_capacity_max": 100.0,
        "carrying_capacity_step": 10.0,
    }
    assert len(candidate_grid(grid)) == 6


def test_fit_model_returns_best():
    candidates = [ParameterCandidate(0.10, 90.0), ParameterCandidate(0.18, 100.0)]
    best, scored = fit_model(sample_data(), candidates)
    assert best in scored


def test_calibration_risk_score_positive():
    record = CalibrationRecord(
        "objective_function",
        "loss",
        "Uses squared residuals.",
        "Does loss match purpose?",
        "review",
    )
    assert calibration_risk_score(record) > 0
