from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_definite_integrals import (
    grid_size_check,
    interval_length_check,
    numerical_method_check,
    sign_convention_check,
    unit_consistency_check,
)


def test_zero_interval_fails():
    assert interval_length_check(0.0).passed is False


def test_missing_unit_check_fails():
    assert unit_consistency_check(0.0).passed is False


def test_missing_sign_convention_fails():
    assert sign_convention_check(0.0).passed is False


def test_missing_numerical_method_fails():
    assert numerical_method_check(0.0).passed is False


def test_coarse_grid_fails():
    assert grid_size_check(2.0).passed is False


if __name__ == "__main__":
    test_zero_interval_fails()
    test_missing_unit_check_fails()
    test_missing_sign_convention_fails()
    test_missing_numerical_method_fails()
    test_coarse_grid_fails()
    print("advanced definite-integral checks passed")
