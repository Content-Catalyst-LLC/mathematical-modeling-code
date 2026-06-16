from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from initial_conditions_boundary_scope.cli import (
    build_boundary_conditions,
    build_initial_conditions,
    build_scope_records,
)

def test_initial_conditions_present():
    assert len(build_initial_conditions()) >= 2

def test_boundary_conditions_present():
    assert len(build_boundary_conditions()) >= 2

def test_scope_records_include_temporal_scope():
    dimensions = {record.scope_dimension for record in build_scope_records()}
    assert "temporal_scope" in dimensions

def test_boundary_warning_present():
    assert all(record.warning for record in build_boundary_conditions())
