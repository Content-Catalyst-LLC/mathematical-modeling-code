"""
Probability for Systems Modeling:
Rare-event threshold simulation.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def main() -> None:
    rng = np.random.default_rng(42)

    iterations = 200000

    baseline_load = rng.normal(loc=0.0, scale=1.0, size=iterations)
    extreme_shock = rng.lognormal(mean=-0.5, sigma=0.9, size=iterations)
    dependence_factor = rng.beta(2, 6, size=iterations)

    stress_index = baseline_load + extreme_shock * (1 + dependence_factor)

    threshold = np.quantile(stress_index, 0.995)

    summary = pd.DataFrame({
        "metric": [
            "mean_stress",
            "sd_stress",
            "p95_stress",
            "p99_stress",
            "p995_stress",
            "probability_exceeds_3"
        ],
        "value": [
            stress_index.mean(),
            stress_index.std(),
            np.quantile(stress_index, 0.95),
            np.quantile(stress_index, 0.99),
            threshold,
            np.mean(stress_index > 3)
        ]
    })

    outputs = pd.DataFrame({
        "stress_index": stress_index
    })

    print(summary)

    outputs.to_csv("../outputs/python_rare_event_simulation.csv", index=False)
    summary.to_csv("../outputs/python_rare_event_summary.csv", index=False)


if __name__ == "__main__":
    main()
