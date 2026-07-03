from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from graph_theory_foundations.cli import build_audit, connected_components, dijkstra, has_cycle_undirected


def test_graph_structure_audit():
    audit, nodes, edges, graph = build_audit()
    assert audit.node_count == 5
    assert audit.edge_count == 6
    assert audit.component_count == 1
    assert audit.has_cycle is True
    assert audit.max_degree == 3
    assert audit.min_degree == 2


def test_shortest_path():
    audit, nodes, edges, graph = build_audit()
    distances = dijkstra(graph, "water")
    assert round(distances["health"], 6) == 2.5
    assert audit.shortest_path_water_to_health == 2.5


def test_components_and_cycles():
    audit, nodes, edges, graph = build_audit()
    assert connected_components(nodes, graph) == [["communications", "health", "power", "transport", "water"]]
    assert has_cycle_undirected(nodes, graph) is True
