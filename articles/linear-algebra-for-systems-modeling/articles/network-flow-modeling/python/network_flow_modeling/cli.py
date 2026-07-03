from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class EdgeFlowRecord:
    source: str
    target: str
    capacity: float
    cost: float
    flow: float


@dataclass(frozen=True)
class NetworkFlowAudit:
    graph_name: str
    node_count: int
    edge_count: int
    source_node: str
    sink_node: str
    total_source_outflow: float
    total_sink_inflow: float
    capacity_violations: int
    saturated_edge_count: int
    max_absolute_transshipment_imbalance: float
    total_flow_cost: float
    interpretation_warning: str


def build_network() -> tuple[list[str], list[EdgeFlowRecord]]:
    nodes = ["source", "north_hub", "south_hub", "transfer", "sink"]
    edges = [
        EdgeFlowRecord("source", "north_hub", 12.0, 2.0, 10.0),
        EdgeFlowRecord("source", "south_hub", 8.0, 3.0, 6.0),
        EdgeFlowRecord("north_hub", "transfer", 7.0, 1.0, 6.0),
        EdgeFlowRecord("north_hub", "sink", 5.0, 4.0, 4.0),
        EdgeFlowRecord("south_hub", "transfer", 6.0, 2.0, 6.0),
        EdgeFlowRecord("transfer", "sink", 12.0, 1.0, 12.0),
    ]
    return nodes, edges


def node_balances(nodes: list[str], edges: list[EdgeFlowRecord]) -> dict[str, float]:
    balances = {node: 0.0 for node in nodes}
    for edge in edges:
        balances[edge.source] -= edge.flow
        balances[edge.target] += edge.flow
    return balances


def build_audit() -> tuple[NetworkFlowAudit, list[str], list[EdgeFlowRecord], dict[str, float]]:
    nodes, edges = build_network()
    balances = node_balances(nodes, edges)

    source = "source"
    sink = "sink"
    transshipment_nodes = [node for node in nodes if node not in {source, sink}]
    capacity_violations = sum(1 for edge in edges if edge.flow < -1e-12 or edge.flow - edge.capacity > 1e-12)
    saturated_edge_count = sum(1 for edge in edges if abs(edge.flow - edge.capacity) < 1e-12)
    max_transshipment_imbalance = max(abs(balances[node]) for node in transshipment_nodes)
    total_flow_cost = sum(edge.cost * edge.flow for edge in edges)

    audit = NetworkFlowAudit(
        graph_name="synthetic_capacitated_flow_network",
        node_count=len(nodes),
        edge_count=len(edges),
        source_node=source,
        sink_node=sink,
        total_source_outflow=round(-balances[source], 12),
        total_sink_inflow=round(balances[sink], 12),
        capacity_violations=capacity_violations,
        saturated_edge_count=saturated_edge_count,
        max_absolute_transshipment_imbalance=round(max_transshipment_imbalance, 12),
        total_flow_cost=round(total_flow_cost, 12),
        interpretation_warning=(
            "Network flow results depend on node definitions, edge definitions, capacity units, "
            "flow units, cost semantics, source-sink choices, conservation assumptions, time scale, "
            "solver settings, uncertainty, and data provenance."
        ),
    )
    return audit, nodes, edges, balances


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, nodes, edges, balances = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "network_flow_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "edge_flow_table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "capacity", "cost", "flow", "slack", "saturated"])
        writer.writeheader()
        for edge in edges:
            writer.writerow({
                "source": edge.source,
                "target": edge.target,
                "capacity": edge.capacity,
                "cost": edge.cost,
                "flow": edge.flow,
                "slack": round(edge.capacity - edge.flow, 12),
                "saturated": abs(edge.capacity - edge.flow) < 1e-12,
            })

    with (output_dir / "tables" / "node_balance_table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node", "balance"])
        writer.writeheader()
        for node in nodes:
            writer.writerow({"node": node, "balance": round(balances[node], 12)})

    (output_dir / "json" / "network_flow_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Network flow audit complete.")


if __name__ == "__main__":
    main()
