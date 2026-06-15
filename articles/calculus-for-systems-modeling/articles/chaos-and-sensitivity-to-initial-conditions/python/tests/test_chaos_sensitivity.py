from pathlib import Path
import math
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from chaos_sensitivity.cli import (
    estimate_lyapunov,
    forecast_horizon,
    logistic_derivative,
    logistic_map,
    simulate_pair,
)

def test_logistic_map():
    assert abs(logistic_map(0.2, 3.9) - 0.624) < 1e-12

def test_logistic_derivative():
    assert abs(logistic_derivative(0.2, 3.9) - 2.34) < 1e-12

def test_simulate_pair_length():
    assert len(simulate_pair(0.2, 1e-8, 3.9, 100)) == 101

def test_lyapunov_is_finite():
    value = estimate_lyapunov(0.2, 3.9, 50, 100)
    assert math.isfinite(value)

def test_forecast_horizon():
    horizon = forecast_horizon(1e-8, 1e-2, 0.5)
    assert horizon is not None
    assert horizon > 0
