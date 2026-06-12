from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class NetworkRecord:
    key: str
    component_type: str
    expression_or_structure: str
    interpretation: str
    review_question: str
    status: str


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relationship: str
    weight: float
    evidence_quality: str


def validate_edge(edge: Edge) -> None:
    if not edge.source or not edge.target:
        raise ValueError("Edge source and target must be non-empty.")
    if edge.weight < 0:
        raise ValueError("Edge weight must be nonnegative.")
    if edge.evidence_quality.lower() not in {"high", "medium", "low"}:
        raise ValueError("Evidence quality must be high, medium, or low.")


def build_adjacency(edges: list[Edge]) -> dict[str, list[str]]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        validate_edge(edge)
        adjacency[edge.source].append(edge.target)
        adjacency.setdefault(edge.target, [])
    return dict(adjacency)


def reachable_count(start: str, adjacency: dict[str, list[str]]) -> int:
    seen = {start}
    queue: deque[str] = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) - 1


def weak_component_count(edges: list[Edge]) -> int:
    undirected: dict[str, set[str]] = defaultdict(set)
    nodes = set()
    for edge in edges:
        nodes.add(edge.source)
        nodes.add(edge.target)
        undirected[edge.source].add(edge.target)
        undirected[edge.target].add(edge.source)

    seen: set[str] = set()
    components = 0
    for node in sorted(nodes):
        if node in seen:
            continue
        components += 1
        queue: deque[str] = deque([node])
        seen.add(node)
        while queue:
            current = queue.popleft()
            for neighbor in undirected[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
    return components


def degree_table(edges: list[Edge]) -> list[dict[str, object]]:
    nodes = sorted({edge.source for edge in edges} | {edge.target for edge in edges})
    adjacency = build_adjacency(edges)
    incoming = {node: 0 for node in nodes}
    outgoing = {node: 0 for node in nodes}
    incoming_weight = {node: 0.0 for node in nodes}
    outgoing_weight = {node: 0.0 for node in nodes}

    for edge in edges:
        outgoing[edge.source] += 1
        incoming[edge.target] += 1
        outgoing_weight[edge.source] += edge.weight
        incoming_weight[edge.target] += edge.weight

    rows = []
    for node in nodes:
        rows.append({
            "node": node,
            "in_degree": incoming[node],
            "out_degree": outgoing[node],
            "total_degree": incoming[node] + outgoing[node],
            "weighted_in_degree": round(incoming_weight[node], 8),
            "weighted_out_degree": round(outgoing_weight[node], 8),
            "reachable_nodes": reachable_count(node, adjacency),
        })
    return rows


def network_risk_score(record: NetworkRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(record.status.lower(), 4.0)
    text = f"{record.component_type} {record.expression_or_structure} {record.review_question}".lower()
    for term in ["edge", "weight", "centrality", "direction", "critical", "dependency", "scale", "boundary"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_edges(path: Path) -> list[Edge]:
    edges = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            edge = Edge(row["source"], row["target"], row["relationship"], float(row["weight"]), row["evidence_quality"])
            validate_edge(edge)
            edges.append(edge)
    return edges


def load_network_records(path: Path) -> list[NetworkRecord]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(NetworkRecord(
                row["key"],
                row["component_type"],
                row["expression_or_structure"],
                row["interpretation"],
                row["review_question"],
                row["status"],
            ))
    return records


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def build_network_audit_card(records: list[NetworkRecord], edges: list[Edge], diagnostics: list[dict[str, object]]) -> dict[str, object]:
    register_rows = [{**asdict(record), "network_risk_score": network_risk_score(record)} for record in records]
    nodes = sorted({edge.source for edge in edges} | {edge.target for edge in edges})
    return {
        "article": "Network Models and Graph Structures",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "weak_component_count": weak_component_count(edges),
        "network_model_register": register_rows,
        "node_diagnostics": diagnostics,
        "high_priority_network_records": [row for row in register_rows if float(row["network_risk_score"]) >= 8.0],
        "audit_checks": [
            "nodes are defined at the correct scale",
            "edge meaning is documented",
            "edge direction and weight are validated",
            "centrality is interpreted cautiously",
            "network conclusions are tested against missing-edge uncertainty",
        ],
    }
