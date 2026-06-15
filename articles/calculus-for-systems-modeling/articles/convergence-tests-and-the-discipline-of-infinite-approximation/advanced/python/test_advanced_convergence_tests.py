from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_convergence_tests import (
    inconclusive_result_check,
    remainder_estimate_check,
    term_test_misuse_check,
    test_conditions_check,
    test_selected_check,
)


def test_missing_test_selected_fails():
    assert test_selected_check(0.0).passed is False


def test_missing_test_conditions_fails():
    assert test_conditions_check(0.0).passed is False


def test_term_test_backward_fails():
    assert term_test_misuse_check(1.0, 1.0).passed is False


def test_missing_remainder_estimate_fails():
    assert remainder_estimate_check(0.0).passed is False


def test_unhandled_inconclusive_result_fails():
    assert inconclusive_result_check(0.0).passed is False


if __name__ == "__main__":
    test_missing_test_selected_fails()
    test_missing_test_conditions_fails()
    test_term_test_backward_fails()
    test_missing_remainder_estimate_fails()
    test_unhandled_inconclusive_result_fails()
    print("advanced convergence-test checks passed")
