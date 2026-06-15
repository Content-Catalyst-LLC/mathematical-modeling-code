from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from approximation_error.cli import audit_exp, taylor_exp_maclaurin


def test_order_zero_exp():
    assert abs(taylor_exp_maclaurin(2.0, 0) - 1.0) < 1e-12


def test_error_decreases_with_order():
    low = audit_exp(1.0, 2).absolute_error
    high = audit_exp(1.0, 8).absolute_error
    assert high < low


def test_far_center_warning():
    record = audit_exp(3.0, 10)
    assert "local validity" in record.warning
