from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from flow_to_stock.core import FlowRecord, audit_flow_to_stock, sample_records


def test_sample_records_exist():
    assert len(sample_records()) == 5


def test_audit_ending_stock_identity():
    audit = audit_flow_to_stock(50.0, sample_records())
    assert audit.ending_stock == audit.initial_stock + audit.net_accumulation


def test_net_accumulation_identity():
    audit = audit_flow_to_stock(50.0, sample_records())
    assert audit.net_accumulation == audit.cumulative_inflow - audit.cumulative_outflow


def test_exposure_positive():
    audit = audit_flow_to_stock(50.0, sample_records())
    assert audit.cumulative_exposure > 0
    assert audit.population_weighted_exposure > audit.cumulative_exposure


def test_rejects_nonpositive_duration():
    records = [FlowRecord(1, 0.0, 1.0, 0.0, 2.0, 10.0)]
    try:
        audit_flow_to_stock(0.0, records)
    except ValueError as exc:
        assert "durations" in str(exc)
    else:
        raise AssertionError("Expected ValueError for nonpositive duration")
