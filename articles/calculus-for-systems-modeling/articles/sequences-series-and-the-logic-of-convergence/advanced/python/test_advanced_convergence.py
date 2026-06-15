from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_convergence import (
    absolute_convergence_check,
    latest_term_test,
    remainder_bound_check,
    sequence_defined_check,
    stopping_rule_check,
)


def test_missing_sequence_definition_fails():
    assert sequence_defined_check(0.0).passed is False


def test_missing_stopping_rule_fails():
    assert stopping_rule_check(0.0).passed is False


def test_missing_remainder_bound_fails():
    assert remainder_bound_check(0.0).passed is False


def test_latest_term_without_tail_bound_fails():
    assert latest_term_test(0.0001, None).passed is False


def test_missing_absolute_convergence_review_fails():
    assert absolute_convergence_check(0.0).passed is False


if __name__ == "__main__":
    test_missing_sequence_definition_fails()
    test_missing_stopping_rule_fails()
    test_missing_remainder_bound_fails()
    test_latest_term_without_tail_bound_fails()
    test_missing_absolute_convergence_review_fails()
    print("advanced convergence checks passed")
