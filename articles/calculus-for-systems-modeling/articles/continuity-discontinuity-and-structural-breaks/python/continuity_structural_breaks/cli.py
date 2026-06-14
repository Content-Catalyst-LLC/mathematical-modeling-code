from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from continuity_structural_breaks.core import (
    diagnose_breaks,
    piecewise_system,
    summarize_flags,
    to_dicts,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run continuity and structural-break diagnostics.")
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--step", type=float, default=0.25)
    parser.add_argument("--max-x", type=float, default=10.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    n = int(args.max_x / args.step)
    xs = [i * args.step for i in range(n + 1)]
    ys = [piecewise_system(x) for x in xs]
    rows = diagnose_breaks(xs, ys)
    summary = summarize_flags(rows)

    write_csv(args.output_dir / "tables" / "continuity_break_diagnostics.csv", to_dicts(rows))
    write_csv(args.output_dir / "tables" / "continuity_break_summary.csv", summary)

    manifest = {
        "article": "Continuity, Discontinuity, and Structural Breaks",
        "series": "Calculus for Systems Modeling",
        "advanced_standard": True,
        "methods": ["piecewise_model", "finite_difference_slope_checks", "jump_detection", "slope_break_detection"],
        "interpretive_warning": "Synthetic break diagnostics flag review candidates; they do not prove real-world structural breaks.",
    }
    write_json(args.output_dir / "json" / "continuity_break_manifest.json", manifest)

    log_path = args.output_dir / "logs" / "python_workflow.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Continuity break diagnostic workflow completed.\n", encoding="utf-8")

    print("Continuity and structural-break workflow complete.")
    print(f"Points: {len(xs)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
