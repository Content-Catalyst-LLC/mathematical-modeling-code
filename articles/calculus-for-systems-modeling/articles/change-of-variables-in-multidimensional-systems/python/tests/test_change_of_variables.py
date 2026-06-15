from pathlib import Path
import sys
import math

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from change_of_variables.cli import audit_change_of_variables, exposure_cartesian, exposure_polar, polar_total

def test_exposure_origin():
    assert exposure_cartesian(0.0, 0.0) == 20.0

def test_exposure_consistency():
    assert abs(exposure_cartesian(3.0, 0.0) - exposure_polar(3.0, 0.0)) < 1e-12

def test_polar_total_positive():
    assert polar_total(3.0, 0.5, math.pi / 24.0) > 0

def test_audit_difference_nonnegative():
    record = audit_change_of_variables(3.0, 0.5, math.pi / 24.0, "test")
    assert record.absolute_difference >= 0
    assert record.relative_difference >= 0

def test_jacobian_rule_present():
    record = audit_change_of_variables(3.0, 0.5, math.pi / 24.0, "test")
    assert "r" in record.jacobian_rule
