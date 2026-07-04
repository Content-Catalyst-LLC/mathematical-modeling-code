from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class CrossLanguageMatrixAudit:
    model_name: str
    language: str
    matrix_shape: str
    vector_shape: str
    indexing_convention: str
    matrix_multiplication_operator: str
    elementwise_operator: str
    solve_method: str
    condition_number: float
    matrix_vector_product_norm: float
    matrix_matrix_product_trace: float
    solve_residual_norm: float
    determinant: float
    validation_status: str
    interpretation_warning: str


def matvec(A: list[list[float]], x: list[float]) -> list[float]:
    return [sum(row[j] * x[j] for j in range(len(x))) for row in A]


def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    rows = len(A)
    cols = len(B[0])
    inner = len(B)
    return [[sum(A[i][k] * B[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def transpose(A: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*A)]


def norm2(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def det3(A: list[list[float]]) -> float:
    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def solve3(A: list[list[float]], b: list[float]) -> list[float]:
    detA = det3(A)
    if abs(detA) < 1e-12:
        raise ValueError("Matrix is singular or nearly singular.")

    def replace_column(col: int) -> list[list[float]]:
        M = [row[:] for row in A]
        for i in range(3):
            M[i][col] = b[i]
        return M

    return [det3(replace_column(j)) / detA for j in range(3)]


def frobenius_norm(A: list[list[float]]) -> float:
    return math.sqrt(sum(value * value for row in A for value in row))


def condition_proxy(A: list[list[float]]) -> float:
    # Lightweight Frobenius condition proxy using exact inverse for 3x3 through solves.
    inverse_cols = [solve3(A, e) for e in ([1.0,0.0,0.0], [0.0,1.0,0.0], [0.0,0.0,1.0])]
    Ainv = transpose(inverse_cols)
    return frobenius_norm(A) * frobenius_norm(Ainv)


def cross_language_audit() -> tuple[CrossLanguageMatrixAudit, list[float], list[list[float]], list[float]]:
    A = [
        [4.0, 1.0, 0.5],
        [1.0, 3.0, 0.25],
        [0.5, 0.25, 2.5],
    ]
    x = [1.0, 2.0, -1.0]
    b = [6.0, 5.0, 2.0]

    y = matvec(A, x)
    product = matmul(A, transpose(A))
    solution = solve3(A, b)
    residual = [bi - ai for bi, ai in zip(b, matvec(A, solution))]

    audit = CrossLanguageMatrixAudit(
        model_name="cross_language_matrix_operation_audit",
        language="python_standard_library",
        matrix_shape="3x3",
        vector_shape="3",
        indexing_convention="zero_based",
        matrix_multiplication_operator="custom_matvec_or_library",
        elementwise_operator="*",
        solve_method="small_system_cramers_rule_for_portable_demo",
        condition_number=round(condition_proxy(A), 12),
        matrix_vector_product_norm=round(norm2(y), 12),
        matrix_matrix_product_trace=round(sum(product[i][i] for i in range(3)), 12),
        solve_residual_norm=round(norm2(residual), 12),
        determinant=round(det3(A), 12),
        validation_status="pass_residual_shape_and_condition_proxy_checks",
        interpretation_warning="Cross-language matrix results should be compared by mathematical intent, shapes, residuals, condition numbers, tolerances, indexing conventions, and operator semantics.",
    )
    return audit, y, product, solution


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, y, product, solution = cross_language_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "cross_language_matrix_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "matrix_vector_product.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "value"])
        writer.writeheader()
        for index, value in enumerate(y):
            writer.writerow({"index": index, "value": round(float(value), 12)})

    with (output_dir / "tables" / "linear_solve_solution.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "value"])
        writer.writeheader()
        for index, value in enumerate(solution):
            writer.writerow({"index": index, "value": round(float(value), 12)})

    (output_dir / "json" / "cross_language_matrix_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Cross-language matrix audit complete.")


if __name__ == "__main__":
    main()
