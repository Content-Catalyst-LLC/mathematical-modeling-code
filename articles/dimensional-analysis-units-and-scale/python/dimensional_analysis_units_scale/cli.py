from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from dimensional_analysis_units_scale.core import (
    build_dimensional_audit_card,
    load_scale_scenarios,
    load_unit_records,
    simulate_scale_scenario,
    summarize_scale_scenario,
    unit_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the dimensional analysis, units, and scale workflow.")
    parser.add_argument("--unit-file", type=Path, default=Path("data/unit_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/scale_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    unit_records = load_unit_records(args.unit_file)
    scenarios = load_scale_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_scale_scenario(scenario)
        all_rows.extend(rows)
        summary = summarize_scale_scenario(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    unit_rows = [
        {
            **asdict(item),
            "unit_risk_score": unit_risk_score(item),
        }
        for item in unit_records
    ]

    write_csv(tables_dir / "unit_scale_timeseries.csv", all_rows)
    write_csv(tables_dir / "unit_scale_summary.csv", summary_rows)
    write_csv(tables_dir / "unit_register.csv", unit_rows)
    write_json(json_dir / "dimensional_audit_card.json", build_dimensional_audit_card(unit_records, summary_rows))

    print("Dimensional analysis, units, and scale workflow complete.")
    print(f"Unit records: {len(unit_records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
