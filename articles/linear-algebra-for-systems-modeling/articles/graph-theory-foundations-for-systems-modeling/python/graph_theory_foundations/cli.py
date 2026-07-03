from __future__ import annotations

import argparse
import csv
import heapq
import json
import math
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class GraphStructureAudit:
    graph_name: str
    node_count: int
    edge_count: int
    directed: bool
    weighted: bool
    component_count: int
    max_degree: int
    min_degree: int
    average_degree: float
    has_cycle: bool
    shortest_path_water_to_health: float
    graph_density: float
    representation_warning: str


def build_graph() -> tuple[list[str], list[tuple[str, str, float]]]:
    nodes = ["water", "power", "transport", "communications", "health"]
    edges = [
        ("water", "power", 1.0),
        ("power", "transport", 1.5),
        ("power", "communications", 0.8),
        ("transport", "communications", 1.2),
        ("communications", "health", 1.0),
        ("water", "health", 2.5),
    ]
    return nodes, edges


def adjacency_list(nodes: list[str], edges: list[tuple[str, str, float]]) -> dict[str, list[tuple[str, float]]]:
    graph = {node: [] for node in nodes}
    for source, target, weight in edges:
        graph[source].append((target, weight))
        graph[target].append((source, weight))
    return graph


def connected_components(nodes: list[str], graph: dict[str, list[tuple[str, float]]]) -> list[list[str]]:
    visited: set[str] = set()
    components: list[list[str]] = []
    for node in nodes:
        if node in visited:
            continue
        queue = deque([node])
        visited.add(node)
        component = []
        while queue:
            current = queue.popleft()
            component.append(current)
            for neighbor, _weight in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        components.append(sorted(component))
    return components


def dijkstra(graph: dict[str, list[tuple[str, float]]], source: str) -> dict[str, float]:
    distances = {node: math.inf for node in graph}
    distances[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        current_distance, node = heapq.heappop(heap)
        if current_distance > distances[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distances


def has_cycle_undirected(nodes: list[str], graph: dict[str, list[tuple[str, float]]]) -> bool:
    visited: set[str] = set()

    def dfs(node: str, parent: str | None) -> bool:
        visited.add(node)
        for neighbor, _weight in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for node in nodes:
        if node not in visited and dfs(node, None):
            return True
    return False


def write_edge_list(path: Path, edges: list[tuple[str, str, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target", "weight"])
        writer.writeheader()
        for source, target, weight in edges:
            writer.writerow({"source": source, "target": weight if False else target, "weight": weight})


def write_degree_table(path: Path, graph: dict[str, list[tuple[str, float]]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node", "degree", "weighted_degree"])
        writer.writeheader()
        for node, neighbors in sorted(graph.items()):
            writer.writerow({
                "node": node,
                "degree": len(neighbors),
                "weighted_degree": round(sum(weight for _neighbor, weight in neighbors), 8),
            })


def build_audit() -> tuple[GraphStructureAudit, list[str], list[tuple[str, str, float]], dict[str, list[tuple[str, float]]]]:
    nodes, edges = build_graph()
    graph = adjacency_list(nodes, edges)
    components = connected_components(nodes, graph)
    degrees = [len(graph[node]) for node in nodes]
    distances = dijkstra(graph, "water")
    n = len(nodes)
    possible_edges = n * (n - 1) / 2
    density = len(edges) / possible_edges

    audit = GraphStructureAudit(
        graph_name="synthetic_infrastructure_graph_foundations",
        node_count=n,
        edge_count=len(edges),
        directed=False,
        weighted=True,
        component_count=len(components),
        max_degree=max(degrees),
        min_degree=min(degrees),
        average_degree=round(sum(degrees) / n, 12),
        has_cycle=has_cycle_undirected(nodes, graph),
        shortest_path_water_to_health=round(distances["health"], 12),
        graph_density=round(density, 12),
        representation_warning=(
            "Graph conclusions depend on node definitions, edge definitions, graph boundary, "
            "direction conventions, weight semantics, missing edges, time period, and data provenance."
        ),
    )
    return audit, nodes, edges, graph


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, nodes, edges, graph = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "graph_structure_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    write_edge_list(output_dir / "tables" / "graph_edge_list.csv", edges)
    write_degree_table(output_dir / "tables" / "graph_degree_table.csv", graph)

    (output_dir / "json" / "graph_structure_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Graph structure audit complete.")


if __name__ == "__main__":
    main()
