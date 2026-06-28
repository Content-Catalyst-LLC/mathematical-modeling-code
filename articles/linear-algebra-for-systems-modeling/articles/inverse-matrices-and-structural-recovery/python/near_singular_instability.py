"""
Near-singular instability example.

A matrix can be invertible and still be dangerous for structural recovery.
Small measurement perturbations in b can create large changes in x.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    A = np.array([
        [1.0, 1.0],
        [1.0, 1.0001],
    ])

    x_true = np.array([1.0, 1.0])
    b = A @ x_true

    x_recovered = np.linalg.solve(A, b)

    b_noisy = b + np.array([1e-4, -1e-4])
    x_noisy = np.linalg.solve(A, b_noisy)

    cond = np.linalg.cond(A)
    det = np.linalg.det(A)

    rel_b_change = np.linalg.norm(b_noisy - b) / np.linalg.norm(b)
    rel_x_change = np.linalg.norm(x_noisy - x_recovered) / np.linalg.norm(x_recovered)

    print("A =")
    print(A)
    print(f"det(A) = {det:.8e}")
    print(f"cond(A) = {cond:.8e}")
    print("true x =", x_true)
    print("b = A x =", b)
    print("recovered x =", x_recovered)
    print("noisy b =", b_noisy)
    print("recovered x from noisy b =", x_noisy)
    print(f"relative b change = {rel_b_change:.8e}")
    print(f"relative x change = {rel_x_change:.8e}")
    print(f"error amplification = {rel_x_change / rel_b_change:.8e}")

    print("\nInterpretation:")
    print("The matrix is technically invertible, but recovery is unstable.")
    print("This is a structural warning for measurement systems and inverse problems.")


if __name__ == "__main__":
    main()
