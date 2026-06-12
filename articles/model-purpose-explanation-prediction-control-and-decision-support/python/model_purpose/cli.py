from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from model_purpose.core import (
    build_model_purpose_card,
    load_purpose_records,
    load_scenarios,
    purpose_risk_score,
    simulate_resource,
    summarize_resource,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the model-purpose companion workflow.")
    parser.add_argument("--purpose-file", type=Path, default=Path("data/purpose_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/purpose_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    purpose_records = load_purpose_records(args.purpose_file)
    scenarios = load_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_resource(scenario)
        all_rows.extend(rows)
        summary = summarize_resource(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    purpose_rows = [
        {
            **asdict(item),
            "purpose_risk_score": purpose_risk_score(item),
        }
        for item in purpose_records
    ]

    write_csv(tables_dir / "purpose_scenario_timeseries.csv", all_rows)
    write_csv(tables_dir / "purpose_scenario_summary.csv", summary_rows)
    write_csv(tables_dir / "purpose_register.csv", purpose_rows)
    write_json(json_dir / "model_purpose_card.json", build_model_purpose_card(purpose_records, summary_rows))

    print("Model purpose workflow complete.")
    print(f"Purpose records: {len(purpose_records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
