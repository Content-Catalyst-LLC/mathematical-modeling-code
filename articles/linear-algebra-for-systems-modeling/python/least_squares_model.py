"""
Linear Algebra for Systems Modeling:
Least-squares approximation.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def main() -> None:
    observations = pd.read_csv("../data/systems_observations.csv")

    X_raw = observations[[
        "infrastructure_capacity",
        "ecological_resilience",
        "governance_quality"
    ]].to_numpy(dtype=float)

    y = observations["economic_activity"].to_numpy(dtype=float)

    X = np.column_stack([np.ones(X_raw.shape[0]), X_raw])

    coefficients, residuals, rank, singular_values = np.linalg.lstsq(X, y, rcond=None)

    fitted = X @ coefficients
    residual = y - fitted

    coefficient_summary = pd.DataFrame({
        "term": ["intercept", "infrastructure_capacity", "ecological_resilience", "governance_quality"],
        "coefficient": coefficients
    })

    diagnostic_summary = pd.DataFrame({
        "metric": ["rank", "rmse", "residual_sum_of_squares"],
        "value": [
            rank,
            float(np.sqrt(np.mean(residual**2))),
            float(np.sum(residual**2))
        ]
    })

    fitted_results = pd.DataFrame({
        "observation_id": observations["observation_id"],
        "observed": y,
        "fitted": fitted,
        "residual": residual
    })

    print(coefficient_summary)
    print(diagnostic_summary)

    coefficient_summary.to_csv("../outputs/python_least_squares_coefficients.csv", index=False)
    diagnostic_summary.to_csv("../outputs/python_least_squares_diagnostics.csv", index=False)
    fitted_results.to_csv("../outputs/python_least_squares_fitted.csv", index=False)


if __name__ == "__main__":
    main()
