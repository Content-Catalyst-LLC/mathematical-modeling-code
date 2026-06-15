from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_inverse import derivative_invertibility_check, domain_check, jacobian_conditioning_check, residual_check


def test_derivative_check_flags_zero():
    assert derivative_invertibility_check(0.0).passed is False


def test_conditioning_check_flags_large_condition_number():
    assert jacobian_conditioning_check(1e10).passed is False


def test_domain_check_flags_outside_domain():
    assert domain_check(-2.0, -1.0).passed is False


def test_residual_check_flags_large_residual():
    assert residual_check(1e-2).passed is False


if __name__ == "__main__":
    test_derivative_check_flags_zero()
    test_conditioning_check_flags_large_condition_number()
    test_domain_check_flags_outside_domain()
    test_residual_check_flags_large_residual()
    print("advanced inverse checks passed")
