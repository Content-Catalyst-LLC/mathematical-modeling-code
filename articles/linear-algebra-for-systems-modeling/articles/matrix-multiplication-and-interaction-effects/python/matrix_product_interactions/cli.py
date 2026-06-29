from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]

@dataclass(frozen=True)
class MatrixProductAudit:
    system_name: str
    left_shape: str
    right_shape: str
    product_shape: str
    product_matrix: str
    reverse_product_available: bool
    noncommutative_warning: str
    interaction_interpretation: str
    governance_warning: str

def shape(A: Matrix) -> tuple[int, int]:
    return len(A), len(A[0]) if A else 0

def matmul(A: Matrix, B: Matrix) -> Matrix:
    a_rows, a_cols = shape(A)
    b_rows, b_cols = shape(B)
    if a_cols != b_rows:
        raise ValueError(f"incompatible dimensions: {a_rows}x{a_cols} times {b_rows}x{b_cols}")
    return [[sum(A[i][k] * B[k][j] for k in range(a_cols)) for j in range(b_cols)] for i in range(a_rows)]

def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)

def build_audit() -> MatrixProductAudit:
    B = [[0.80, 0.20], [0.35, 0.60], [0.10, 0.50]]
    A = [[1.10, 0.40, 0.20], [0.25, 0.90, 0.70]]
    product = matmul(A, B)
    try:
        reverse_product = matmul(B, A)
        reverse_available = True
        noncommutative_warning = "reverse product is dimensionally available but represents a different transformation order" if reverse_product != product else "reverse product happens to match in this example"
    except ValueError:
        reverse_available = False
        noncommutative_warning = "reverse product is not dimensionally compatible"
    left_rows, left_cols = shape(A)
    right_rows, right_cols = shape(B)
    product_rows, product_cols = shape(product)
    return MatrixProductAudit(
        system_name="two_stage_demand_to_stress_interaction",
        left_shape=f"{left_rows}x{left_cols}",
        right_shape=f"{right_rows}x{right_cols}",
        product_shape=f"{product_rows}x{product_cols}",
        product_matrix=matrix_to_string(product),
        reverse_product_available=reverse_available,
        noncommutative_warning=noncommutative_warning,
        interaction_interpretation="B maps demand categories into intermediate components; A maps intermediate components into stress indicators; AB maps demand categories directly into stress indicators through all intermediate pathways.",
        governance_warning="Matrix products should document transformation order, intermediate-layer meaning, unit compatibility, row-column alignment, and whether indirect effects are substantively valid.",
    )

def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    row = asdict(build_audit())
    with (output_dir / "tables" / "matrix_product_interaction_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    (output_dir / "json" / "matrix_product_interaction_audit.json").write_text(json.dumps(row, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Matrix product interaction audit complete.")

if __name__ == "__main__":
    main()
