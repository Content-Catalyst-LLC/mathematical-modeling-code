from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from power_series.cli import audit_geometric_series, geometric_power_series


def test_geometric_partial_sum():
    assert abs(geometric_power_series(0.5, 3) - 1.75) < 1e-12


def test_inside_radius_has_reference():
    record = audit_geometric_series(0.5, 10)
    assert record.reference_value is not None
    assert record.absolute_error is not None


def test_outside_radius_warns():
    record = audit_geometric_series(1.25, 10)
    assert record.reference_value is None
    assert "does not converge" in record.warning
