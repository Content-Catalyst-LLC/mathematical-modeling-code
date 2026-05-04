"""
Differential Equations for Systems Modeling:
SIR epidemiological model.

Educational example only.
"""

from __future__ import annotations

import pandas as pd


def simulate_sir(
    beta: float,
    gamma: float,
    initial_susceptible: float,
    initial_infected: float,
    initial_recovered: float,
    dt: float,
    steps: int
) -> pd.DataFrame:
    """
    Simulate SIR dynamics using Euler's method.

    dS/dt = -beta*S*I/N
    dI/dt = beta*S*I/N - gamma*I
    dR/dt = gamma*I
    """
    susceptible = [initial_susceptible]
    infected = [initial_infected]
    recovered = [initial_recovered]
    time = [0.0]

    population = initial_susceptible + initial_infected + initial_recovered

    for i in range(1, steps):
        s = susceptible[-1]
        infected_current = infected[-1]
        r = recovered[-1]

        d_s = -beta * s * infected_current / population
        d_i = beta * s * infected_current / population - gamma * infected_current
        d_r = gamma * infected_current

        susceptible.append(max(s + d_s * dt, 0.0))
        infected.append(max(infected_current + d_i * dt, 0.0))
        recovered.append(max(r + d_r * dt, 0.0))
        time.append(time[-1] + dt)

    return pd.DataFrame({
        "time": time,
        "susceptible": susceptible,
        "infected": infected,
        "recovered": recovered
    })


def main() -> None:
    params = pd.read_csv("../data/sir_parameters.csv").set_index("parameter")["value"]

    simulation = simulate_sir(
        beta=float(params["beta"]),
        gamma=float(params["gamma"]),
        initial_susceptible=float(params["initial_susceptible"]),
        initial_infected=float(params["initial_infected"]),
        initial_recovered=float(params["initial_recovered"]),
        dt=float(params["dt"]),
        steps=int(params["steps"])
    )

    summary = pd.DataFrame({
        "metric": [
            "peak_infected",
            "time_of_peak",
            "final_susceptible",
            "final_recovered"
        ],
        "value": [
            simulation["infected"].max(),
            simulation.loc[simulation["infected"].idxmax(), "time"],
            simulation["susceptible"].iloc[-1],
            simulation["recovered"].iloc[-1]
        ]
    })

    print(simulation.head())
    print(summary)

    simulation.to_csv("../outputs/python_sir_simulation.csv", index=False)
    summary.to_csv("../outputs/python_sir_summary.csv", index=False)


if __name__ == "__main__":
    main()
