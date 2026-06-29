from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix2 = list[list[float]]


@dataclass(frozen=True)
class EigenstructureAudit:
    system_name: str
    matrix_entries: str
    trace: float
    determinant: float
    eigenvalue_1: float
    eigenvalue_2: float
    spectral_radius: float
    dominant_eigenvalue: float
    stability_classification: str
    eigenpair_residual_warning: str
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


def classify_stability(spectral_radius: float) -> str:
    if spectral_radius < 1.0:
        return "asymptotically_damped_discrete_time"
    if abs(spectral_radius - 1.0) <= 1e-10:
        return "marginal_or_persistent_discrete_time"
    return "amplifying_or_unstable_discrete_time"


def build_audit() -> EigenstructureAudit:
    A = [
        [0.82, 0.12],
        [0.18, 0.76],
    ]

    tr = trace_2x2(A)
    det = determinant_2x2(A)
    lambda_1, lambda_2 = eigenvalues_2x2(A)
    spectral_radius = max(abs(lambda_1), abs(lambda_2))
    dominant = lambda_1 if abs(lambda_1) >= abs(lambda_2) else lambda_2

    return EigenstructureAudit(
        system_name="two_sector_mode_audit",
        matrix_entries=matrix_to_string(A),
        trace=round(tr, 12),
        determinant=round(det, 12),
        eigenvalue_1=round(lambda_1, 12),
        eigenvalue_2=round(lambda_2, 12),
        spectral_radius=round(spectral_radius, 12),
        dominant_eigenvalue=round(dominant, 12),
        stability_classification=classify_stability(spectral_radius),
        eigenpair_residual_warning=(
            "For production workflows, compute eigenpair residuals ||Av-lambda v|| "
            "using a numerical linear algebra library and report sensitivity diagnostics."
        ),
        interpretation_warning=(
            "Eigenvalues describe modes of the specified matrix, not automatic causal mechanisms. "
            "Mode interpretation depends on matrix construction, units, scaling, domain meaning, "
            "and whether linear dynamics are appropriate."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "eigenstructure_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "eigenstructure_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Eigenstructure audit complete.")


if __name__ == "__main__":
    main()
