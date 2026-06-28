from __future__ import annotations
import csv, json, math
from pathlib import Path

MATRIX = [[0.80, 0.15], [0.20, 0.90]]

def determinant_2x2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

def trace_2x2(matrix):
    return matrix[0][0] + matrix[1][1]

def eigenvalues_2x2(matrix):
    trace = trace_2x2(matrix)
    determinant = determinant_2x2(matrix)
    root = math.sqrt(trace * trace - 4.0 * determinant)
    return ((trace + root) / 2.0, (trace - root) / 2.0)

def main():
    outputs = Path("outputs")
    outputs.mkdir(parents=True, exist_ok=True)
    eigen_1, eigen_2 = eigenvalues_2x2(MATRIX)
    result = {
        "determinant": determinant_2x2(MATRIX),
        "trace": trace_2x2(MATRIX),
        "eigenvalue_1": eigen_1,
        "eigenvalue_2": eigen_2,
        "dominant_eigenvalue": max(abs(eigen_1), abs(eigen_2)),
        "warning": "Calculator outputs require matrix meaning, units, scale, and model context."
    }
    with (outputs / "matrix_calculator_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys()))
        writer.writeheader()
        writer.writerow(result)
    (outputs / "matrix_calculator_results.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print("matrix calculator smoke test complete")

if __name__ == "__main__":
    main()
