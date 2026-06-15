from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_integration_by_parts import (
    boundary_interpretation_check,
    causal_claim_check,
    residual_interpretation_check,
    residual_tolerance_check,
    unit_consistency_check,
)


def test_large_residual_fails():
    assert residual_tolerance_check(0.1).passed is False


def test_missing_unit_check_fails():
    assert unit_consistency_check(0.0).passed is False


def test_missing_boundary_interpretation_fails():
    assert boundary_interpretation_check(0.0).passed is False


def test_missing_residual_interpretation_fails():
    assert residual_interpretation_check(0.0).passed is False


def test_causal_overclaim_fails():
    assert causal_claim_check(1.0).passed is False


if __name__ == "__main__":
    test_large_residual_fails()
    test_missing_unit_check_fails()
    test_missing_boundary_interpretation_fails()
    test_missing_residual_interpretation_fails()
    test_causal_overclaim_fails()
    print("advanced integration-by-parts checks passed")
