from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_chain_rule import domain_compatibility_check, differentiable_links_check, implementation_warning_check, local_validity_check


def test_domain_check_flags_outside_value():
    assert domain_compatibility_check(1.5, 0.0, 1.0).passed is False


def test_differentiable_links_flags_false_link():
    assert differentiable_links_check([True, False, True]).passed is False


def test_local_validity_flags_overextension():
    assert local_validity_check(5.0).passed is False


def test_implementation_warning_flags_conditionals():
    assert implementation_warning_check(True).passed is False


if __name__ == "__main__":
    test_domain_check_flags_outside_value()
    test_differentiable_links_flags_false_link()
    test_local_validity_flags_overextension()
    test_implementation_warning_flags_conditionals()
    print("advanced chain-rule checks passed")
