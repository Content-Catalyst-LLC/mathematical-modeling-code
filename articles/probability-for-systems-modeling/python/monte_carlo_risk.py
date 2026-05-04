"""
Probability for Systems Modeling:
Monte Carlo risk simulation.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_system_loss(
    exposure_min: float,
    exposure_max: float,
    vulnerability_alpha: float,
    vulnerability_beta: float,
    shock_meanlog: float,
    shock_sdlog: float,
    iterations: int,
    seed: int
) -> pd.DataFrame:
    """Simulate uncertain system loss from exposure, vulnerability, and shock intensity."""
    rng = np.random.default_rng(seed)

    exposure = rng.uniform(exposure_min, exposure_max, iterations)
    vulnerability = rng.beta(vulnerability_alpha, vulnerability_beta, iterations)
    shock_intensity = rng.lognormal(mean=shock_meanlog, sigma=shock_sdlog, size=iterations)

    system_loss = exposure * vulnerability * shock_intensity

    return pd.DataFrame({
        "exposure": exposure,
        "vulnerability": vulnerability,
        "shock_intensity": shock_intensity,
        "system_loss": system_loss
    })


def summarize_loss(simulation: pd.DataFrame) -> dict[str, float]:
    """Summarize simulated loss distribution."""
    return {
        "expected_loss": float(simulation["system_loss"].mean()),
        "median_loss": float(simulation["system_loss"].median()),
        "loss_sd": float(simulation["system_loss"].std()),
        "p90_loss": float(simulation["system_loss"].quantile(0.90)),
        "p95_loss": float(simulation["system_loss"].quantile(0.95)),
        "p99_loss": float(simulation["system_loss"].quantile(0.99)),
        "probability_loss_gt_0_50": float((simulation["system_loss"] > 0.50).mean())
    }


def main() -> None:
    parameters = pd.read_csv("../data/monte_carlo_risk_parameters.csv")

    all_results = []
    summary_rows = []

    for i, row in parameters.iterrows():
        simulation = simulate_system_loss(
            exposure_min=float(row["exposure_min"]),
            exposure_max=float(row["exposure_max"]),
            vulnerability_alpha=float(row["vulnerability_alpha"]),
            vulnerability_beta=float(row["vulnerability_beta"]),
            shock_meanlog=float(row["shock_meanlog"]),
            shock_sdlog=float(row["shock_sdlog"]),
            iterations=int(row["iterations"]),
            seed=42 + i
        )

        simulation["scenario_id"] = row["scenario_id"]
        all_results.append(simulation)

        summary = summarize_loss(simulation)
        summary["scenario_id"] = row["scenario_id"]
        summary_rows.append(summary)

    results = pd.concat(all_results, ignore_index=True)
    summary = pd.DataFrame(summary_rows)

    print(summary)

    results.to_csv("../outputs/python_monte_carlo_risk_results.csv", index=False)
    summary.to_csv("../outputs/python_monte_carlo_risk_summary.csv", index=False)


if __name__ == "__main__":
    main()
