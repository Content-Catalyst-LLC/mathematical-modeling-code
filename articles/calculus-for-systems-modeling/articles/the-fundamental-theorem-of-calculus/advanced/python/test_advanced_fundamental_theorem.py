from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_fundamental_theorem import (
    baseline_check,
    grid_step_check,
    interval_length_check,
    residual_tolerance_check,
    unit_consistency_check,
)


def test_large_residual_fails():
    assert residual_tolerance_check(0.05).passed is False


def test_zero_interval_fails():
    assert interval_length_check(0.0).passed is False


def test_missing_unit_check_fails():
    assert unit_consistency_check(0.0).passed is False


def test_missing_baseline_fails():
    assert baseline_check(0.0).passed is False


def test_coarse_grid_fails():
    assert grid_step_check(2.0).passed is False


if __name__ == "__main__":
    test_large_residual_fails()
    test_zero_interval_fails()
    test_missing_unit_check_fails()
    test_missing_baseline_fails()
    test_coarse_grid_fails()
    print("advanced Fundamental Theorem checks passed")
