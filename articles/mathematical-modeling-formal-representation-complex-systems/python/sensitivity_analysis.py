"""
Mathematical Modeling: Sensitivity Analysis

Educational example for testing model response across parameter combinations.
"""

from __future__ import annotations

import pandas as pd

from logistic_model import simulate_logistic


def main() -> None:
    parameter_grid = pd.read_csv("../data/model_parameter_grid.csv")
    results = []

    for _, row in parameter_grid.iterrows():
        simulation = simulate_logistic(
            initial_state=10.0,
            growth_rate=float(row["growth_rate"]),
            carrying_capacity=float(row["carrying_capacity"]),
            time_steps=80
        )

        results.append({
            "growth_rate": row["growth_rate"],
            "carrying_capacity": row["carrying_capacity"],
            "final_state": float(simulation["state"].iloc[-1]),
            "maximum_state": float(simulation["state"].max())
        })

    sensitivity = pd.DataFrame(results).sort_values("final_state", ascending=False)

    print(sensitivity)

    sensitivity.to_csv("../outputs/logistic_sensitivity_summary.csv", index=False)


if __name__ == "__main__":
    main()
