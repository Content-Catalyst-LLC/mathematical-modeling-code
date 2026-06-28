from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class MatrixSystemRecord:
    model_name: str
    rows: int
    columns: int
    rank: int
    determinant: float | None
    trace: float | None
    dominant_eigenvalue: float | None
    matrix_meaning: str
    interpretation_warning: str

def determinant_2x2(matrix: list[list[float]]) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

def trace_2x2(matrix: list[list[float]]) -> float:
    return matrix[0][0] + matrix[1][1]

def eigenvalues_2x2(matrix: list[list[float]]) -> tuple[float, float]:
    trace = trace_2x2(matrix)
    determinant = determinant_2x2(matrix)
    discriminant = trace * trace - 4.0 * determinant
    if discriminant < 0:
        return (float("nan"), float("nan"))
    root = math.sqrt(discriminant)
    return ((trace + root) / 2.0, (trace - root) / 2.0)

def rank_2x2(matrix: list[list[float]], tolerance: float = 1e-10) -> int:
    if abs(determinant_2x2(matrix)) > tolerance:
        return 2
    nonzero = any(abs(value) > tolerance for row in matrix for value in row)
    return 1 if nonzero else 0

def build_record() -> MatrixSystemRecord:
    matrix = [[0.80, 0.15], [0.20, 0.90]]
    eigen_1, eigen_2 = eigenvalues_2x2(matrix)
    dominant = max(abs(eigen_1), abs(eigen_2))
    return MatrixSystemRecord(
        model_name="two_component_transition_model",
        rows=2,
        columns=2,
        rank=rank_2x2(matrix),
        determinant=determinant_2x2(matrix),
        trace=trace_2x2(matrix),
        dominant_eigenvalue=dominant,
        matrix_meaning="transition-like matrix connecting two system components across a modeling step",
        interpretation_warning=(
            "Matrix interpretation depends on what entries represent, how variables are scaled, "
            "and whether a linear transformation is appropriate for the modeled system."
        ),
    )

def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    record = build_record()
    row = asdict(record)
    with (output_dir / "tables" / "linear_algebra_matrix_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)
    (output_dir / "json" / "linear_algebra_matrix_audit.json").write_text(json.dumps(row, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Linear algebra matrix audit complete.")

if __name__ == "__main__":
    main()
