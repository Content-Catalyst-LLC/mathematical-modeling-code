from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

from derivatives_rates_change.core import (
    convergence_orders,
    load_h_values,
    rate_diagnostics,
    to_dicts,
    vector_field_records,
    write_csv,
    write_json,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h-file", type=Path, default=Path("data/rate_steps.csv"))
    parser.add_argument("--x0", type=float, default=5.0)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    h_values = load_h_values(args.h_file)
    rates = rate_diagnostics(args.x0, h_values)
    orders = convergence_orders(rates)
    vectors = vector_field_records([-0.1, 0.0, 0.25, 0.5, 1.0, 1.1])

    write_csv(args.output_dir / "tables" / "rate_diagnostics.csv", to_dicts(rates))
    write_csv(args.output_dir / "tables" / "rate_convergence_orders.csv", orders)
    write_csv(args.output_dir / "tables" / "vector_field_invariant_review.csv", to_dicts(vectors))

    write_json(args.output_dir / "json" / "derivative_rate_manifest.json", {
        "article": "Derivatives and Rates of Change",
        "advanced_standard": True,
        "methods": ["average_rate", "forward_difference", "backward_difference", "central_difference", "elasticity", "vector_field_review"],
        "warning": "Finite-difference derivatives are approximations, not proof of differentiability."
    })

    (args.output_dir / "logs").mkdir(parents=True, exist_ok=True)
    (args.output_dir / "logs" / "python_workflow.log").write_text("Derivatives and rates workflow completed.\n", encoding="utf-8")
    print("Derivatives and rates workflow complete.")


if __name__ == "__main__":
    main()
