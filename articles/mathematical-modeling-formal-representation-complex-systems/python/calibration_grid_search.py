"""
Mathematical Modeling: Calibration by Grid Search

Educational example for estimating a growth parameter by minimizing mean squared error.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from logistic_model import simulate_logistic


def mean_squared_error(observed: np.ndarray, predicted: np.ndarray) -> float:
    """Return mean squared error between observed and predicted values."""
    return float(np.mean((observed - predicted) ** 2))


def main() -> None:
    observations = pd.read_csv("../data/logistic_observations.csv")
    candidate_growth_rates = np.linspace(0.05, 0.35, 61)

    rows = []

    for candidate_rate in candidate_growth_rates:
        candidate_model = simulate_logistic(
            initial_state=float(observations["observed_state"].iloc[0]),
            growth_rate=float(candidate_rate),
            carrying_capacity=100.0,
            time_steps=len(observations)
        )

        mse = mean_squared_error(
            observed=observations["observed_state"].to_numpy(),
            predicted=candidate_model["state"].to_numpy()
        )

        rows.append({
            "candidate_growth_rate": float(candidate_rate),
            "mean_squared_error": mse
        })

    calibration = pd.DataFrame(rows)
    best = calibration.loc[calibration["mean_squared_error"].idxmin()]

    print("Best parameter estimate:")
    print(best)

    calibration.to_csv("../outputs/calibration_grid_search.csv", index=False)


if __name__ == "__main__":
    main()
