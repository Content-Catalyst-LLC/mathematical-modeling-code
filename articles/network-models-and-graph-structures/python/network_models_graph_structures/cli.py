from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from network_models_graph_structures.core import (
    build_network_audit_card,
    degree_table,
    load_edges,
    load_network_records,
    network_risk_score,
    weak_component_count,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the network models and graph structures workflow.")
    parser.add_argument("--edge-file", type=Path, default=Path("data/infrastructure_edges.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/network_model_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    edges = load_edges(args.edge_file)
    records = load_network_records(args.register_file)

    edge_rows = [asdict(edge) for edge in edges]
    node_rows = degree_table(edges)
    register_rows = [{**asdict(item), "network_risk_score": network_risk_score(item)} for item in records]

    summary_rows = [{
        "node_count": len({edge.source for edge in edges} | {edge.target for edge in edges}),
        "edge_count": len(edges),
        "weak_component_count": weak_component_count(edges),
        "total_edge_weight": round(sum(edge.weight for edge in edges), 8),
        "high_evidence_edges": sum(1 for edge in edges if edge.evidence_quality.lower() == "high"),
        "medium_evidence_edges": sum(1 for edge in edges if edge.evidence_quality.lower() == "medium"),
        "low_evidence_edges": sum(1 for edge in edges if edge.evidence_quality.lower() == "low"),
    }]

    write_csv(tables_dir / "network_edge_list.csv", edge_rows)
    write_csv(tables_dir / "network_node_diagnostics.csv", node_rows)
    write_csv(tables_dir / "network_model_register.csv", register_rows)
    write_csv(tables_dir / "network_summary.csv", summary_rows)
    write_json(json_dir / "network_model_audit_card.json", build_network_audit_card(records, edges, node_rows))

    print("Network models and graph structures workflow complete.")
    print(f"Network records: {len(records)}")
    print(f"Edges: {len(edges)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
