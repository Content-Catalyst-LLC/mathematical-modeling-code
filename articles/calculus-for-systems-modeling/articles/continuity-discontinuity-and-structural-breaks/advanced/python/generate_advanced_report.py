from __future__ import annotations

from pathlib import Path
import sys

CURRENT = Path(__file__).resolve()
ADVANCED_DIR = CURRENT.parents[1]
sys.path.insert(0, str(CURRENT.parent))

from advanced_continuity import (
    diagnose_breaks,
    invariant_review,
    piecewise_system,
    records_to_dicts,
    regularity_examples,
    write_csv,
    write_json,
)


def main() -> None:
    output_dir = ADVANCED_DIR / "outputs"
    report_dir = output_dir / "reports"
    table_dir = output_dir / "tables"
    json_dir = output_dir / "json"

    xs = [i * 0.25 for i in range(41)]
    ys = [piecewise_system(x) for x in xs]
    breaks = diagnose_breaks(xs, ys)
    regularities = regularity_examples()
    invariant = invariant_review([0.0, 0.4, 1.0, -0.1, 1.2], 0.0, 1.0)

    break_dicts = records_to_dicts(breaks)
    regularity_dicts = records_to_dicts(regularities)
    invariant_dicts = records_to_dicts(invariant)

    write_csv(table_dir / "advanced_break_diagnostics.csv", break_dicts)
    write_csv(table_dir / "advanced_regularities.csv", regularity_dicts)
    write_csv(table_dir / "invariant_review.csv", invariant_dicts)

    flagged = [row for row in break_dicts if row["flag"] != "ok"]
    invariant_failures = [row for row in invariant_dicts if not row["inside"]]

    audit = {
        "article": "Continuity, Discontinuity, and Structural Breaks",
        "advanced_standard": True,
        "formal_topics": [
            "epsilon_delta_continuity",
            "sequential_continuity",
            "topological_continuity",
            "subspace_continuity",
            "uniform_continuity",
            "lipschitz_continuity",
            "absolute_continuity",
            "semicontinuity",
            "structural_breaks"
        ],
        "diagnostics": [
            "level_jump_detection",
            "slope_break_detection",
            "piecewise_model_review",
            "invariant_interval_review",
            "regularity_examples"
        ],
        "flagged_breaks": flagged,
        "invariant_failures": invariant_failures,
        "warnings": [
            "A diagnostic flag is not proof of a real structural break.",
            "Noise, sampling frequency, smoothing, and measurement error affect discontinuity detection.",
            "A function can be continuous but not differentiable.",
            "A structural break can change slope, variance, parameters, or mechanism even when level remains continuous."
        ]
    }

    write_json(json_dir / "advanced_continuity_audit.json", audit)

    report_dir.mkdir(parents=True, exist_ok=True)
    report = f"""# Advanced Mathematical Audit: Continuity, Discontinuity, and Structural Breaks

## Formal topics included

- Epsilon-delta continuity
- Sequential and metric-space continuity
- Topological continuity
- Subspace continuity
- One-sided continuity
- Uniform continuity
- Lipschitz continuity
- Absolute continuity
- Semicontinuity
- Structural breaks and piecewise models

## Diagnostics included

- Level-jump detection
- Slope-break detection
- Piecewise-model review
- Invariant interval review
- Regularity example registry

## Flagged break candidates

{flagged}

## Invariant failures

{invariant_failures}

## Mathematical warnings

- Continuity is a representational assumption, not a default property of reality.
- Discontinuity can represent real thresholds, but it can also be created by noise or sampling.
- Differentiability implies continuity, but continuity does not imply differentiability.
- Pointwise convergence of continuous functions does not necessarily preserve continuity.
- Structural breaks can occur in level, slope, variance, parameters, governing equations, or mechanism.

## Modeling implication

A model should state its regularity assumptions: continuous, uniformly continuous, Lipschitz, differentiable, smooth, absolutely continuous, semicontinuous, piecewise continuous, or discontinuous.
"""

    (report_dir / "advanced_continuity_audit.md").write_text(report, encoding="utf-8")
    print("Advanced continuity audit generated.")
    print(report_dir / "advanced_continuity_audit.md")


if __name__ == "__main__":
    main()
