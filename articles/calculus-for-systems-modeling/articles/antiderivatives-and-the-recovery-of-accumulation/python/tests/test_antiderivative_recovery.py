from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from antiderivative_recovery.core import net_flow, trapezoid_recovery


def test_net_flow_positive_at_start():
    assert net_flow(0.0) == 5.0


def test_recovery_preserves_initial_condition():
    records = trapezoid_recovery([0, 1, 2], 100.0)
    assert records[0].recovered_stock == 100.0
    assert "baseline" in records[0].warning


def test_trapezoidal_recovery_increases_stock_for_positive_flow():
    records = trapezoid_recovery([0, 1, 2], 100.0)
    assert records[-1].recovered_stock > records[0].recovered_stock


def test_invalid_time_order_rejected():
    try:
        trapezoid_recovery([0, 1, 1], 100.0)
    except ValueError as exc:
        assert "strictly increasing" in str(exc)
    else:
        raise AssertionError("Expected ValueError for repeated time point")
