from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from abstraction_representation.core import (
    build_representation_card,
    load_representation_choices,
    load_scenarios,
    representation_risk_score,
    simulate_stock_flow,
    summarize_stock_flow,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the abstraction and representation companion workflow.")
    parser.add_argument("--choices-file", type=Path, default=Path("data/representation_choices.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/stock_flow_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    choices = load_representation_choices(args.choices_file)
    scenarios = load_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_stock_flow(scenario)
        all_rows.extend(rows)
        summary = summarize_stock_flow(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    audit_rows = [
        {
            **asdict(choice),
            "representation_risk_score": representation_risk_score(choice),
        }
        for choice in choices
    ]

    write_csv(tables_dir / "stock_flow_timeseries.csv", all_rows)
    write_csv(tables_dir / "stock_flow_summary.csv", summary_rows)
    write_csv(tables_dir / "representation_audit.csv", audit_rows)
    write_json(json_dir / "representation_card.json", build_representation_card(choices, summary_rows))

    print("Abstraction and representation workflow complete.")
    print(f"Representation choices: {len(choices)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
