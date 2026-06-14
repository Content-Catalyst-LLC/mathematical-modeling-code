from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from functions_variables_mathematical_representation.core import (
    build_manifest,
    evaluate_models,
    load_x_values,
    summarize_results,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run functional representation workflow.")
    parser.add_argument("--x-file", type=Path, default=Path("data/input_values.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    x_values = load_x_values(args.x_file)
    rows = evaluate_models(x_values)
    summary = summarize_results(rows)

    results_path = args.output_dir / "tables" / "functional_model_results.csv"
    summary_path = args.output_dir / "tables" / "functional_model_summary.csv"
    manifest_path = args.output_dir / "json" / "functional_model_manifest.json"
    log_path = args.output_dir / "logs" / "python_workflow.log"

    write_csv(results_path, rows)
    write_csv(summary_path, summary)
    write_json(manifest_path, build_manifest(summary))

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Functional representation workflow completed.\n", encoding="utf-8")

    print("Functional representation workflow complete.")
    print(f"Input values: {len(x_values)}")
    print(f"Rows: {len(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
