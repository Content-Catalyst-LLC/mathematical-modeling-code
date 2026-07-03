from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]
Vector = list[float]


@dataclass(frozen=True)
class IncidenceStructureAudit:
    graph_name: str
    node_count: int
    edge_count: int
    directed_convention: str
    signed_incidence: bool
    nonzero_incidence_entries: int
    incidence_density: float
    max_absolute_node_balance: float
    laplacian_trace: float
    rank_estimate: int
    flow_conservation_warning: str
    representation_warning: str


def transpose(A: Matrix) -> Matrix:
    return [list(row) for row in zip(*A)]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def matvec(A: Matrix, x: Vector) -> Vector:
    return [sum(A[i][j] * x[j] for j in range(len(x))) for i in range(len(A))]


def count_nonzero(A: Matrix) -> int:
    return sum(1 for row in A for value in row if value != 0.0)


def trace(A: Matrix) -> float:
    return sum(A[i][i] for i in range(min(len(A), len(A[0]))))


def rank_via_row_reduction(A: Matrix, tolerance: float = 1e-10) -> int:
    M = [row[:] for row in A]
    rows = len(M)
    cols = len(M[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for r in range(rank, rows):
            if abs(M[r][col]) > tolerance:
                pivot = r
                break
        if pivot is None:
            continue
        M[rank], M[pivot] = M[pivot], M[rank]
        pivot_value = M[rank][col]
        M[rank] = [value / pivot_value for value in M[rank]]
        for r in range(rows):
            if r != rank and abs(M[r][col]) > tolerance:
                factor = M[r][col]
                M[r] = [M[r][c] - factor * M[rank][c] for c in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def write_matrix_csv(path: Path, row_names: list[str], col_names: list[str], A: Matrix) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["row"] + col_names)
        for name, row in zip(row_names, A):
            writer.writerow([name] + [round(value, 8) for value in row])


def build_incidence(node_names: list[str], edges: list[tuple[str, str, float]]) -> Matrix:
    node_index = {node: i for i, node in enumerate(node_names)}
    B = [[0.0 for _ in edges] for _ in node_names]
    for edge_index, (source, target, _weight) in enumerate(edges):
        B[node_index[source]][edge_index] = -1.0
        B[node_index[target]][edge_index] = 1.0
    return B


def build_audit() -> tuple[IncidenceStructureAudit, list[str], list[str], Matrix, Matrix, Vector]:
    node_names = ["water", "power", "transport", "communications"]
    edges = [
        ("water", "power", 0.75),
        ("power", "transport", 0.60),
        ("power", "communications", 0.80),
        ("transport", "communications", 0.45),
        ("communications", "water", 0.30),
    ]
    edge_names = [f"e{i+1}_{source}_to_{target}" for i, (source, target, _weight) in enumerate(edges)]

    B = build_incidence(node_names, edges)
    flows = [12.0, 9.0, 5.0, 4.0, 3.0]
    balances = matvec(B, flows)
    L = matmul(B, transpose(B))
    nonzero = count_nonzero(B)
    density = nonzero / (len(B) * len(B[0]))

    audit = IncidenceStructureAudit(
        graph_name="synthetic_infrastructure_incidence_graph",
        node_count=len(node_names),
        edge_count=len(edges),
        directed_convention="B[v,e] = -1 at source/tail and +1 at target/head.",
        signed_incidence=True,
        nonzero_incidence_entries=nonzero,
        incidence_density=round(density, 12),
        max_absolute_node_balance=round(max(abs(value) for value in balances), 12),
        laplacian_trace=round(trace(L), 12),
        rank_estimate=rank_via_row_reduction(B),
        flow_conservation_warning=(
            "Node balances are computed from synthetic edge flows. Interpreting imbalance requires "
            "source, sink, storage, and boundary assumptions."
        ),
        representation_warning=(
            "Incidence structure depends on node definitions, edge definitions, sign convention, "
            "edge direction, weight semantics, data provenance, and conservation assumptions."
        ),
    )
    return audit, node_names, edge_names, B, L, balances


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, node_names, edge_names, B, L, balances = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "incidence_structure_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    write_matrix_csv(output_dir / "tables" / "oriented_incidence_matrix.csv", node_names, edge_names, B)
    write_matrix_csv(output_dir / "tables" / "graph_laplacian_from_incidence.csv", node_names, node_names, L)

    with (output_dir / "tables" / "node_balance_from_edge_flows.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node", "balance"])
        writer.writeheader()
        for node, balance in zip(node_names, balances):
            writer.writerow({"node": node, "balance": round(balance, 8)})

    (output_dir / "json" / "incidence_structure_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Incidence structure audit complete.")


if __name__ == "__main__":
    main()
