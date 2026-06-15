from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_substitution import (
    monotonicity_check,
    residual_tolerance_check,
    scale_factor_check,
    transformed_bounds_check,
    unit_consistency_check,
)


def test_large_residual_fails():
    assert residual_tolerance_check(0.1).passed is False


def test_missing_scale_factor_fails():
    assert scale_factor_check(0.0).passed is False


def test_missing_bounds_fails():
    assert transformed_bounds_check(0.0).passed is False


def test_missing_unit_check_fails():
    assert unit_consistency_check(0.0).passed is False


def test_nonmonotonic_interval_fails():
    assert monotonicity_check(-0.2).passed is False


if __name__ == "__main__":
    test_large_residual_fails()
    test_missing_scale_factor_fails()
    test_missing_bounds_fails()
    test_missing_unit_check_fails()
    test_nonmonotonic_interval_fails()
    print("advanced substitution checks passed")
