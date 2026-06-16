from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from scaling_units_nondimensionalization.cli import (
    build_unit_records,
    build_scale_records,
    build_nondimensional_records,
)

def test_unit_records_present():
    assert len(build_unit_records()) >= 3

def test_scale_records_present():
    assert len(build_scale_records()) >= 2

def test_scaled_stock_value():
    records = {record.quantity_name: record for record in build_nondimensional_records()}
    assert abs(records["scaled_stock"].dimensionless_value - 0.4) < 1e-9

def test_scaled_time_positive():
    records = {record.quantity_name: record for record in build_nondimensional_records()}
    assert records["scaled_time"].dimensionless_value > 0
