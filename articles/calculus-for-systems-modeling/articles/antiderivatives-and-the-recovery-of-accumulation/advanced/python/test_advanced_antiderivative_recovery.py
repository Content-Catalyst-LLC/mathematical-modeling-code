from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_antiderivative_recovery import (
    domain_interval_check,
    initial_condition_check,
    missing_flow_check,
    time_grid_check,
    unit_consistency_check,
)


def test_initial_condition_missing_fails():
    assert initial_condition_check(0.0).passed is False


def test_unit_consistency_missing_fails():
    assert unit_consistency_check(0.0).passed is False


def test_large_time_grid_fails():
    assert time_grid_check(5.0).passed is False


def test_missing_flow_review_fails():
    assert missing_flow_check(0.0).passed is False


def test_domain_interval_missing_fails():
    assert domain_interval_check(0.0).passed is False


if __name__ == "__main__":
    test_initial_condition_missing_fails()
    test_unit_consistency_missing_fails()
    test_large_time_grid_fails()
    test_missing_flow_review_fails()
    test_domain_interval_missing_fails()
    print("advanced antiderivative recovery checks passed")
