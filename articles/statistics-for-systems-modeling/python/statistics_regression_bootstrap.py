"""
Statistics for Systems Modeling:
Regression, bootstrap uncertainty, and prediction error.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def generate_synthetic_systems_data(n: int = 250, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic systems data."""
    rng = np.random.default_rng(seed)

    data = pd.DataFrame({
        "exposure": rng.uniform(0, 100, n),
        "capacity": rng.uniform(20, 120, n),
        "governance_quality": rng.uniform(0, 1, n),
        "noise": rng.normal(0, 8, n)
    })

    data["system_burden"] = (
        35
        + 0.42 * data["exposure"]
        - 0.28 * data["capacity"]
        - 14.0 * data["governance_quality"]
        + data["noise"]
    )

    return data


def main() -> None:
    output_dir = "../outputs"

    data = generate_synthetic_systems_data()

    train, test = train_test_split(data, test_size=0.25, random_state=42)

    predictors = ["exposure", "capacity", "governance_quality"]

    x_train = sm.add_constant(train[predictors])
    y_train = train["system_burden"]

    x_test = sm.add_constant(test[predictors])
    y_test = test["system_burden"]

    model = sm.OLS(y_train, x_train).fit()

    predictions = model.predict(x_test)
    test_rmse = mean_squared_error(y_test, predictions, squared=False)

    bootstrap_rows = []

    for i in range(1000):
        sample = train.sample(n=len(train), replace=True, random_state=1000 + i)
        x_boot = sm.add_constant(sample[predictors])
        y_boot = sample["system_burden"]
        boot_model = sm.OLS(y_boot, x_boot).fit()

        bootstrap_rows.append({
            "iteration": i,
            "exposure_coefficient": boot_model.params["exposure"],
            "capacity_coefficient": boot_model.params["capacity"],
            "governance_quality_coefficient": boot_model.params["governance_quality"]
        })

    bootstrap_results = pd.DataFrame(bootstrap_rows)
    bootstrap_summary = bootstrap_results.quantile([0.025, 0.5, 0.975]).T
    bootstrap_summary.columns = ["lower_95", "median", "upper_95"]

    diagnostics = pd.DataFrame({
        "fitted": model.fittedvalues,
        "residual": model.resid
    })

    diagnostic_summary = pd.DataFrame({
        "metric": ["train_rmse", "test_rmse", "residual_mean", "residual_sd"],
        "value": [
            mean_squared_error(y_train, model.fittedvalues, squared=False),
            test_rmse,
            diagnostics["residual"].mean(),
            diagnostics["residual"].std()
        ]
    })

    print(model.summary())
    print(bootstrap_summary)
    print(diagnostic_summary)

    data.to_csv(f"{output_dir}/statistics_systems_data.csv", index=False)
    bootstrap_results.to_csv(f"{output_dir}/bootstrap_coefficients.csv", index=False)
    bootstrap_summary.to_csv(f"{output_dir}/bootstrap_coefficient_summary.csv")
    diagnostics.to_csv(f"{output_dir}/regression_residuals.csv", index=False)
    diagnostic_summary.to_csv(f"{output_dir}/regression_diagnostic_summary.csv", index=False)


if __name__ == "__main__":
    main()
