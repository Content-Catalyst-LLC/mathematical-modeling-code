from __future__ import annotations

from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_differentiability import (
    derivative_diagnostics,
    invariant_review,
    kink_response,
    local_linearization_error,
    records_to_dicts,
    saturation_response,
    smooth_derivative,
    smooth_response,
    write_csv,
    write_json,
)


def main() -> None:
    output_dir = ADVANCED_DIR / "outputs"
    report_dir = output_dir / "reports"
    table_dir = output_dir / "tables"
    json_dir = output_dir / "json"

    h_values = [1.0, 0.5, 0.25, 0.125, 0.0625, -0.0625, -0.125, -0.25, -0.5, -1.0]
    positive_h = sorted([h for h in h_values if h > 0], reverse=True)

    linear_rows = (
        local_linearization_error("smooth_exp_response", smooth_response, smooth_derivative(5.0), 5.0, h_values)
        + local_linearization_error("kink_abs_response", kink_response, 0.0, 0.0, h_values)
        + local_linearization_error("saturation_response_boundary", saturation_response, 1.0, 1.0, h_values)
    )

    diagnostic_rows = (
        derivative_diagnostics("smooth_exp_response", smooth_response, 5.0, positive_h)
        + derivative_diagnostics("kink_abs_response", kink_response, 0.0, positive_h)
        + derivative_diagnostics("saturation_response_boundary", saturation_response, 1.0, positive_h)
    )

    invariant = invariant_review([0.0, 0.25, 0.8, 1.0, -0.05, 1.2], 0.0, 1.0)

    linear_dicts = records_to_dicts(linear_rows)
    diagnostic_dicts = records_to_dicts(diagnostic_rows)
    invariant_dicts = records_to_dicts(invariant)

    write_csv(table_dir / "advanced_local_linearization_error.csv", linear_dicts)
    write_csv(table_dir / "advanced_derivative_diagnostics.csv", diagnostic_dicts)
    write_csv(table_dir / "invariant_review.csv", invariant_dicts)

    flagged_kinks = [row for row in diagnostic_dicts if row["kink_flag"]]
    invariant_failures = [row for row in invariant_dicts if not row["inside"]]

    audit = {
        "article": "Differentiability and Local Behavior",
        "advanced_standard": True,
        "formal_topics": [
            "derivative_as_limit",
            "local_linearization",
            "differentiability_implies_continuity",
            "one_sided_derivatives",
            "partial_vs_full_differentiability",
            "directional_derivatives",
            "frechet_differentiability",
            "gateaux_differentiability",
            "jacobian_local_map",
            "nonsmooth_analysis_warning"
        ],
        "diagnostics": [
            "local_linearization_error",
            "one_sided_derivative_gap",
            "kink_detection",
            "boundary_saturation_review",
            "invariant_interval_review"
        ],
        "flagged_kinks": flagged_kinks,
        "invariant_failures": invariant_failures,
        "warnings": [
            "A symbolic derivative does not establish empirical smoothness.",
            "Partial derivatives do not guarantee full differentiability.",
            "Finite-difference estimates can hide kinks at coarse resolution.",
            "Derivatives are local approximations, not global models.",
            "Boundary derivatives must respect the feasible domain."
        ]
    }

    write_json(json_dir / "advanced_differentiability_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    report = f"""# Advanced Mathematical Audit: Differentiability and Local Behavior

## Formal topics included

- Derivative as limit
- Differentiability as local linear approximation
- Differentiability implies continuity
- One-sided derivatives
- Partial and directional derivatives
- Fréchet and Gâteaux differentiability
- Jacobian as local linear map
- Nonsmooth behavior and generalized-tool warnings

## Diagnostics included

- Local linearization error
- Forward/backward/central finite differences
- One-sided derivative gap
- Kink detection
- Boundary saturation review
- Invariant interval review

## Flagged kink or boundary records

{flagged_kinks}

## Invariant failures

{invariant_failures}

## Mathematical warnings

- A derivative is a local approximation object, not a global model.
- Continuity does not imply differentiability.
- Existence of partial derivatives does not imply full differentiability.
- Directional derivatives can exist without a Fréchet derivative.
- Numerical derivative estimates depend on step size, noise, and hidden nonsmoothness.

## Modeling implication

Derivative-based claims should specify the domain, operating point, perturbation directions, smoothness assumptions, and numerical diagnostics supporting local approximation.
"""

    (report_dir / "advanced_differentiability_audit.md").write_text(report, encoding="utf-8")
    print("Advanced differentiability audit generated.")
    print(report_dir / "advanced_differentiability_audit.md")


if __name__ == "__main__":
    main()
