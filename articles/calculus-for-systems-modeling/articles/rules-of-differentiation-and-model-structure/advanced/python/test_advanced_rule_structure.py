from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_rule_structure import chain_link_check, implicit_regular_check, log_positive_check, quotient_denominator_check


def test_quotient_denominator_check_flags_zero():
    assert quotient_denominator_check(0.0).passed is False


def test_chain_link_check_flags_failed_link():
    assert chain_link_check([True, False, True]).passed is False


def test_implicit_regular_check_flags_zero_partial():
    assert implicit_regular_check(0.0).passed is False


def test_log_positive_check_flags_negative():
    assert log_positive_check(-1.0).passed is False


if __name__ == "__main__":
    test_quotient_denominator_check_flags_zero()
    test_chain_link_check_flags_failed_link()
    test_implicit_regular_check_flags_zero_partial()
    test_log_positive_check_flags_negative()
    print("advanced rule-structure checks passed")
