"""
Mathematical Modeling: Logistic Growth Simulation

Educational example for simulating a discrete logistic model.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_logistic(
    initial_state: float,
    growth_rate: float,
    carrying_capacity: float,
    time_steps: int
) -> pd.DataFrame:
    """Simulate a discrete logistic growth model."""
    state = np.zeros(time_steps)
    state[0] = initial_state

    for t in range(1, time_steps):
        state[t] = (
            state[t - 1]
            + growth_rate * state[t - 1] * (1.0 - state[t - 1] / carrying_capacity)
        )

    return pd.DataFrame({
        "time": np.arange(time_steps),
        "state": state,
        "growth_rate": growth_rate,
        "carrying_capacity": carrying_capacity
    })


def main() -> None:
    simulation = simulate_logistic(
        initial_state=10.0,
        growth_rate=0.18,
        carrying_capacity=100.0,
        time_steps=80
    )

    print(simulation.head())

    simulation.to_csv("../outputs/logistic_baseline_simulation.csv", index=False)


if __name__ == "__main__":
    main()
