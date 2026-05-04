"""
Scientific Computing for Systems Modeling:
Simulation workflow and parameter sweep.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_logistic(
    initial_state: float,
    growth_rate: float,
    capacity: float,
    dt: float,
    steps: int
) -> pd.DataFrame:
    """Simulate a logistic dynamic system using Euler's method."""
    time = np.zeros(steps)
    state = np.zeros(steps)

    state[0] = initial_state

    for i in range(1, steps):
        derivative = growth_rate * state[i - 1] * (1.0 - state[i - 1] / capacity)
        state[i] = state[i - 1] + derivative * dt
        time[i] = time[i - 1] + dt

    return pd.DataFrame({
        "time": time,
        "state": state,
        "growth_rate": growth_rate,
        "capacity": capacity,
        "dt": dt
    })


def main() -> None:
    parameter_grid = pd.read_csv("../data/simulation_parameter_grid.csv")

    all_simulations = []
    summary_rows = []

    for _, row in parameter_grid.iterrows():
        simulation = simulate_logistic(
            initial_state=float(row["initial_state"]),
            growth_rate=float(row["growth_rate"]),
            capacity=float(row["capacity"]),
            dt=float(row["dt"]),
            steps=int(row["steps"])
        )

        simulation["scenario_id"] = row["scenario_id"]
        all_simulations.append(simulation)

        summary_rows.append({
            "scenario_id": row["scenario_id"],
            "growth_rate": row["growth_rate"],
            "capacity": row["capacity"],
            "dt": row["dt"],
            "final_state": float(simulation["state"].iloc[-1]),
            "maximum_state": float(simulation["state"].max()),
            "mean_state": float(simulation["state"].mean())
        })

    simulation_results = pd.concat(all_simulations, ignore_index=True)
    summary = pd.DataFrame(summary_rows).sort_values("final_state", ascending=False)

    print(summary)

    simulation_results.to_csv("../outputs/python_simulation_results.csv", index=False)
    summary.to_csv("../outputs/python_simulation_summary.csv", index=False)


if __name__ == "__main__":
    main()
