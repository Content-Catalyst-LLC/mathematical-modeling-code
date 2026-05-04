"""
Scientific Computing for Systems Modeling:
Monte Carlo uncertainty workflow.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from simulation_workflow import simulate_logistic


def main() -> None:
    rng = np.random.default_rng(42)
    scenarios = pd.read_csv("../data/monte_carlo_parameters.csv")

    rows = []

    for _, scenario in scenarios.iterrows():
        for iteration in range(int(scenario["iterations"])):
            sampled_growth_rate = max(
                rng.normal(
                    loc=float(scenario["mean_growth_rate"]),
                    scale=float(scenario["sd_growth_rate"])
                ),
                0.0
            )

            simulation = simulate_logistic(
                initial_state=float(scenario["initial_state"]),
                growth_rate=sampled_growth_rate,
                capacity=float(scenario["capacity"]),
                dt=float(scenario["dt"]),
                steps=int(scenario["steps"])
            )

            rows.append({
                "scenario_id": scenario["scenario_id"],
                "iteration": iteration,
                "sampled_growth_rate": sampled_growth_rate,
                "final_state": float(simulation["state"].iloc[-1]),
                "maximum_state": float(simulation["state"].max())
            })

    results = pd.DataFrame(rows)

    summary = results.groupby("scenario_id").agg(
        final_state_mean=("final_state", "mean"),
        final_state_p05=("final_state", lambda x: x.quantile(0.05)),
        final_state_p50=("final_state", lambda x: x.quantile(0.50)),
        final_state_p95=("final_state", lambda x: x.quantile(0.95)),
        maximum_state_mean=("maximum_state", "mean")
    ).reset_index()

    print(summary)

    results.to_csv("../outputs/python_monte_carlo_results.csv", index=False)
    summary.to_csv("../outputs/python_monte_carlo_summary.csv", index=False)


if __name__ == "__main__":
    main()
