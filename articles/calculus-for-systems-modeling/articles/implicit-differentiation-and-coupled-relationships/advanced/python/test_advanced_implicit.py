from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_implicit import branch_distance_check, conditioning_check, regularity_check, residual_check


def test_regularity_check_flags_zero():
    assert regularity_check(0.0).passed is False


def test_conditioning_check_flags_large_condition_number():
    assert conditioning_check(1e10).passed is False


def test_branch_distance_flags_overextension():
    assert branch_distance_check(3.0).passed is False


def test_residual_check_flags_large_residual():
    assert residual_check(1e-2).passed is False


if __name__ == "__main__":
    test_regularity_check_flags_zero()
    test_conditioning_check_flags_large_condition_number()
    test_branch_distance_flags_overextension()
    test_residual_check_flags_large_residual()
    print("advanced implicit checks passed")
