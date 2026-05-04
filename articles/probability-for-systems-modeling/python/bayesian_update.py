"""
Probability for Systems Modeling:
Beta-binomial Bayesian updating.

Educational example only.
"""

from __future__ import annotations

import pandas as pd


def beta_binomial_update(prior_alpha: float, prior_beta: float, successes: int, failures: int) -> dict[str, float]:
    """Update a beta prior with binomial observations."""
    posterior_alpha = prior_alpha + successes
    posterior_beta = prior_beta + failures

    prior_mean = prior_alpha / (prior_alpha + prior_beta)
    posterior_mean = posterior_alpha / (posterior_alpha + posterior_beta)

    return {
        "prior_alpha": prior_alpha,
        "prior_beta": prior_beta,
        "successes": successes,
        "failures": failures,
        "posterior_alpha": posterior_alpha,
        "posterior_beta": posterior_beta,
        "prior_mean": prior_mean,
        "posterior_mean": posterior_mean
    }


def main() -> None:
    cases = pd.read_csv("../data/bayesian_update_cases.csv")

    rows = []

    for _, row in cases.iterrows():
        update = beta_binomial_update(
            prior_alpha=float(row["prior_alpha"]),
            prior_beta=float(row["prior_beta"]),
            successes=int(row["successes"]),
            failures=int(row["failures"])
        )

        update["case_id"] = row["case_id"]
        update["description"] = row["description"]
        rows.append(update)

    updates = pd.DataFrame(rows)

    print(updates)

    updates.to_csv("../outputs/python_bayesian_update_results.csv", index=False)


if __name__ == "__main__":
    main()
