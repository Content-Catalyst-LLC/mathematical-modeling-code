"""
Differential Equations for Systems Modeling:
Predator-prey coupled ODE system.

Educational example only.
"""

from __future__ import annotations

import pandas as pd


def simulate_predator_prey(
    alpha: float,
    beta: float,
    delta: float,
    gamma: float,
    initial_prey: float,
    initial_predator: float,
    dt: float,
    steps: int
) -> pd.DataFrame:
    """
    Simulate Lotka-Volterra predator-prey dynamics using Euler's method.

    dx/dt = alpha*x - beta*x*y
    dy/dt = delta*x*y - gamma*y
    """
    time = [0.0]
    prey = [initial_prey]
    predator = [initial_predator]

    for i in range(1, steps):
        x = prey[-1]
        y = predator[-1]

        dx = alpha * x - beta * x * y
        dy = delta * x * y - gamma * y

        prey.append(max(x + dx * dt, 0.0))
        predator.append(max(y + dy * dt, 0.0))
        time.append(time[-1] + dt)

    return pd.DataFrame({
        "time": time,
        "prey": prey,
        "predator": predator
    })


def main() -> None:
    params = pd.read_csv("../data/predator_prey_parameters.csv").set_index("parameter")["value"]

    simulation = simulate_predator_prey(
        alpha=float(params["alpha"]),
        beta=float(params["beta"]),
        delta=float(params["delta"]),
        gamma=float(params["gamma"]),
        initial_prey=float(params["initial_prey"]),
        initial_predator=float(params["initial_predator"]),
        dt=float(params["dt"]),
        steps=int(params["steps"])
    )

    summary = pd.DataFrame({
        "metric": [
            "final_prey",
            "final_predator",
            "max_prey",
            "max_predator",
            "min_prey",
            "min_predator"
        ],
        "value": [
            simulation["prey"].iloc[-1],
            simulation["predator"].iloc[-1],
            simulation["prey"].max(),
            simulation["predator"].max(),
            simulation["prey"].min(),
            simulation["predator"].min()
        ]
    })

    print(simulation.head())
    print(summary)

    simulation.to_csv("../outputs/python_predator_prey_simulation.csv", index=False)
    summary.to_csv("../outputs/python_predator_prey_summary.csv", index=False)


if __name__ == "__main__":
    main()
