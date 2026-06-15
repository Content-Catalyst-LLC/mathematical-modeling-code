from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
sys.path.insert(0, str(CURRENT.parent))

from advanced_flow_to_stock import (
    exposure_window_check,
    gross_flow_reporting_check,
    initial_stock_check,
    sign_convention_check,
    unit_consistency_check,
)


def test_missing_initial_stock_fails():
    assert initial_stock_check(0.0).passed is False


def test_missing_sign_convention_fails():
    assert sign_convention_check(0.0).passed is False


def test_missing_gross_flow_reporting_fails():
    assert gross_flow_reporting_check(0.0).passed is False


def test_missing_exposure_window_fails():
    assert exposure_window_check(0.0).passed is False


def test_missing_unit_check_fails():
    assert unit_consistency_check(0.0).passed is False


if __name__ == "__main__":
    test_missing_initial_stock_fails()
    test_missing_sign_convention_fails()
    test_missing_gross_flow_reporting_fails()
    test_missing_exposure_window_fails()
    test_missing_unit_check_fails()
    print("advanced flow-to-stock checks passed")
