from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from network_models_graph_structures.core import (
    Edge,
    NetworkRecord,
    build_adjacency,
    degree_table,
    network_risk_score,
    reachable_count,
    weak_component_count,
)


def sample_edges():
    return [
        Edge("a", "b", "dependency", 0.8, "high"),
        Edge("b", "c", "dependency", 0.5, "medium"),
        Edge("d", "e", "dependency", 0.2, "low"),
    ]


def test_reachability_counts_directed_paths():
    adjacency = build_adjacency(sample_edges())
    assert reachable_count("a", adjacency) == 2
    assert reachable_count("c", adjacency) == 0


def test_weak_component_count():
    assert weak_component_count(sample_edges()) == 2


def test_degree_table_has_all_nodes():
    rows = degree_table(sample_edges())
    nodes = {row["node"] for row in rows}
    assert nodes == {"a", "b", "c", "d", "e"}


def test_network_risk_score_positive():
    record = NetworkRecord("edge_weight", "edge_weight", "w_ij", "Weight represents dependency strength.", "How was weight estimated?", "review")
    assert network_risk_score(record) > 0
