from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class LargeScaleMatrixComputationAudit:
    model_name: str
    matrix_dimension: int
    nonzero_entries: int
    density: float
    dense_storage_mb: float
    sparse_storage_mb_estimate: float
    storage_reduction_factor: float
    matrix_type: str
    dominant_eigenvalue_estimate: float
    matrix_vector_product_norm: float
    iterative_residual_initial: float
    iterative_residual_final: float
    iterations: int
    convergence_warning: str
    interpretation_warning: str


def build_sparse_entries(n: int = 200, coupling: float = 0.04) -> list[tuple[int, int, float]]:
    entries: list[tuple[int, int, float]] = []
    for i in range(n):
        entries.append((i, i, 1.8))
        if i > 0:
            entries.append((i, i - 1, -coupling))
        if i < n - 1:
            entries.append((i, i + 1, -coupling))
        if i + 10 < n:
            entries.append((i, i + 10, -coupling / 2.0))
            entries.append((i + 10, i, -coupling / 2.0))
    return entries


def matvec(entries: list[tuple[int, int, float]], x: list[float], n: int) -> list[float]:
    y = [0.0] * n
    for i, j, value in entries:
        y[i] += value * x[j]
    return y


def norm2(values: list[float]) -> float:
    return math.sqrt(sum(v * v for v in values))


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def power_iteration(entries: list[tuple[int, int, float]], n: int, iterations: int = 80) -> float:
    x = [1.0 / math.sqrt(n)] * n
    eigenvalue = 0.0
    for _ in range(iterations):
        y = matvec(entries, x, n)
        y_norm = norm2(y)
        if y_norm == 0:
            break
        x = [value / y_norm for value in y]
        eigenvalue = dot(x, matvec(entries, x, n))
    return eigenvalue


def jacobi_iteration(entries: list[tuple[int, int, float]], b: list[float], n: int, iterations: int = 80) -> tuple[list[float], list[float]]:
    diagonal = [0.0] * n
    offdiag: list[tuple[int, int, float]] = []
    for i, j, value in entries:
        if i == j:
            diagonal[i] = value
        else:
            offdiag.append((i, j, value))

    if any(value == 0.0 for value in diagonal):
        raise ValueError("Jacobi iteration requires nonzero diagonal entries.")

    x = [0.0] * n
    residuals: list[float] = []
    for _ in range(iterations):
        ax = matvec(entries, x, n)
        residuals.append(norm2([bi - ai for bi, ai in zip(b, ax)]))
        rx = [0.0] * n
        for i, j, value in offdiag:
            rx[i] += value * x[j]
        x = [(b[i] - rx[i]) / diagonal[i] for i in range(n)]

    ax = matvec(entries, x, n)
    residuals.append(norm2([bi - ai for bi, ai in zip(b, ax)]))
    return x, residuals


def computation_audit() -> tuple[LargeScaleMatrixComputationAudit, list[float], list[float]]:
    n = 200
    entries = build_sparse_entries(n)
    nonzero = len(entries)
    density = nonzero / (n * n)
    dense_storage_mb = n * n * 8 / 1_000_000
    sparse_storage_mb_estimate = nonzero * (8 + 4 + 4) / 1_000_000
    storage_reduction_factor = dense_storage_mb / sparse_storage_mb_estimate

    x = [1.0 + i / (n - 1) for i in range(n)]
    y = matvec(entries, x, n)
    _, residuals = jacobi_iteration(entries, [1.0] * n, n)
    dominant = power_iteration(entries, n)

    audit = LargeScaleMatrixComputationAudit(
        model_name="synthetic_large_scale_matrix_computation_audit",
        matrix_dimension=n,
        nonzero_entries=nonzero,
        density=round(density, 12),
        dense_storage_mb=round(dense_storage_mb, 12),
        sparse_storage_mb_estimate=round(sparse_storage_mb_estimate, 12),
        storage_reduction_factor=round(storage_reduction_factor, 12),
        matrix_type="banded_sparse_like_symmetric_system",
        dominant_eigenvalue_estimate=round(dominant, 12),
        matrix_vector_product_norm=round(norm2(y), 12),
        iterative_residual_initial=round(residuals[0], 12),
        iterative_residual_final=round(residuals[-1], 12),
        iterations=80,
        convergence_warning="Iterative solver output depends on matrix structure, scaling, preconditioning, stopping tolerance, residual diagnostics, and numerical precision.",
        interpretation_warning="Large-scale matrix outputs are computational results under storage, approximation, precision, solver, and model assumptions. Larger computations are not automatically more reliable.",
    )
    return audit, residuals, y


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, residuals, product_vector = computation_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "large_scale_matrix_computation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "iterative_residual_history.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["iteration", "residual_norm"])
        writer.writeheader()
        for index, residual in enumerate(residuals):
            writer.writerow({"iteration": index, "residual_norm": round(float(residual), 12)})

    with (output_dir / "tables" / "matrix_vector_product_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "value"])
        writer.writeheader()
        for index, value in enumerate(product_vector[:25]):
            writer.writerow({"index": index, "value": round(float(value), 12)})

    (output_dir / "json" / "large_scale_matrix_computation_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Large-scale matrix computation audit complete.")


if __name__ == "__main__":
    main()
