from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from model_calibration_calculus.cli import (
    evaluate_candidate,
    grid_search,
    logistic_solution,
    residuals,
    synthetic_data,
)

def test_logistic_solution_initial_value():
    assert logistic_solution(0.0, 10.0, 0.34, 105.0) == 10.0

def test_synthetic_data_length():
    assert len(synthetic_data()) == 7

def test_residuals_length():
    data = synthetic_data()
    assert len(residuals(data, 0.34, 105.0)) == len(data)

def test_grid_search_sorted():
    candidates = grid_search(synthetic_data())
    assert candidates[0].loss <= candidates[-1].loss

def test_candidate_loss_nonnegative():
    candidate = evaluate_candidate(synthetic_data(), 0.34, 105.0)
    assert candidate.loss >= 0.0
