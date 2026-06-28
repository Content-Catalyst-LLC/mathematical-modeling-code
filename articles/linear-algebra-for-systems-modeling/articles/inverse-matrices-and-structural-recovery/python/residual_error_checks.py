"""
Residual and error checks for structural recovery.

A recovered vector should be evaluated by:
- residual norm ||Ax - b||
- relative residual
- relative state error when ground truth is available
- condition number
"""

from __future__ import annotations

import numpy as np


def recovery_report(A: np.ndarray, b: np.ndarray, x_true: np.ndarray | None = None) -> dict[str, float]:
    if A.shape[0] == A.shape[1] and np.linalg.matrix_rank(A) == A.shape[1]:
        x_hat = np.linalg.solve(A, b)
        method = "solve"
    else:
        x_hat = np.linalg.pinv(A) @ b
        method = "pseudoinverse"

    residual = A @ x_hat - b
    residual_norm = float(np.linalg.norm(residual))
    relative_residual = float(residual_norm / max(np.linalg.norm(b), 1e-15))
    condition_number = float(np.linalg.cond(A))

    print("method =", method)
    print("x_hat =", x_hat)
    print("residual =", residual)
    print(f"residual norm = {residual_norm:.8e}")
    print(f"relative residual = {relative_residual:.8e}")
    print(f"condition number = {condition_number:.8e}")

    report = {
        "residual_norm": residual_norm,
        "relative_residual": relative_residual,
        "condition_number": condition_number,
    }

    if x_true is not None:
        relative_state_error = float(np.linalg.norm(x_hat - x_true) / max(np.linalg.norm(x_true), 1e-15))
        print(f"relative state error = {relative_state_error:.8e}")
        report["relative_state_error"] = relative_state_error

    return report


def main() -> None:
    A = np.array([[3.0, 1.0], [2.0, 4.0]])
    x_true = np.array([2.0, 1.0])
    b = A @ x_true

    print("=== Clean square recovery ===")
    recovery_report(A, b, x_true)

    print("\n=== Noisy near-singular recovery ===")
    A_bad = np.array([[1.0, 1.0], [1.0, 1.0001]])
    x_bad_true = np.array([1.0, 1.0])
    b_bad = A_bad @ x_bad_true + np.array([1e-4, -1e-4])
    recovery_report(A_bad, b_bad, x_bad_true)


if __name__ == "__main__":
    main()
