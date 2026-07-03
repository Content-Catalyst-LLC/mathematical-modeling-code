from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from incidence_structure.cli import build_audit, count_nonzero, matvec, rank_via_row_reduction


def test_incidence_structure_counts():
    audit, node_names, edge_names, B, L, balances = build_audit()
    assert audit.node_count == 4
    assert audit.edge_count == 5
    assert count_nonzero(B) == 10
    assert audit.incidence_density == 0.5


def test_node_balance_and_laplacian():
    audit, node_names, edge_names, B, L, balances = build_audit()
    assert round(sum(balances), 8) == 0.0
    assert audit.max_absolute_node_balance == 9.0
    assert audit.laplacian_trace == 10.0


def test_rank_estimate():
    audit, node_names, edge_names, B, L, balances = build_audit()
    assert rank_via_row_reduction(B) == 3
    assert audit.rank_estimate == 3
