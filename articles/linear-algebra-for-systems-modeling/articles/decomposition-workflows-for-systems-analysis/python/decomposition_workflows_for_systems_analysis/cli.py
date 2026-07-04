from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DecompositionWorkflowAudit:
    model_name: str
    matrix_shape: str
    matrix_class: str
    recommended_workflow: str
    determinant_2x2_leading_block: float
    condition_proxy: float
    estimated_rank: int
    singular_value_1: float
    singular_value_2: float
    singular_value_3: float
    low_rank_reconstruction_error: float
    solve_residual_norm: float
    decomposition_warning: str
    interpretation_warning: str


def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def transpose(A: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*A)]


def matvec(A: list[list[float]], x: list[float]) -> list[float]:
    return [sum(row[j] * x[j] for j in range(len(x))) for row in A]


def norm2(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def det2(A: list[list[float]]) -> float:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def solve3_gaussian(A: list[list[float]], b: list[float]) -> list[float]:
    M = [row[:] + [rhs] for row, rhs in zip(A, b)]
    n = 3
    for pivot in range(n):
        best_row = max(range(pivot, n), key=lambda r: abs(M[r][pivot]))
        if abs(M[best_row][pivot]) < 1e-12:
            raise ValueError("Matrix is singular or nearly singular.")
        M[pivot], M[best_row] = M[best_row], M[pivot]
        pivot_value = M[pivot][pivot]
        for col in range(pivot, n + 1):
            M[pivot][col] /= pivot_value
        for row in range(n):
            if row == pivot:
                continue
            factor = M[row][pivot]
            for col in range(pivot, n + 1):
                M[row][col] -= factor * M[pivot][col]
    return [M[i][n] for i in range(n)]


def jacobi_eigenvalues_symmetric_3x3(A: list[list[float]], sweeps: int = 60) -> list[float]:
    M = [row[:] for row in A]
    n = 3
    for _ in range(sweeps):
        p, q = 0, 1
        max_value = abs(M[p][q])
        for i in range(n):
            for j in range(i + 1, n):
                if abs(M[i][j]) > max_value:
                    p, q = i, j
                    max_value = abs(M[i][j])
        if max_value < 1e-12:
            break
        if abs(M[p][p] - M[q][q]) < 1e-15:
            angle = math.pi / 4
        else:
            angle = 0.5 * math.atan2(2 * M[p][q], M[q][q] - M[p][p])
        c = math.cos(angle)
        s = math.sin(angle)
        for k in range(n):
            mkp = M[k][p]
            mkq = M[k][q]
            M[k][p] = c * mkp - s * mkq
            M[k][q] = s * mkp + c * mkq
        for k in range(n):
            mpk = M[p][k]
            mqk = M[q][k]
            M[p][k] = c * mpk - s * mqk
            M[q][k] = s * mpk + c * mqk
    return sorted([M[i][i] for i in range(n)], reverse=True)


def singular_values_via_ata(A: list[list[float]]) -> list[float]:
    ata = matmul(transpose(A), A)
    eigenvalues = jacobi_eigenvalues_symmetric_3x3(ata)
    return [math.sqrt(max(value, 0.0)) for value in eigenvalues]


def decomposition_audit() -> DecompositionWorkflowAudit:
    A = [
        [4.0, 1.0, 0.2],
        [1.0, 3.0, 0.4],
        [0.2, 0.4, 1.2],
        [2.0, 1.5, 0.3],
    ]

    square_block = [row[:3] for row in A[:3]]
    b = [1.0, 2.0, 0.5]
    solution = solve3_gaussian(square_block, b)
    residual = [bi - ai for bi, ai in zip(b, matvec(square_block, solution))]

    singular_values = singular_values_via_ata(A)
    tolerance = 1e-8 * max(singular_values)
    estimated_rank = sum(1 for value in singular_values if value > tolerance)
    condition_proxy = max(singular_values) / max(min(singular_values), 1e-15)
    low_rank_reconstruction_error = math.sqrt(sum(value * value for value in singular_values[2:]))

    return DecompositionWorkflowAudit(
        model_name="decomposition_workflow_audit",
        matrix_shape="4x3",
        matrix_class="rectangular_overdetermined_dense_demo_matrix",
        recommended_workflow="QR_or_SVD_for_least_squares_and_rank_diagnostics",
        determinant_2x2_leading_block=round(det2(square_block), 12),
        condition_proxy=round(condition_proxy, 12),
        estimated_rank=estimated_rank,
        singular_value_1=round(singular_values[0], 12),
        singular_value_2=round(singular_values[1], 12),
        singular_value_3=round(singular_values[2], 12),
        low_rank_reconstruction_error=round(low_rank_reconstruction_error, 12),
        solve_residual_norm=round(norm2(residual), 12),
        decomposition_warning="Rectangular systems should generally use QR or SVD rather than normal equations when stability and rank diagnostics matter.",
        interpretation_warning="Decomposition factors should be interpreted through matrix construction, scaling, rank tolerance, conditioning, residuals, and system meaning.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = decomposition_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "decomposition_workflow_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "singular_value_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["component", "singular_value"])
        writer.writeheader()
        for index, value in enumerate([audit.singular_value_1, audit.singular_value_2, audit.singular_value_3], start=1):
            writer.writerow({"component": index, "singular_value": value})

    (output_dir / "json" / "decomposition_workflow_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Decomposition workflow audit complete.")


if __name__ == "__main__":
    main()
