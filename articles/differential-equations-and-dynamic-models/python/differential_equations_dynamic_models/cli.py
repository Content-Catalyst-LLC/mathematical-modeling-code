from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from differential_equations_dynamic_models.core import (
    build_dynamic_audit_card,
    dynamic_risk_score,
    load_dynamic_scenarios,
    load_model_records,
    simulate_euler,
    summarize_trajectory,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the differential equations and dynamic models workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/dynamic_model_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/dynamic_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    model_records = load_model_records(args.register_file)
    scenarios = load_dynamic_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_euler(scenario)
        all_rows.extend(rows)
        summary = summarize_trajectory(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    register_rows = [
        {
            **asdict(item),
            "dynamic_risk_score": dynamic_risk_score(item),
        }
        for item in model_records
    ]

    write_csv(tables_dir / "dynamic_model_timeseries.csv", all_rows)
    write_csv(tables_dir / "dynamic_model_summary.csv", summary_rows)
    write_csv(tables_dir / "dynamic_model_register.csv", register_rows)
    write_json(json_dir / "dynamic_model_audit_card.json", build_dynamic_audit_card(model_records, summary_rows))

    print("Differential equations and dynamic models workflow complete.")
    print(f"Dynamic records: {len(model_records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
