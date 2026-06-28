"""
Pseudoinverse and least-squares recovery.

This script covers:
- overdetermined recovery with noisy measurements
- underdetermined minimum-norm recovery
- comparison of residuals and ranks
"""

from __future__ import annotations

import numpy as np


def overdetermined_example() -> None:
    print("\n=== Overdetermined sensor recovery ===")

    A = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
        [2.0, -1.0],
    ])
    b = np.array([2.02, 0.97, 3.04, 3.03])

    x_lstsq, residuals, rank, singular_values = np.linalg.lstsq(A, b, rcond=None)
    x_pinv = np.linalg.pinv(A) @ b

    print("A =")
    print(A)
    print("b =", b)
    print("least-squares x =", x_lstsq)
    print("pseudoinverse x =", x_pinv)
    print("rank(A) =", rank)
    print("singular values =", singular_values)
    print("residual vector =", A @ x_lstsq - b)
    print("residual norm =", np.linalg.norm(A @ x_lstsq - b))


def underdetermined_example() -> None:
    print("\n=== Underdetermined minimum-norm recovery ===")

    A = np.array([
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 1.0],
    ])
    b = np.array([3.0, 2.0])

    x_min_norm = np.linalg.pinv(A) @ b

    print("A =")
    print(A)
    print("b =", b)
    print("minimum-norm pseudoinverse solution =", x_min_norm)
    print("residual vector =", A @ x_min_norm - b)
    print("residual norm =", np.linalg.norm(A @ x_min_norm - b))
    print("rank(A) =", np.linalg.matrix_rank(A))
    print("Interpretation: infinitely many exact solutions exist; pseudoinverse selects the minimum-norm one.")


def main() -> None:
    overdetermined_example()
    underdetermined_example()


if __name__ == "__main__":
    main()
