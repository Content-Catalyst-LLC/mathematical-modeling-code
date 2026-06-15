from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_second_derivatives import finite_difference_error_check, inflection_sign_change_check, noise_review_check, smoothness_check


def test_smoothness_check_flags_missing_smoothness():
    assert smoothness_check(0.0).passed is False


def test_inflection_check_flags_missing_sign_change():
    assert inflection_sign_change_check(0.0).passed is False


def test_finite_difference_error_flags_large_error():
    assert finite_difference_error_check(1e-2).passed is False


def test_noise_review_flags_missing_review():
    assert noise_review_check(0.0).passed is False


if __name__ == "__main__":
    test_smoothness_check_flags_missing_smoothness()
    test_inflection_check_flags_missing_sign_change()
    test_finite_difference_error_flags_large_error()
    test_noise_review_flags_missing_review()
    print("advanced second-derivative checks passed")
