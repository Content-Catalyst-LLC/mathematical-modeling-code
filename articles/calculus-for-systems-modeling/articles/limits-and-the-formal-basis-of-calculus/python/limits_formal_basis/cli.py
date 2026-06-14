from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from limits_formal_basis.core import (
    convergence_orders,
    convergence_study,
    epsilon_band_review,
    load_epsilons,
    load_step_sizes,
    to_dicts,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run limit convergence workflow.")
    parser.add_argument("--step-file", type=Path, default=Path("data/step_sizes.csv"))
    parser.add_argument("--epsilon-file", type=Path, default=Path("data/epsilon_bands.csv"))
    parser.add_argument("--x", type=float, default=5.0)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    h_values = load_step_sizes(args.step_file)
    epsilons = load_epsilons(args.epsilon_file)

    rows = convergence_study(args.x, h_values)
    orders = convergence_orders(rows)
    epsilon_review = epsilon_band_review(rows, epsilons)

    write_csv(args.output_dir / "tables" / "limit_convergence_study.csv", to_dicts(rows))
    write_csv(args.output_dir / "tables" / "limit_convergence_orders.csv", orders)
    write_csv(args.output_dir / "tables" / "epsilon_band_review.csv", epsilon_review)

    manifest = {
        "article": "Limits and the Formal Basis of Calculus",
        "series": "Calculus for Systems Modeling",
        "advanced_standard": True,
        "methods": ["forward_difference", "central_difference", "richardson_extrapolation", "epsilon_band_review"],
        "interpretive_warning": "Finite numerical approximations support but do not replace formal limiting arguments.",
    }
    write_json(args.output_dir / "json" / "limit_convergence_manifest.json", manifest)

    log_path = args.output_dir / "logs" / "python_workflow.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Limit convergence workflow completed.\n", encoding="utf-8")

    print("Limit convergence workflow complete.")
    print(f"Step sizes: {len(h_values)}")
    print(f"Epsilon bands: {len(epsilons)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
