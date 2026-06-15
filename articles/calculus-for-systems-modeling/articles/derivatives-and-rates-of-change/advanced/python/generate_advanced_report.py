from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_derivative_rates import (
    convergence_orders,
    invariant_review,
    rate_diagnostics,
    roundoff_review,
    to_dicts,
    write_csv,
    write_json,
)


def main() -> None:
    out = ADVANCED_DIR / "outputs"
    table_dir = out / "tables"
    report_dir = out / "reports"
    json_dir = out / "json"

    rates = rate_diagnostics()
    orders = convergence_orders(rates)
    roundoff = roundoff_review()
    invariant = to_dicts(invariant_review([-0.1, 0.0, 0.25, 0.8, 1.0, 1.1]))

    write_csv(table_dir / "advanced_rate_diagnostics.csv", rates)
    write_csv(table_dir / "advanced_convergence_orders.csv", orders)
    write_csv(table_dir / "roundoff_review.csv", roundoff)
    write_csv(table_dir / "invariant_review.csv", invariant)

    audit = {
        "article": "Derivatives and Rates of Change",
        "advanced_standard": True,
        "topics": [
            "average_vs_instantaneous_rate",
            "derivative_as_limit",
            "derivative_as_local_linear_map",
            "units_and_dimensions",
            "one_sided_rates",
            "relative_rates_and_elasticity",
            "vector_fields",
            "finite_difference_error"
        ],
        "warnings": [
            "A derivative is local, not global.",
            "Rates require units and a variable of differentiation.",
            "Elasticity requires positivity and domain checks.",
            "Finite differences require step-size and roundoff review."
        ],
        "invariant_failures": [row for row in invariant if not row["inside"]],
        "roundoff_warnings": [row for row in roundoff if row["warning"]]
    }
    write_json(json_dir / "advanced_derivative_rate_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "advanced_derivative_rate_audit.md").write_text(
        "# Advanced Mathematical Audit: Derivatives and Rates of Change\n\n"
        "## Formal topics included\n\n"
        "- Average versus instantaneous rates\n"
        "- Derivative as a difference-quotient limit\n"
        "- Derivative as local linear map\n"
        "- Units and dimensional interpretation\n"
        "- Relative rates and elasticity\n"
        "- Vector-field rates\n\n"
        "## Numerical diagnostics included\n\n"
        "- Forward and central finite differences\n"
        "- Convergence-order estimates\n"
        "- Roundoff and cancellation review\n"
        "- Invariant-domain review\n\n"
        "## Modeling implication\n\n"
        "A derivative-based claim should specify what is changing, with respect to what, at which operating point, in which units, under which smoothness assumptions, and with what numerical evidence.\n",
        encoding="utf-8"
    )

    print("Advanced derivative-rate audit generated.")


if __name__ == "__main__":
    main()
