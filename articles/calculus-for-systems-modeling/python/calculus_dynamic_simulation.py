"""
Calculus for Systems Modeling:
Numerical calculus and dynamic simulation.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_logistic(
    initial_state: float,
    rate: float,
    capacity: float,
    dt: float,
    steps: int
) -> pd.DataFrame:
    """Simulate dS/dt = rS(1 - S/K) using Euler's method."""
    time = np.zeros(steps)
    state = np.zeros(steps)
    derivative = np.zeros(steps)

    state[0] = initial_state

    for i in range(1, steps):
        derivative[i - 1] = rate * state[i - 1] * (1.0 - state[i - 1] / capacity)
        state[i] = state[i - 1] + derivative[i - 1] * dt
        time[i] = time[i - 1] + dt

    derivative[-1] = rate * state[-1] * (1.0 - state[-1] / capacity)

    return pd.DataFrame({
        "time": time,
        "state": state,
        "derivative": derivative,
        "rate": rate,
        "capacity": capacity
    })


def cumulative_trapezoid(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Approximate cumulative integral using the trapezoid rule."""
    cumulative = np.zeros_like(y)

    for i in range(1, len(y)):
        width = x[i] - x[i - 1]
        area = 0.5 * (y[i] + y[i - 1]) * width
        cumulative[i] = cumulative[i - 1] + area

    return cumulative


def main() -> None:
    output_dir = "../outputs"

    simulation = simulate_logistic(
        initial_state=10.0,
        rate=0.20,
        capacity=100.0,
        dt=0.1,
        steps=300
    )

    simulation["cumulative_state"] = cumulative_trapezoid(
        simulation["time"].to_numpy(),
        simulation["state"].to_numpy()
    )

    parameter_grid = pd.read_csv("../data/calculus_parameter_grid.csv")

    rows = []

    for _, row in parameter_grid.iterrows():
        result = simulate_logistic(
            initial_state=float(row["initial_state"]),
            rate=float(row["rate"]),
            capacity=float(row["capacity"]),
            dt=float(row["dt"]),
            steps=int(row["steps"])
        )

        rows.append({
            "rate": row["rate"],
            "capacity": row["capacity"],
            "final_state": float(result["state"].iloc[-1]),
            "maximum_state": float(result["state"].max()),
            "maximum_derivative": float(result["derivative"].max())
        })

    sensitivity = pd.DataFrame(rows).sort_values("final_state", ascending=False)

    print(simulation.head())
    print(sensitivity)

    simulation.to_csv(f"{output_dir}/calculus_dynamic_simulation.csv", index=False)
    sensitivity.to_csv(f"{output_dir}/calculus_sensitivity_summary.csv", index=False)


if __name__ == "__main__":
    main()
