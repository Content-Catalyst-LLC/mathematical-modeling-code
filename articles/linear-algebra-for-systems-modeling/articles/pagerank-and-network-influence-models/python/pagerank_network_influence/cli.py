from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]
Vector = list[float]


@dataclass(frozen=True)
class PageRankAudit:
    graph_name: str
    node_count: int
    edge_count: int
    damping_factor: float
    tolerance: float
    iterations: int
    converged: bool
    max_rank_node: str
    max_rank_score: float
    min_rank_node: str
    min_rank_score: float
    rank_sum: float
    dangling_node_count: int
    interpretation_warning: str


def build_graph() -> tuple[list[str], list[tuple[str, str]]]:
    nodes = ["water", "power", "transport", "communications", "health"]
    edges = [
        ("water", "power"),
        ("power", "transport"),
        ("power", "communications"),
        ("transport", "communications"),
        ("communications", "health"),
        ("health", "water"),
        ("transport", "water"),
        ("communications", "power"),
    ]
    return nodes, edges


def build_column_stochastic_matrix(nodes: list[str], edges: list[tuple[str, str]]) -> tuple[Matrix, int]:
    index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    P = [[0.0 for _ in nodes] for _ in nodes]
    out_degree = {node: 0 for node in nodes}
    for source, _target in edges:
        out_degree[source] += 1

    dangling_count = sum(1 for node in nodes if out_degree[node] == 0)

    for source, target in edges:
        P[index[target]][index[source]] += 1.0 / out_degree[source]

    for node in nodes:
        if out_degree[node] == 0:
            source_index = index[node]
            for target_index in range(n):
                P[target_index][source_index] = 1.0 / n

    return P, dangling_count


def matvec(P: Matrix, r: Vector) -> Vector:
    return [sum(P[i][j] * r[j] for j in range(len(r))) for i in range(len(P))]


def l1_distance(a: Vector, b: Vector) -> float:
    return sum(abs(x - y) for x, y in zip(a, b))


def pagerank(
    P: Matrix,
    damping: float = 0.85,
    tolerance: float = 1e-10,
    max_iterations: int = 200,
) -> tuple[Vector, int, bool, list[dict[str, float]]]:
    n = len(P)
    r = [1.0 / n for _ in range(n)]
    teleport = [1.0 / n for _ in range(n)]
    log: list[dict[str, float]] = []

    for iteration in range(1, max_iterations + 1):
        moved = matvec(P, r)
        next_r = [damping * moved[i] + (1.0 - damping) * teleport[i] for i in range(n)]
        residual = l1_distance(next_r, r)
        log.append({"iteration": iteration, "l1_residual": residual})
        r = next_r
        if residual < tolerance:
            return r, iteration, True, log

    return r, max_iterations, False, log


def write_rank_table(path: Path, nodes: list[str], ranks: Vector) -> None:
    rows = sorted(
        [{"node": node, "rank": rank} for node, rank in zip(nodes, ranks)],
        key=lambda row: row["rank"],
        reverse=True,
    )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node", "rank"])
        writer.writeheader()
        for row in rows:
            writer.writerow({"node": row["node"], "rank": round(row["rank"], 12)})


def write_convergence_log(path: Path, log: list[dict[str, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["iteration", "l1_residual"])
        writer.writeheader()
        for row in log:
            writer.writerow({"iteration": row["iteration"], "l1_residual": f"{row['l1_residual']:.12e}"})


def build_audit() -> tuple[PageRankAudit, list[str], list[tuple[str, str]], Vector, list[dict[str, float]]]:
    nodes, edges = build_graph()
    P, dangling_count = build_column_stochastic_matrix(nodes, edges)
    damping = 0.85
    tolerance = 1e-10
    ranks, iterations, converged, convergence_log = pagerank(P, damping=damping, tolerance=tolerance)

    rank_rows = list(zip(nodes, ranks))
    max_node, max_rank = max(rank_rows, key=lambda item: item[1])
    min_node, min_rank = min(rank_rows, key=lambda item: item[1])

    audit = PageRankAudit(
        graph_name="synthetic_directed_network_influence_model",
        node_count=len(nodes),
        edge_count=len(edges),
        damping_factor=damping,
        tolerance=tolerance,
        iterations=iterations,
        converged=converged,
        max_rank_node=max_node,
        max_rank_score=round(max_rank, 12),
        min_rank_node=min_node,
        min_rank_score=round(min_rank, 12),
        rank_sum=round(sum(ranks), 12),
        dangling_node_count=dangling_count,
        interpretation_warning=(
            "PageRank scores depend on node definitions, directed-edge meaning, transition normalization, "
            "dangling-node handling, damping factor, teleportation vector, convergence tolerance, graph boundary, "
            "and data provenance. Rank is a model-specific influence score, not automatic importance."
        ),
    )
    return audit, nodes, edges, ranks, convergence_log


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, nodes, edges, ranks, convergence_log = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "pagerank_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "directed_edge_list.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "target"])
        writer.writeheader()
        for source, target in edges:
            writer.writerow({"source": source, "target": target})

    write_rank_table(output_dir / "tables" / "pagerank_scores.csv", nodes, ranks)
    write_convergence_log(output_dir / "tables" / "pagerank_convergence_log.csv", convergence_log)

    (output_dir / "json" / "pagerank_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("PageRank audit complete.")


if __name__ == "__main__":
    main()
