from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from infrastructure_network_models.cli import build_audit, impacted_capacity, build_assets, build_edges


def test_infrastructure_network_audit():
    audit, assets, edges = build_audit()
    assert audit.node_count == 6
    assert audit.edge_count == 7
    assert audit.layer_count == 6
    assert audit.critical_asset_count == 5
    assert audit.interdependency_edge_count == 3
    assert audit.total_baseline_capacity == 400.0


def test_disruption_capacity_loss():
    assets = build_assets()
    edges = build_edges()
    lost = impacted_capacity("power_substation", assets, edges)
    assert lost == 240.0


def test_capacity_loss_fraction():
    audit, assets, edges = build_audit()
    assert audit.remaining_capacity_after_disruption == 160.0
    assert audit.capacity_loss_fraction == 0.6
