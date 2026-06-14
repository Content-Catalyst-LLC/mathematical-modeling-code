from __future__ import annotations

from pathlib import Path
import statistics
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
ARTICLE_DIR = ADVANCED_DIR.parent

sys.path.insert(0, str(CURRENT.parent))

from advanced_calculus_checks import (
    check_interval_invariant,
    convergence_study,
    estimate_convergence_orders,
    records_to_dicts,
    roundoff_review,
    write_csv,
    write_json,
)


ARTICLE_TITLE = "What Is Calculus for Systems Modeling?"
ARTICLE_SLUG = "what-is-calculus-for-systems-modeling"
ARTICLE_FOCUS = "calculus for systems modeling"


def main() -> None:
    output_dir = ADVANCED_DIR / "outputs"
    report_dir = output_dir / "reports"
    table_dir = output_dir / "tables"
    json_dir = output_dir / "json"

    rows = convergence_study()
    orders = estimate_convergence_orders(rows)
    roundoff = roundoff_review()

    invariant_values = [0.0, 0.25, 0.5, 0.75, 1.0, -0.1, 1.2]
    invariant_reviews = check_interval_invariant(invariant_values, 0.0, 1.0)

    rows_dict = records_to_dicts(rows)
    orders_dict = records_to_dicts(orders)
    invariant_dict = records_to_dicts(invariant_reviews)

    write_csv(table_dir / "convergence_study.csv", rows_dict)
    write_csv(table_dir / "convergence_orders.csv", orders_dict)
    write_csv(table_dir / "invariant_review.csv", invariant_dict)
    write_csv(table_dir / "roundoff_review.csv", roundoff)

    median_orders: dict[str, float] = {}
    for method in sorted({row["method"] for row in orders_dict}):
        vals = [float(row["estimated_order"]) for row in orders_dict if row["method"] == method and float(row["estimated_order"]) == float(row["estimated_order"])]
        if vals:
            median_orders[method] = statistics.median(vals)

    audit = {
        "article_title": ARTICLE_TITLE,
        "article_slug": ARTICLE_SLUG,
        "advanced_focus": ARTICLE_FOCUS,
        "methods": [
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
            "Synthetic smooth function used for numerical review.",
            "Convergence in the test function does not validate empirical modeling assumptions.",
            "Small step sizes can increase roundoff and cancellation error.",
            "Formal article sections should distinguish definition, proposition, counterexample, and boundary behavior."
        ]
    }

    write_json(json_dir / "advanced_math_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    report = f"""# Advanced Mathematical Audit: {ARTICLE_TITLE}

## Article focus

{ARTICLE_FOCUS}

## Methods included

- Forward difference
- Central difference
- Richardson extrapolation
- Estimated convergence order
- Roundoff-window review
- Invariant interval review

## Median estimated convergence orders

{median_orders}

## Invariant review

The invariant interval test uses the interval \\(0 \\le x \\le 1\\) and intentionally includes invalid values so that boundary violations are detected.

Invalid values found:

{audit["invariant_failures"]}

## Mathematical standard for article prose

Future revisions of this article should include a **Mathematical Deepening** section with:

- formal definitions;
- a proposition or lemma where useful;
- at least one counterexample or boundary case;
- explicit assumptions;
- codomain/image/range or state-space distinctions where relevant;
- convergence, stability, conditioning, or approximation notes where computation is involved.

## Interpretation warning

This advanced audit strengthens the companion workflow, but it does not turn a teaching example into empirical validation. The mathematical result remains conditional on definitions, assumptions, domain, smoothness, numerical method, and interpretation.
"""
    (report_dir / "advanced_math_audit.md").write_text(report, encoding="utf-8")

    print(f"Advanced audit generated for {ARTICLE_TITLE}")
    print(report_dir / "advanced_math_audit.md")


if __name__ == "__main__":
    main()
