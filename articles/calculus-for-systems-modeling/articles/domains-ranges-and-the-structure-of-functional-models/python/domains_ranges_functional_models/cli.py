from __future__ import annotations
import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from domains_ranges_functional_models.core import build_manifest, evaluate_scenarios, load_scenarios, summarize_validation, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Run domain and range validation workflow.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/domain_range_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    scenarios = load_scenarios(args.scenario_file)
    results = evaluate_scenarios(scenarios)
    summary = summarize_validation(results)

    write_csv(args.output_dir / "tables" / "domain_range_validation_results.csv", results)
    write_csv(args.output_dir / "tables" / "domain_range_validation_summary.csv", summary)
    write_json(args.output_dir / "json" / "domain_range_manifest.json", build_manifest(scenarios, results))

    log_path = args.output_dir / "logs" / "python_workflow.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Domain and range validation workflow completed.\n", encoding="utf-8")

    print("Domain and range validation workflow complete.")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
