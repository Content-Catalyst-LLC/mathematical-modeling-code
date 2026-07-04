from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class SparseMatrixEfficiencyAudit:
    model_name: str
    matrix_dimension: int
    nonzero_entries: int
    density: float
    dense_storage_mb: float
    coordinate_storage_mb_estimate: float
    storage_reduction_factor: float
    average_row_degree: float
    max_row_degree: int
    isolated_rows: int
    matrix_vector_product_norm: float
    iterative_residual_initial: float
    iterative_residual_final: float
    iterations: int
    sparsity_warning: str
    interpretation_warning: str


def build_sparse_entries(n: int = 250) -> list[tuple[int, int, float]]:
    entries: list[tuple[int, int, float]] = []
    for i in range(n):
        entries.append((i, i, 1.6))
        if i > 0:
            entries.append((i, i - 1, -0.08))
        if i < n - 1:
            entries.append((i, i + 1, -0.08))
        if i + 7 < n:
            entries.append((i, i + 7, -0.025))
            entries.append((i + 7, i, -0.025))
        if i % 25 == 0 and i + 25 < n:
            entries.append((i, i + 25, -0.05))
            entries.append((i + 25, i, -0.05))
    return entries


def matvec(entries: list[tuple[int, int, float]], x: list[float], n: int) -> list[float]:
    y = [0.0] * n
    for i, j, value in entries:
        y[i] += value * x[j]
    return y


def norm2(values: list[float]) -> float:
    return math.sqrt(sum(v * v for v in values))


def degree_summary(entries: list[tuple[int, int, float]], n: int) -> tuple[float, int, int]:
    row_counts = [0] * n
    for i, j, value in entries:
        if i != j and value != 0:
            row_counts[i] += 1
    average = sum(row_counts) / n
    maximum = max(row_counts)
    isolated = sum(1 for value in row_counts if value == 0)
    return average, maximum, isolated


def jacobi_like_residuals(entries: list[tuple[int, int, float]], n: int, iterations: int = 60) -> list[float]:
    diagonal = [0.0] * n
    offdiag: list[tuple[int, int, float]] = []
    for i, j, value in entries:
        if i == j:
            diagonal[i] = value
        else:
            offdiag.append((i, j, value))
    if any(value == 0.0 for value in diagonal):
        raise ValueError("Jacobi-like residual tracking requires nonzero diagonal entries.")

    x = [0.0] * n
    b = [1.0] * n
    residuals: list[float] = []
    for _ in range(iterations):
        ax = matvec(entries, x, n)
        residuals.append(norm2([bi - ai for bi, ai in zip(b, ax)]))
        offdiag_x = [0.0] * n
        for i, j, value in offdiag:
            offdiag_x[i] += value * x[j]
        x = [(b[i] - offdiag_x[i]) / diagonal[i] for i in range(n)]
    ax = matvec(entries, x, n)
    residuals.append(norm2([bi - ai for bi, ai in zip(b, ax)]))
    return residuals


def sparse_efficiency_audit() -> tuple[SparseMatrixEfficiencyAudit, list[float], list[float]]:
    n = 250
    entries = build_sparse_entries(n)
    nonzero = len(entries)
    density = nonzero / (n * n)

    dense_storage_mb = (n * n * 8) / 1_000_000
    coordinate_storage_mb_estimate = (nonzero * (8 + 4 + 4)) / 1_000_000
    storage_reduction_factor = dense_storage_mb / coordinate_storage_mb_estimate

    average_degree, max_degree, isolated_rows = degree_summary(entries, n)

    x = [1.0 + i / (n - 1) for i in range(n)]
    y = matvec(entries, x, n)
    residuals = jacobi_like_residuals(entries, n, iterations=60)

    audit = SparseMatrixEfficiencyAudit(
        model_name="synthetic_sparse_matrix_efficiency_audit",
        matrix_dimension=n,
        nonzero_entries=nonzero,
        density=round(density, 12),
        dense_storage_mb=round(dense_storage_mb, 12),
        coordinate_storage_mb_estimate=round(coordinate_storage_mb_estimate, 12),
        storage_reduction_factor=round(storage_reduction_factor, 12),
        average_row_degree=round(average_degree, 12),
        max_row_degree=max_degree,
        isolated_rows=isolated_rows,
        matrix_vector_product_norm=round(norm2(y), 12),
        iterative_residual_initial=round(residuals[0], 12),
        iterative_residual_final=round(residuals[-1], 12),
        iterations=60,
        sparsity_warning="Sparse efficiency depends on whether zero entries represent true absence, unknown relationships, thresholded weak values, or modeling exclusions.",
        interpretation_warning="Sparse matrix outputs should be interpreted through storage format, sparsity pattern, solver diagnostics, conditioning, threshold rules, and validation evidence.",
    )
    return audit, residuals, y


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit, residuals, product_vector = sparse_efficiency_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "sparse_matrix_efficiency_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    with (output_dir / "tables" / "sparse_iterative_residual_history.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["iteration", "residual_norm"])
        writer.writeheader()
        for index, residual in enumerate(residuals):
            writer.writerow({"iteration": index, "residual_norm": round(float(residual), 12)})

    with (output_dir / "tables" / "sparse_matrix_vector_product_sample.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["index", "value"])
        writer.writeheader()
        for index, value in enumerate(product_vector[:25]):
            writer.writerow({"index": index, "value": round(float(value), 12)})

    (output_dir / "json" / "sparse_matrix_efficiency_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Sparse matrix efficiency audit complete.")


if __name__ == "__main__":
    main()
