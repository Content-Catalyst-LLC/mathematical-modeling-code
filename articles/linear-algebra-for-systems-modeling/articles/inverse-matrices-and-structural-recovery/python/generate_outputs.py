"""
Generate CSV outputs for the article companion folder.
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def write_recovery_summary() -> None:
    cases = []

    matrices = {
        "well_conditioned": (
            np.array([[3.0, 1.0], [2.0, 4.0]]),
            np.array([7.0, 8.0]),
        ),
        "near_singular": (
            np.array([[1.0, 1.0], [1.0, 1.0001]]),
            np.array([2.0, 2.0001]),
        ),
        "singular": (
            np.array([[2.0, 4.0], [1.0, 2.0]]),
            np.array([6.0, 3.0]),
        ),
    }

    for name, (A, b) in matrices.items():
        rank = np.linalg.matrix_rank(A)
        det = np.linalg.det(A)
        cond = np.linalg.cond(A)

        if rank == A.shape[1]:
            x = np.linalg.solve(A, b)
            method = "solve"
        else:
            x = np.linalg.pinv(A) @ b
            method = "pseudoinverse"

        residual_norm = np.linalg.norm(A @ x - b)

        cases.append({
            "case": name,
            "method": method,
            "rank": rank,
            "determinant": det,
            "condition_number": cond,
            "x1": x[0],
            "x2": x[1],
            "residual_norm": residual_norm,
        })

    output_path = OUTPUT_DIR / "recovery_diagnostics.csv"

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "case",
                "method",
                "rank",
                "determinant",
                "condition_number",
                "x1",
                "x2",
                "residual_norm",
            ],
        )
        writer.writeheader()
        writer.writerows(cases)

    print(f"Wrote {output_path}")


def write_perturbation_sensitivity() -> None:
    A = np.array([[1.0, 1.0], [1.0, 1.0001]])
    x_true = np.array([1.0, 1.0])
    b = A @ x_true

    rows = []

    for eps in [1e-8, 1e-7, 1e-6, 1e-5, 1e-4]:
        b_noisy = b + np.array([eps, -eps])
        x_hat = np.linalg.solve(A, b_noisy)

        rel_b_change = np.linalg.norm(b_noisy - b) / np.linalg.norm(b)
        rel_x_change = np.linalg.norm(x_hat - x_true) / np.linalg.norm(x_true)

        rows.append({
            "epsilon": eps,
            "relative_b_change": rel_b_change,
            "relative_x_change": rel_x_change,
            "amplification": rel_x_change / rel_b_change,
            "x1": x_hat[0],
            "x2": x_hat[1],
        })

    output_path = OUTPUT_DIR / "perturbation_sensitivity.csv"

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "epsilon",
                "relative_b_change",
                "relative_x_change",
                "amplification",
                "x1",
                "x2",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {output_path}")


def main() -> None:
    write_recovery_summary()
    write_perturbation_sensitivity()


if __name__ == "__main__":
    main()
