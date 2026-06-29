from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

Matrix = list[list[float]]


@dataclass(frozen=True)
class DiagonalizationAudit:
    system_name: str
    matrix_entries: str
    eigenvector_matrix: str
    diagonal_matrix: str
    reconstruction_error_frobenius: float
    spectral_radius: float
    dominant_eigenvalue: float
    condition_warning: str
    stability_classification: str
    modal_interpretation_warning: str


def matmul(A: Matrix, B: Matrix) -> Matrix:
    return [
        [sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def subtract(A: Matrix, B: Matrix) -> Matrix:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def frobenius(A: Matrix) -> float:
    return math.sqrt(sum(value * value for row in A for value in row))


def matrix_to_string(A: Matrix) -> str:
    return ";".join(",".join(f"{value:.6f}" for value in row) for row in A)


def inverse_2x2(A: Matrix) -> Matrix:
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if abs(det) <= 1e-12:
        raise ValueError("matrix is singular or nearly singular")
    return [
        [A[1][1] / det, -A[0][1] / det],
        [-A[1][0] / det, A[0][0] / det],
    ]


def classify_stability(spectral_radius: float) -> str:
    if spectral_radius < 1.0:
        return "all_modes_decay_discrete_time"
    if abs(spectral_radius - 1.0) <= 1e-10:
        return "persistent_or_marginal_mode_present"
    return "amplifying_mode_present"


def build_audit() -> DiagonalizationAudit:
    P = [
        [1.0, 1.0],
        [1.0, -2.0],
    ]
    D = [
        [0.92, 0.0],
        [0.0, 0.55],
    ]
    Pinv = inverse_2x2(P)
    A = matmul(matmul(P, D), Pinv)
    A_reconstructed = matmul(matmul(P, D), Pinv)
    reconstruction_error = frobenius(subtract(A, A_reconstructed))

    eigenvalues = [0.92, 0.55]
    spectral_radius = max(abs(value) for value in eigenvalues)
    dominant = max(eigenvalues, key=lambda value: abs(value))

    return DiagonalizationAudit(
        system_name="two_mode_diagonalization_audit",
        matrix_entries=matrix_to_string(A),
        eigenvector_matrix=matrix_to_string(P),
        diagonal_matrix=matrix_to_string(D),
        reconstruction_error_frobenius=round(reconstruction_error, 12),
        spectral_radius=round(spectral_radius, 12),
        dominant_eigenvalue=round(dominant, 12),
        condition_warning=(
            "For production workflows, compute cond(P), eigenpair residuals, spectral gaps, "
            "and perturbation sensitivity before interpreting modal coordinates."
        ),
        stability_classification=classify_stability(spectral_radius),
        modal_interpretation_warning=(
            "Diagonalization decouples the representation, not necessarily the real system. "
            "Modal meaning depends on matrix construction, units, scaling, and domain interpretation."
        ),
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "diagonalization_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "diagonalization_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Diagonalization audit complete.")


if __name__ == "__main__":
    main()
