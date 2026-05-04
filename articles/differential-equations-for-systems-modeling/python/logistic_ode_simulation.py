"""
Differential Equations for Systems Modeling:
Logistic ODE simulation and sensitivity analysis.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def logistic_rate(state: float, growth_rate: float, capacity: float) -> float:
    """Return dS/dt for logistic growth."""
    return growth_rate * state * (1.0 - state / capacity)


def simulate_logistic_ode(
    initial_state: float,
    growth_rate: float,
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
        derivative[i - 1] = logistic_rate(
            state=state[i - 1],
            growth_rate=growth_rate,
            capacity=capacity
        )
        state[i] = state[i - 1] + derivative[i - 1] * dt
        time[i] = time[i - 1] + dt

    derivative[-1] = logistic_rate(
        state=state[-1],
        growth_rate=growth_rate,
        capacity=capacity
    )

    return pd.DataFrame({
        "time": time,
        "state": state,
        "derivative": derivative,
        "growth_rate": growth_rate,
        "capacity": capacity,
        "dt": dt
    })


def run_parameter_sweep(parameter_grid: pd.DataFrame) -> pd.DataFrame:
    """Run sensitivity sweep over logistic ODE parameters."""
    rows = []

    for _, row in parameter_grid.iterrows():
        simulation = simulate_logistic_ode(
            initial_state=float(row["initial_state"]),
            growth_rate=float(row["growth_rate"]),
            capacity=float(row["capacity"]),
            dt=float(row["dt"]),
            steps=int(row["steps"])
        )

        rows.append({
            "model_name": row["model_name"],
            "growth_rate": row["growth_rate"],
            "capacity": row["capacity"],
            "dt": row["dt"],
            "steps": row["steps"],
            "final_state": float(simulation["state"].iloc[-1]),
            "maximum_state": float(simulation["state"].max()),
            "maximum_derivative": float(simulation["derivative"].max())
        })

    return pd.DataFrame(rows).sort_values("final_state", ascending=False)


def main() -> None:
    parameter_grid = pd.read_csv("../data/ode_parameter_grid.csv")

    baseline = simulate_logistic_ode(
        initial_state=10.0,
        growth_rate=0.20,
        capacity=100.0,
        dt=0.1,
        steps=300
    )

    sensitivity = run_parameter_sweep(parameter_grid)

    phase_values = pd.DataFrame({"state": np.linspace(0, 130, 261)})
    phase_values["derivative"] = phase_values["state"].apply(
        lambda value: logistic_rate(value, growth_rate=0.20, capacity=100.0)
    )

    print(baseline.head())
    print("\nSensitivity summary:")
    print(sensitivity)

    baseline.to_csv("../outputs/python_logistic_ode_baseline.csv", index=False)
    sensitivity.to_csv("../outputs/python_logistic_ode_sensitivity.csv", index=False)
    phase_values.to_csv("../outputs/python_logistic_phase_values.csv", index=False)


if __name__ == "__main__":
    main()
