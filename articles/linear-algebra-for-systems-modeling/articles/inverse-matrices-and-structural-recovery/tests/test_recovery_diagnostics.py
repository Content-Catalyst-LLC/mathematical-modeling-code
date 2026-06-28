"""
Lightweight validation tests for inverse recovery examples.

Run from article directory:

python3 tests/test_recovery_diagnostics.py
"""

from __future__ import annotations

import numpy as np


def test_well_conditioned_recovery() -> None:
    A = np.array([[3.0, 1.0], [2.0, 4.0]])
    x_true = np.array([2.0, 1.0])
    b = A @ x_true
    x_hat = np.linalg.solve(A, b)

    assert np.allclose(x_hat, x_true)
    assert np.linalg.norm(A @ x_hat - b) < 1e-12


def test_singular_rank_deficiency() -> None:
    A = np.array([[2.0, 4.0], [1.0, 2.0]])
    assert np.linalg.matrix_rank(A) == 1
    assert abs(np.linalg.det(A)) < 1e-12


def test_near_singular_condition_number() -> None:
    A = np.array([[1.0, 1.0], [1.0, 1.0001]])
    assert np.linalg.cond(A) > 1e4


def test_overdetermined_least_squares() -> None:
    A = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, 1.0],
        [2.0, -1.0],
    ])
    b = np.array([2.02, 0.97, 3.04, 3.03])
    x_hat, *_ = np.linalg.lstsq(A, b, rcond=None)

    assert x_hat.shape == (2,)
    assert np.linalg.norm(A @ x_hat - b) < 0.1


def main() -> None:
    test_well_conditioned_recovery()
    test_singular_rank_deficiency()
    test_near_singular_condition_number()
    test_overdetermined_least_squares()
    print("All inverse recovery diagnostics passed.")


if __name__ == "__main__":
    main()
