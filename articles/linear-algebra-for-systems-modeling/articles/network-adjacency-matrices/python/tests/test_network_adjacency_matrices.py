from pathlib import Path
import sys
ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))
from network_adjacency_matrices.cli import build_audit, count_nonzero, row_sums, col_sums, matmul

def test_basic_adjacency_counts():
    audit, node_names, A, A2, P = build_audit()
    assert audit.node_count == 5
    assert audit.edge_count == 20
    assert count_nonzero(A) == 20
    assert audit.diagonal_nonzero_count == 0

def test_degree_and_normalization():
    audit, node_names, A, A2, P = build_audit()
    assert round(max(row_sums(A)), 6) == 2.15
    assert round(max(col_sums(A)), 6) == 1.95
    for row in P:
        assert abs(sum(row) - 1.0) < 1e-9

def test_matrix_powers():
    audit, node_names, A, A2, P = build_audit()
    assert A2 == matmul(A, A)
    assert audit.two_step_walk_total > 0
