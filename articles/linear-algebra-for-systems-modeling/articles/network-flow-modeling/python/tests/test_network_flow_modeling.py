from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from network_flow_modeling.cli import build_audit, node_balances


def test_network_flow_audit():
    audit, nodes, edges, balances = build_audit()
    assert audit.node_count == 5
    assert audit.edge_count == 6
    assert audit.capacity_violations == 0
    assert audit.saturated_edge_count == 2
    assert audit.total_source_outflow == 16.0
    assert audit.total_sink_inflow == 16.0


def test_transshipment_balance():
    audit, nodes, edges, balances = build_audit()
    for node in ["north_hub", "south_hub", "transfer"]:
        assert abs(balances[node]) < 1e-12
    assert audit.max_absolute_transshipment_imbalance == 0.0


def test_cost():
    audit, nodes, edges, balances = build_audit()
    assert audit.total_flow_cost == 82.0
