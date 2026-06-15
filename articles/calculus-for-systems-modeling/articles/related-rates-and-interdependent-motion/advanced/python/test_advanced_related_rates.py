from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_related_rates import derivative_conditioning_check, domain_check, finite_difference_error_check, unit_review_check


def test_domain_check_flags_negative_state():
    assert domain_check(-1.0).passed is False


def test_derivative_conditioning_flags_zero():
    assert derivative_conditioning_check(0.0).passed is False


def test_finite_difference_error_flags_large_error():
    assert finite_difference_error_check(1e-2).passed is False


def test_unit_review_flags_missing_units():
    assert unit_review_check(0.0).passed is False


if __name__ == "__main__":
    test_domain_check_flags_negative_state()
    test_derivative_conditioning_flags_zero()
    test_finite_difference_error_flags_large_error()
    test_unit_review_flags_missing_units()
    print("advanced related-rates checks passed")
