from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class StabilityConditioningAudit:
    model_name: str
    matrix_case: str
    matrix_shape: str
    determinant: float
    condition_number_proxy: float
    solution_norm: float
    residual_norm: float
    relative_residual: float
    perturbation_size: float
    perturbed_solution_change: float
    stability_status: str
    interpretation_warning: str


def matvec(A: list[list[float]], x: list[float]) -> list[float]:
    return [sum(row[j] * x[j] for j in range(len(x))) for row in A]


def norm2(x: list[float]) -> float:
    return math.sqrt(sum(v * v for v in x))


def det2(A: list[list[float]]) -> float:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def solve2(A: list[list[float]], b: list[float]) -> list[float]:
    determinant = det2(A)
    if abs(determinant) < 1e-14:
        raise ValueError("Matrix is singular or too close to singular for this demonstration.")
    return [
        (b[0] * A[1][1] - A[0][1] * b[1]) / determinant,
        (A[0][0] * b[1] - b[0] * A[1][0]) / determinant,
    ]


def inverse2(A: list[list[float]]) -> list[list[float]]:
    determinant = det2(A)
    if abs(determinant) < 1e-14:
        raise ValueError("Matrix is singular or nearly singular.")
    return [
        [A[1][1] / determinant, -A[0][1] / determinant],
        [-A[1][0] / determinant, A[0][0] / determinant],
    ]


def frobenius_norm(A: list[list[float]]) -> float:
    return math.sqrt(sum(value * value for row in A for value in row))


def condition_proxy(A: list[list[float]]) -> float:
    return frobenius_norm(A) * frobenius_norm(inverse2(A))


def audit_case(case_name: str, A: list[list[float]], b: list[float]) -> StabilityConditioningAudit:
    x = solve2(A, b)
    residual = [bi - ai for bi, ai in zip(b, matvec(A, x))]
    residual_norm = norm2(residual)
    relative_residual = residual_norm / max(norm2(b), 1e-15)

    perturbation_size = 1e-5
    b_perturbed = [b[0] + perturbation_size, b[1] - perturbation_size]
    x_perturbed = solve2(A, b_perturbed)
    solution_change = norm2([xp - xi for xp, xi in zip(x_perturbed, x)])

    cond = condition_proxy(A)
    status = "review_required_ill_conditioned" if cond > 1_000 else "stable_under_demo_threshold"

    return StabilityConditioningAudit(
        model_name="numerical_stability_conditioning_audit",
        matrix_case=case_name,
        matrix_shape="2x2",
        determinant=round(det2(A), 12),
        condition_number_proxy=round(cond, 12),
        solution_norm=round(norm2(x), 12),
        residual_norm=round(residual_norm, 12),
        relative_residual=round(relative_residual, 12),
        perturbation_size=perturbation_size,
        perturbed_solution_change=round(solution_change, 12),
        stability_status=status,
        interpretation_warning="Residuals should be interpreted alongside conditioning, scaling, perturbation sensitivity, solver method, precision, and model purpose.",
    )


def build_audits() -> list[StabilityConditioningAudit]:
    well_conditioned_A = [
        [3.0, 0.5],
        [0.5, 2.0],
    ]
    ill_conditioned_A = [
        [1.0, 0.9999],
        [0.9999, 0.99980001],
    ]
    b = [1.0, 0.5]
    return [
        audit_case("well_conditioned_system", well_conditioned_A, b),
        audit_case("ill_conditioned_system", ill_conditioned_A, b),
    ]


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audits = build_audits()
    rows = [asdict(audit) for audit in audits]

    with (output_dir / "tables" / "stability_conditioning_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "stability_conditioning_audit.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Numerical stability and conditioning audit complete.")


if __name__ == "__main__":
    main()
