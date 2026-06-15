from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from equilibrium_stability.cli import (
    bistable_rate,
    classify_scalar_stability,
    logistic_derivative,
    logistic_rate,
    numerical_derivative,
    build_stability_records,
)

def test_logistic_rate():
    assert logistic_rate(10.0, 0.6, 100.0) == 5.4

def test_logistic_derivative_boundary_and_capacity():
    assert logistic_derivative(0.0, 0.6, 100.0) == 0.6
    assert logistic_derivative(100.0, 0.6, 100.0) == -0.6

def test_bistable_rate_equilibrium():
    assert bistable_rate(0.4, 0.4) == 0.0

def test_classify_stability():
    assert classify_scalar_stability(-0.1) == "locally_stable"
    assert classify_scalar_stability(0.1) == "locally_unstable"
    assert classify_scalar_stability(0.0) == "inconclusive_by_linearization"

def test_records_count():
    assert len(build_stability_records()) == 5

def test_numerical_derivative_threshold_positive():
    derivative = numerical_derivative(lambda x: bistable_rate(x, 0.4), 0.4)
    assert derivative > 0
