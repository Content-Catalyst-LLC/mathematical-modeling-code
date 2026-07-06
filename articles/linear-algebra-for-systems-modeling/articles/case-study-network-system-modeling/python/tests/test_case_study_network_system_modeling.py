from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from case_study_network_system_modeling.cli import build_audit


def test_network_audit_counts():
    audit = build_audit()
    assert audit.node_count == 5
    assert audit.edge_count == 6
    assert audit.total_weight == 17.0


def test_network_weighted_degree_and_laplacian_trace():
    audit = build_audit()
    assert audit.highest_weighted_degree_node == "B"
    assert audit.highest_weighted_degree == 12.0
    assert audit.laplacian_trace == 34.0


def test_network_stress_test_preserves_connectivity_in_this_case():
    audit = build_audit()
    assert audit.baseline_component_count == 1
    assert audit.stressed_component_count == 1
    assert audit.removed_edge == "B-D"
