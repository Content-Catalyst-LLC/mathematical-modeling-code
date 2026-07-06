from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class NetworkSystemAudit:
    workflow_name: str
    network_name: str
    node_count: int
    edge_count: int
    total_weight: float
    highest_weighted_degree_node: str
    highest_weighted_degree: float
    laplacian_trace: float
    baseline_component_count: int
    stressed_component_count: int
    removed_edge: str
    vulnerability_warning: str
    interpretation_warning: str


NODES = ["A", "B", "C", "D", "E"]

EDGES = [
    ("A", "B", 4.0),
    ("A", "C", 2.0),
    ("B", "C", 3.0),
    ("B", "D", 5.0),
    ("C", "D", 1.0),
    ("D", "E", 2.0),
]


def empty_matrix(n: int) -> list[list[float]]:
    return [[0.0 for _ in range(n)] for _ in range(n)]


def adjacency_matrix(edges: list[tuple[str, str, float]]) -> list[list[float]]:
    index = {node: i for i, node in enumerate(NODES)}
    A = empty_matrix(len(NODES))
    for u, v, weight in edges:
        i = index[u]
        j = index[v]
        A[i][j] = weight
        A[j][i] = weight
    return A


def weighted_degrees(A: list[list[float]]) -> list[float]:
    return [sum(row) for row in A]


def laplacian(A: list[list[float]]) -> list[list[float]]:
    degrees = weighted_degrees(A)
    L = empty_matrix(len(A))
    for i in range(len(A)):
        for j in range(len(A)):
            if i == j:
                L[i][j] = degrees[i]
            else:
                L[i][j] = -A[i][j]
    return L


def component_count(A: list[list[float]]) -> int:
    n = len(A)
    visited = [False] * n

    def dfs(start: int) -> None:
        stack = [start]
        while stack:
            node = stack.pop()
            if visited[node]:
                continue
            visited[node] = True
            for neighbor, weight in enumerate(A[node]):
                if weight > 0 and not visited[neighbor]:
                    stack.append(neighbor)

    count = 0
    for i in range(n):
        if not visited[i]:
            count += 1
            dfs(i)
    return count


def remove_edge(edges: list[tuple[str, str, float]], edge_to_remove: tuple[str, str]) -> list[tuple[str, str, float]]:
    u0, v0 = edge_to_remove
    return [(u, v, weight) for u, v, weight in edges if {u, v} != {u0, v0}]


def build_audit() -> NetworkSystemAudit:
    A = adjacency_matrix(EDGES)
    degrees = weighted_degrees(A)
    L = laplacian(A)

    highest_index = max(range(len(NODES)), key=lambda i: degrees[i])
    total_weight = sum(weight for _, _, weight in EDGES)

    stressed_edges = remove_edge(EDGES, ("B", "D"))
    A_stressed = adjacency_matrix(stressed_edges)

    return NetworkSystemAudit(
        workflow_name="network_system_modeling_audit",
        network_name="synthetic_infrastructure_service_network",
        node_count=len(NODES),
        edge_count=len(EDGES),
        total_weight=round(total_weight, 12),
        highest_weighted_degree_node=NODES[highest_index],
        highest_weighted_degree=round(degrees[highest_index], 12),
        laplacian_trace=round(sum(L[i][i] for i in range(len(L))), 12),
        baseline_component_count=component_count(A),
        stressed_component_count=component_count(A_stressed),
        removed_edge="B-D",
        vulnerability_warning="The edge-removal scenario changes network structure under one simplified stress test. It does not predict real failure behavior without capacity, timing, redundancy, and domain validation.",
        interpretation_warning="Network metrics depend on node definitions, edge meanings, weights, directionality, boundary choices, and missing-edge assumptions. Centrality and vulnerability should be interpreted only within that representation.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "network_system_modeling_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "network_system_modeling_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Network System Modeling Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Network: {audit.network_name}",
        f"- Node count: {audit.node_count}",
        f"- Edge count: {audit.edge_count}",
        f"- Total edge weight: {audit.total_weight}",
        f"- Highest weighted-degree node: {audit.highest_weighted_degree_node}",
        f"- Highest weighted degree: {audit.highest_weighted_degree}",
        f"- Laplacian trace: {audit.laplacian_trace}",
        f"- Baseline component count: {audit.baseline_component_count}",
        f"- Stressed component count: {audit.stressed_component_count}",
        f"- Removed edge: {audit.removed_edge}",
        "",
        audit.vulnerability_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "network_system_modeling_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Network system modeling audit complete.")


if __name__ == "__main__":
    main()
