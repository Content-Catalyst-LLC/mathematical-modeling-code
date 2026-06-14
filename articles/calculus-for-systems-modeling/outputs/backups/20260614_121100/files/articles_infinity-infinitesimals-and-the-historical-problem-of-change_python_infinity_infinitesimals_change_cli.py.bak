from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from infinity_infinitesimals_change.core import (
    build_manifest,
    load_step_sizes,
    run_approximations,
    summarize_approximations,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run difference quotient convergence workflow.")
    parser.add_argument("--step-file", type=Path, default=Path("data/step_sizes.csv"))
    parser.add_argument("--x", type=float, default=5.0)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    h_values = load_step_sizes(args.step_file)
    records = run_approximations(args.x, h_values)
    rows = [asdict(item) for item in records]
    summary = summarize_approximations(records)

    write_csv(args.output_dir / "tables" / "difference_quotient_convergence.csv", rows)
    write_csv(args.output_dir / "tables" / "difference_quotient_summary.csv", summary)
    write_json(args.output_dir / "json" / "difference_quotient_manifest.json", build_manifest(records))

    log_path = args.output_dir / "logs" / "python_workflow.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Difference quotient convergence workflow completed.\n", encoding="utf-8")

    print("Difference quotient convergence workflow complete.")
    print(f"Step sizes: {len(h_values)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
