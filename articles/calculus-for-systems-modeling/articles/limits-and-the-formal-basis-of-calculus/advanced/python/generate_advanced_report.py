from __future__ import annotations

from pathlib import Path
import statistics
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_limits import (
    convergence_orders,
    convergence_study,
    invariant_review,
    records_to_dicts,
    roundoff_review,
    write_csv,
    write_json,
)


def main() -> None:
    output_dir = ADVANCED_DIR / "outputs"
    report_dir = output_dir / "reports"
    table_dir = output_dir / "tables"
    json_dir = output_dir / "json"

    rows = convergence_study()
    orders = convergence_orders(rows)
    roundoff = roundoff_review()
    invariant = invariant_review([0.0, 0.2, 0.8, 1.0, -0.05, 1.1], 0.0, 1.0)

    rows_dict = records_to_dicts(rows)
    orders_dict = records_to_dicts(orders)
    invariant_dict = records_to_dicts(invariant)

    write_csv(table_dir / "advanced_convergence_study.csv", rows_dict)
    write_csv(table_dir / "advanced_convergence_orders.csv", orders_dict)
    write_csv(table_dir / "roundoff_review.csv", roundoff)
    write_csv(table_dir / "invariant_review.csv", invariant_dict)

    median_orders = {}
    for method in sorted({row["method"] for row in orders_dict}):
        values = [float(row["estimated_order"]) for row in orders_dict if row["method"] == method]
        if values:
            median_orders[method] = statistics.median(values)

    audit = {
        "article": "Limits and the Formal Basis of Calculus",
        "advanced_standard": True,
        "formal_topics": [
            "epsilon_delta_definition",
            "sequential_characterization",
            "metric_space_limits",
            "uniform_vs_pointwise_convergence",
            "noncommuting_limits",
            "boundary_and_pathology_review"
        ],
        "numerical_methods": [
            "forward_difference",
            "central_difference",
            "richardson_extrapolation",
            "convergence_order_estimation",
            "roundoff_review",
            "invariant_interval_review"
        ],
        "median_estimated_orders": median_orders,
        "invariant_failures": [row for row in invariant_dict if not row["inside"]],
        "warnings": [
            "Finite numerical approximations do not prove formal limits.",
            "Pointwise convergence does not imply uniform convergence.",
            "Interchanging limits with derivatives, integrals, expectations, or optimization requires additional hypotheses.",
            "Shrinking step size can eventually worsen finite-difference estimates because of roundoff and cancellation."
        ]
    }

    write_json(json_dir / "advanced_limits_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    report = f"""# Advanced Mathematical Audit: Limits and the Formal Basis of Calculus

## Formal topics included

- Epsilon-delta limits
- Sequential characterization
- Metric-space limits
- Pointwise versus uniform convergence
- Noncommuting limits and operations
- Boundary/pathology review

## Numerical methods included

- Forward difference
- Central difference
- Richardson extrapolation
- Convergence-order estimation
- Roundoff and cancellation review
- Invariant interval review

## Median estimated convergence orders

{median_orders}

## Invariant failures

{audit["invariant_failures"]}

## Mathematical warnings

- A numerical convergence table is not a proof of a mathematical limit.
- A mathematical limit can be formally correct while remaining empirically irrelevant to a model.
- Pointwise convergence is insufficient for many preservation claims.
- Interchanging limits with integrals, derivatives, expectations, or optimization requires explicit justification.
- Boundary behavior should be analyzed separately from interior behavior.

## Modeling implication

A limit statement should specify the domain, codomain, topology or metric, convergence mode, and operation being preserved.
"""

    (report_dir / "advanced_limits_audit.md").write_text(report, encoding="utf-8")
    print("Advanced limits audit generated.")
    print(report_dir / "advanced_limits_audit.md")


if __name__ == "__main__":
    main()
