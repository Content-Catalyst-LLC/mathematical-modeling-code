from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_elasticity_sensitivity import (
    finite_difference_error_check,
    local_scope_check,
    nonzero_input_check,
    nonzero_output_check,
    positive_log_domain_check,
)


def test_zero_input_fails_elasticity_check():
    assert nonzero_input_check(0.0).passed is False


def test_zero_output_fails_elasticity_check():
    assert nonzero_output_check(0.0).passed is False


def test_negative_log_domain_fails():
    assert positive_log_domain_check(-1.0, 10.0).passed is False


def test_large_finite_difference_error_fails():
    assert finite_difference_error_check(1e-2).passed is False


def test_missing_local_scope_fails():
    assert local_scope_check(0.0).passed is False


if __name__ == "__main__":
    test_zero_input_fails_elasticity_check()
    test_zero_output_fails_elasticity_check()
    test_negative_log_domain_fails()
    test_large_finite_difference_error_fails()
    test_missing_local_scope_fails()
    print("advanced elasticity/sensitivity checks passed")
