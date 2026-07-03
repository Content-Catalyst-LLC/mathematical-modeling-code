from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from pagerank_network_influence.cli import build_audit, build_column_stochastic_matrix, build_graph, pagerank


def test_transition_matrix_is_column_stochastic():
    nodes, edges = build_graph()
    P, dangling = build_column_stochastic_matrix(nodes, edges)
    for col in range(len(nodes)):
        assert abs(sum(P[row][col] for row in range(len(nodes))) - 1.0) < 1e-12
    assert dangling == 0


def test_pagerank_converges_and_sums_to_one():
    nodes, edges = build_graph()
    P, _dangling = build_column_stochastic_matrix(nodes, edges)
    ranks, iterations, converged, log = pagerank(P)
    assert converged is True
    assert iterations <= 200
    assert abs(sum(ranks) - 1.0) < 1e-10


def test_audit_output():
    audit, nodes, edges, ranks, convergence_log = build_audit()
    assert audit.node_count == 5
    assert audit.edge_count == 8
    assert audit.converged is True
    assert audit.rank_sum == 1.0
    assert len(convergence_log) == audit.iterations
