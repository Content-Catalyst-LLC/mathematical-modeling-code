from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path
Matrix = list[list[float]]

@dataclass(frozen=True)
class NetworkAdjacencyAudit:
    network_name: str
    node_count: int
    edge_count: int
    directed: bool
    weighted: bool
    diagonal_nonzero_count: int
    density: float
    max_out_weight: float
    max_in_weight: float
    two_step_walk_total: float
    row_normalized: bool
    direction_convention: str
    weight_meaning: str
    interpretation_warning: str

def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def row_sums(A: Matrix) -> list[float]: return [sum(row) for row in A]
def col_sums(A: Matrix) -> list[float]: return [sum(A[i][j] for i in range(len(A))) for j in range(len(A[0]))]
def count_nonzero(A: Matrix) -> int: return sum(1 for row in A for value in row if value != 0.0)
def diagonal_nonzero_count(A: Matrix) -> int: return sum(1 for i in range(min(len(A), len(A[0]))) if A[i][i] != 0.0)
def row_normalize(A: Matrix) -> Matrix:
    return [[0.0 for _ in row] if sum(row)==0 else [v/sum(row) for v in row] for row in A]
def write_matrix_csv(path: Path, node_names: list[str], A: Matrix) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["node"] + node_names)
        for node, row in zip(node_names, A):
            writer.writerow([node] + [round(value, 8) for value in row])

def build_audit():
    node_names = ["water", "power", "transport", "communications", "health"]
    A = [[0.00,0.75,0.20,0.10,0.30],[0.15,0.00,0.65,0.80,0.55],[0.10,0.25,0.00,0.35,0.40],[0.05,0.45,0.30,0.00,0.25],[0.20,0.30,0.35,0.40,0.00]]
    n = len(A); edge_count = count_nonzero(A); A2 = matmul(A, A); P = row_normalize(A)
    audit = NetworkAdjacencyAudit("synthetic_infrastructure_dependency_network", n, edge_count, True, True, diagonal_nonzero_count(A), round(edge_count/(n*n),12), round(max(row_sums(A)),12), round(max(col_sums(A)),12), round(sum(sum(row) for row in A2),12), True, "A[i][j] means dependency or influence from row node i to column node j.", "Synthetic edge weights represent relative dependency strength, not physical capacity.", "Adjacency conclusions depend on node boundaries, edge definitions, direction conventions, weight meaning, missing-edge assumptions, time variation, and data provenance.")
    return audit, node_names, A, A2, P

def write_outputs(output_dir: Path) -> None:
    (output_dir/"tables").mkdir(parents=True, exist_ok=True); (output_dir/"json").mkdir(parents=True, exist_ok=True)
    audit, node_names, A, A2, P = build_audit(); row = asdict(audit)
    with (output_dir/"tables/network_adjacency_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys())); writer.writeheader(); writer.writerow(row)
    write_matrix_csv(output_dir/"tables/adjacency_matrix.csv", node_names, A)
    write_matrix_csv(output_dir/"tables/two_step_walk_matrix.csv", node_names, A2)
    write_matrix_csv(output_dir/"tables/row_normalized_transition_matrix.csv", node_names, P)
    (output_dir/"json/network_adjacency_audit.json").write_text(json.dumps(row, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--output-dir", type=Path, default=Path("outputs")); args = parser.parse_args()
    write_outputs(args.output_dir); print("Network adjacency audit complete.")
if __name__ == "__main__": main()
