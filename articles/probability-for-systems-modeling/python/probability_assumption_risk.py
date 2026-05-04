"""
Probability for Systems Modeling:
Assumption risk scoring.

Educational example only.
"""

from __future__ import annotations

import pandas as pd


def main() -> None:
    assumptions = pd.read_csv("../data/probability_assumptions.csv")

    assumptions["risk_score"] = (
        (1.0 - assumptions["confidence"]) * assumptions["impact_if_wrong"]
    )

    assumptions = assumptions.sort_values("risk_score", ascending=False)

    print(assumptions)

    assumptions.to_csv("../outputs/python_probability_assumption_risk.csv", index=False)


if __name__ == "__main__":
    main()
