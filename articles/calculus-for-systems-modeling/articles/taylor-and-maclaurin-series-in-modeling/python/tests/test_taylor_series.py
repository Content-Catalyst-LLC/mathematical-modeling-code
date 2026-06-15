from pathlib import Path
import sys
import math

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from taylor_series.cli import audit_exp, audit_sin, taylor_exp_maclaurin


def test_exp_order_zero():
    assert abs(taylor_exp_maclaurin(2.0, 0) - 1.0) < 1e-12


def test_exp_error_decreases():
    low = audit_exp(1.0, 2).absolute_error
    high = audit_exp(1.0, 8).absolute_error
    assert high < low


def test_sin_reasonable():
    record = audit_sin(1.0, 8)
    assert abs(record.approximation - math.sin(1.0)) < 1e-8
