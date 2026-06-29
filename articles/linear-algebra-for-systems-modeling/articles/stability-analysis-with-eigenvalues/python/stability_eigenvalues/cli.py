from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix2 = list[list[float]]


@dataclass(frozen=True)
class StabilityAudit:
    system_name: str
    matrix_entries: str
    trace: float
    determinant: float
    eigenvalue_1: float
    eigenvalue_2: float
    spectral_radius: float
    discrete_time_classification: str
    continuous_time_real_part_classification: str
    dominant_mode_warning: str
    interpretation_warning: str


def trace_2x2(A: Matrix2) -> float:
    return A[0][0] + A[1][1]


def determinant_2x2(A: Matrix2) -> float:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def eigenvalues_2x2(A: Matrix2) -> tuple[float, float]:
    tr = trace_2x2(A)
    det = determinant_2x2(A)
    discriminant = tr * tr - 4.0 * det
    if discriminant < 0:
        raise ValueError("This teaching routine handles real eigenvalues only.")
    root = math.sqrt(discriminant)
    return ((tr + root) / 2.0, (tr - root) / 2.0)


def matrix_to_string(A: Matrix2) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def classify_discrete(eigenvalues: tuple[float, float]) -> str:
    spectral_radius = max(abs(value) for value in eigenvalues)
    if spectral_radius < 1.0:
        return "asymptotically_stable_discrete_time"
    if abs(spectral_radius - 1.0) <= 1e-10:
        return "boundary_or_marginal_discrete_time"
    return "unstable_discrete_time"


def classify_continuous(eigenvalues: tuple[float, float]) -> str:
    largest_real_part = max(eigenvalues)
    if largest_real_part < 0.0:
        return "asymptotically_stable_continuous_time"
    if abs(largest_real_part) <= 1e-10:
        return "boundary_or_marginal_continuous_time"
    return "unstable_continuous_time"


def build_audit() -> StabilityAudit:
    A = [
        [0.82, 0.12],
        [0.18, 0.76],
    ]

    eigenvalues = eigenvalues_2x2(A)
    spectral_radius = max(abs(value) for value in eigenvalues)

    return StabilityAudit(
        system_name="two_mode_stability_audit",
        matrix_entries=matrix_to_string(A),
        trace=round(trace_2x2(A), 12),
        determinant=round(determinant_2x2(A), 12),
        eigenvalue_1=round(eigenvalues[0], 12),
        eigenvalue_2=round(eigenvalues[1], 12),
        spectral_radius=round(spectral_radius, 12),
        discrete_time_classification=classify_discrete(eigenvalues),
        continuous_time_real_part_classification=classify_continuous(eigenvalues),
        dominant_mode_warning=(
            "The largest eigenvalue magnitude controls asymptotic discrete-time behavior, "
            "but short-run transient growth, forcing, nonlinearities, and initial conditions must also be reviewed."
        ),
        interpretation_warning=(
            "Stability classification depends on whether the matrix represents a discrete-time update, "
            "a continuous-time generator, or a local linearization. Do not reuse one stability rule across time models."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "stability_analysis_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "stability_analysis_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Eigenvalue stability audit complete.")


if __name__ == "__main__":
    main()
