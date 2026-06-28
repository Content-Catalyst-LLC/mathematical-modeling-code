"""
Applied sensor/state recovery example.

A small sensor matrix maps hidden system state variables to observed readings.
The goal is to recover the hidden state and diagnose whether the sensor layout
supports reliable reconstruction.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Hidden state: [temperature_offset, pressure_offset, flow_offset]
    x_true = np.array([1.5, -0.75, 2.0])

    # Four sensors measuring combinations of the three hidden state variables.
    H = np.array([
        [1.0, 0.0, 0.2],
        [0.0, 1.0, -0.1],
        [1.0, 1.0, 0.0],
        [0.5, -0.2, 1.0],
    ])

    clean_measurements = H @ x_true
    noise = np.array([0.01, -0.02, 0.015, -0.01])
    y = clean_measurements + noise

    x_hat, residuals, rank, singular_values = np.linalg.lstsq(H, y, rcond=None)

    residual = H @ x_hat - y
    state_error = x_hat - x_true

    print("Sensor matrix H =")
    print(H)
    print("rank(H) =", rank)
    print("singular values =", singular_values)
    print("condition number H =", np.linalg.cond(H))
    print("true hidden state =", x_true)
    print("observed measurements y =", y)
    print("estimated hidden state =", x_hat)
    print("state estimation error =", state_error)
    print("measurement residual =", residual)
    print("residual norm =", np.linalg.norm(residual))

    print("\nInterpretation:")
    print("The overdetermined sensor system supports least-squares state recovery.")
    print("Rank and condition number indicate whether the sensor layout is informative and stable.")


if __name__ == "__main__":
    main()
