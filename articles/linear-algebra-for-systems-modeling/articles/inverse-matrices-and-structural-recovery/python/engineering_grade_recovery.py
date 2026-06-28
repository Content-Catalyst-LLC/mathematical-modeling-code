"""
Engineer-grade recovery diagnostics for inverse matrices.

This script demonstrates:
- direct solve instead of explicit inverse
- determinant and rank diagnostics
- condition number
- residual norm and relative residual
- sensitivity to measurement perturbation
"""

from __future__ import annotations

import numpy as np


def diagnostics(A: np.ndarray, b: np.ndarray, label: str) -> None:
    print(f"\n=== {label} ===")
    print("A =")
    print(A)
    print("b =", b)

    m, n = A.shape
    rank = np.linalg.matrix_rank(A)
    cond = np.linalg.cond(A) if m == n else np.linalg.cond(A.T @ A)

    print(f"shape(A) = {A.shape}")
    print(f"rank(A) = {rank}")
    print(f"condition indicator = {cond:.6g}")

    if m == n:
        det = np.linalg.det(A)
        print(f"det(A) = {det:.6g}")

        if rank == n:
            x = np.linalg.solve(A, b)
            residual = A @ x - b
            rel_residual = np.linalg.norm(residual) / max(np.linalg.norm(b), 1e-15)

            print("method = solve(A, b)")
            print("recovered x =", x)
            print(f"residual norm = {np.linalg.norm(residual):.6e}")
            print(f"relative residual = {rel_residual:.6e}")

            b_perturbed = b + np.array([1e-4, -1e-4])
            x_perturbed = np.linalg.solve(A, b_perturbed)

            rel_b_change = np.linalg.norm(b_perturbed - b) / np.linalg.norm(b)
            rel_x_change = np.linalg.norm(x_perturbed - x) / np.linalg.norm(x)

            print("perturbed b =", b_perturbed)
            print("perturbed recovered x =", x_perturbed)
            print(f"relative b change = {rel_b_change:.6e}")
            print(f"relative x change = {rel_x_change:.6e}")
            print(f"amplification factor = {rel_x_change / rel_b_change:.6g}")
        else:
            print("Matrix is rank deficient; exact inverse recovery is not unique.")
    else:
        print("Rectangular system; use least squares or pseudoinverse diagnostics.")


def main() -> None:
    A = np.array([[3.0, 1.0], [2.0, 4.0]])
    x_true = np.array([2.0, 1.0])
    b = A @ x_true

    diagnostics(A, b, "well-conditioned square recovery")

    A_singular = np.array([[2.0, 4.0], [1.0, 2.0]])
    b_singular = np.array([6.0, 3.0])

    diagnostics(A_singular, b_singular, "singular recovery failure")


if __name__ == "__main__":
    main()
