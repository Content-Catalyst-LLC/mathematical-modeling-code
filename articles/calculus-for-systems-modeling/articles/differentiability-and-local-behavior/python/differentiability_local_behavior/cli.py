from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from differentiability_local_behavior.core import (
    finite_difference_diagnostics,
    kink_response,
    load_h_values,
    local_linearization_error,
    smooth_derivative,
    smooth_response,
    to_dicts,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run differentiability and local behavior diagnostics.")
    parser.add_argument("--h-file", type=Path, default=Path("data/local_linearization_steps.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    h_values = load_h_values(args.h_file)
    positive_h_values = sorted([h for h in h_values if h > 0], reverse=True)

    smooth_linear = local_linearization_error(
        "smooth_exp_response",
        smooth_response,
        smooth_derivative(5.0),
        5.0,
        h_values,
    )

    kink_linear = local_linearization_error(
        "kink_abs_response",
        kink_response,
        0.0,
        0.0,
        h_values,
    )

    smooth_fd = finite_difference_diagnostics("smooth_exp_response", smooth_response, 5.0, positive_h_values)
    kink_fd = finite_difference_diagnostics("kink_abs_response", kink_response, 0.0, positive_h_values)

    write_csv(args.output_dir / "tables" / "local_linearization_error.csv", to_dicts(smooth_linear + kink_linear))
    write_csv(args.output_dir / "tables" / "finite_difference_kink_diagnostics.csv", to_dicts(smooth_fd + kink_fd))

    flagged = [row for row in kink_fd if row.kink_flag]
    manifest = {
        "article": "Differentiability and Local Behavior",
        "series": "Calculus for Systems Modeling",
        "advanced_standard": True,
        "methods": ["local_linearization_error", "forward_difference", "backward_difference", "central_difference", "one_sided_gap"],
        "flagged_kink_records": len(flagged),
        "interpretive_warning": "Finite-difference diagnostics are evidence for review, not proof of differentiability or nondifferentiability.",
    }
    write_json(args.output_dir / "json" / "differentiability_manifest.json", manifest)

    log_path = args.output_dir / "logs" / "python_workflow.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Differentiability local behavior workflow completed.\n", encoding="utf-8")

    print("Differentiability and local behavior workflow complete.")
    print(f"h values: {len(h_values)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
