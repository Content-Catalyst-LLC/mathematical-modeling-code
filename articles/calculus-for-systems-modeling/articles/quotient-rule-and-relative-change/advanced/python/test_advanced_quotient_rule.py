from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_quotient_rule import denominator_check, positivity_check, relative_rate_identity


def test_denominator_check_flags_zero():
    assert denominator_check(0.0).passed is False


def test_positivity_check_flags_negative():
    assert positivity_check(-1.0).passed is False


def test_relative_rate_identity_passes_exact_case():
    assert relative_rate_identity(-0.01, 0.02, -0.03).passed is True


def test_relative_rate_identity_flags_mismatch():
    assert relative_rate_identity(-0.01, 0.02, -0.02).passed is False


if __name__ == "__main__":
    test_denominator_check_flags_zero()
    test_positivity_check_flags_negative()
    test_relative_rate_identity_passes_exact_case()
    test_relative_rate_identity_flags_mismatch()
    print("advanced quotient-rule checks passed")
