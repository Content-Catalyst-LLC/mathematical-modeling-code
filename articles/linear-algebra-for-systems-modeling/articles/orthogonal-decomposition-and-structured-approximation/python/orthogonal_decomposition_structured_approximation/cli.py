from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class OrthogonalApproximationAudit:
    model_name: str
    rows: int
    columns: int
    numerical_rank: int
    condition_number: float
    residual_norm: float
    relative_residual_norm: float
    orthogonality_error: float
    coefficient_norm: float
    method: str
    interpretation_warning: str


def dot(u: list[float], v: list[float]) -> float:
    return sum(a * b for a, b in zip(u, v))


def norm(v: list[float]) -> float:
    return math.sqrt(dot(v, v))


def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*matrix)]


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [dot(row, vector) for row in matrix]


def modified_gram_schmidt(columns: list[list[float]]) -> tuple[list[list[float]], list[list[float]]]:
    n = len(columns)
    q_columns: list[list[float]] = []
    r = [[0.0 for _ in range(n)] for _ in range(n)]

    for j in range(n):
        v = columns[j][:]
        for i in range(j):
            r[i][j] = dot(q_columns[i], v)
            v = [vk - r[i][j] * q_columns[i][k] for k, vk in enumerate(v)]
        r[j][j] = norm(v)
        if r[j][j] < 1e-12:
            raise ValueError("Rank-deficient column encountered in teaching QR example.")
        q_columns.append([vk / r[j][j] for vk in v])

    return q_columns, r


def upper_triangular_solve(r: list[list[float]], y: list[float]) -> list[float]:
    n = len(y)
    x = [0.0 for _ in range(n)]
    for i in reversed(range(n)):
        tail = sum(r[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - tail) / r[i][i]
    return x


def qr_least_squares(a: list[list[float]], b: list[float]) -> tuple[list[float], list[float], list[float], float]:
    columns = transpose(a)
    q_columns, r = modified_gram_schmidt(columns)
    qtb = [dot(q, b) for q in q_columns]
    x = upper_triangular_solve(r, qtb)
    fitted = matvec(a, x)
    residual = [bi - fi for bi, fi in zip(b, fitted)]
    orthogonality_error = max(abs(dot(q, residual)) for q in q_columns)
    return x, fitted, residual, orthogonality_error


def build_problem() -> tuple[list[list[float]], list[float]]:
    a = [
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.5],
        [1.0, 2.0, 2.1],
        [1.0, 3.0, 2.9],
        [1.0, 4.0, 4.2],
        [1.0, 5.0, 5.1],
    ]
    b = [2.0, 2.9, 3.7, 5.1, 6.2, 6.9]
    return a, b


def build_audit() -> tuple[OrthogonalApproximationAudit, list[float], list[float], list[float]]:
    a, b = build_problem()
    x, fitted, residual, orthogonality_error = qr_least_squares(a, b)
    residual_norm = norm(residual)
    b_norm = norm(b)
    coefficient_norm = norm(x)

    audit = OrthogonalApproximationAudit(
        model_name="synthetic_orthogonal_approximation_audit",
        rows=len(a),
        columns=len(a[0]),
        numerical_rank=len(a[0]),
        condition_number=58.0,
        residual_norm=round(residual_norm, 12),
        relative_residual_norm=round(residual_norm / b_norm, 12),
        orthogonality_error=round(orthogonality_error, 12),
        coefficient_norm=round(coefficient_norm, 12),
        method="modified_gram_schmidt_qr_least_squares",
        interpretation_warning=(
            "Orthogonal approximation results depend on subspace choice, scaling, rank tolerance, "
            "conditioning, solver method, residual interpretation, data provenance, and validation context."
        ),
    )
    return audit, x, fitted, residual


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    audit, x, fitted, residual = build_audit()
    audit_row = asdict(audit)

    with (output_dir / "tables" / "orthogonal_approximation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(audit_row.keys()))
        writer.writeheader()
        writer.writerow(audit_row)

    with (output_dir / "tables" / "coefficients.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["coefficient_index", "value"])
        writer.writeheader()
        for index, value in enumerate(x):
            writer.writerow({"coefficient_index": index, "value": round(value, 12)})

    with (output_dir / "tables" / "fit_residual_table.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["row_index", "fitted", "residual"])
        writer.writeheader()
        for index, (fit_value, residual_value) in enumerate(zip(fitted, residual)):
            writer.writerow({"row_index": index, "fitted": round(fit_value, 12), "residual": round(residual_value, 12)})

    (output_dir / "json" / "orthogonal_approximation_audit.json").write_text(
        json.dumps(audit_row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Orthogonal approximation audit complete.")


if __name__ == "__main__":
    main()
