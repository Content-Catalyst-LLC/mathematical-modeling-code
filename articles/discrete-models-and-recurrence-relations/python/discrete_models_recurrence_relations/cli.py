from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from discrete_models_recurrence_relations.core import (
    build_recurrence_audit_card,
    load_recurrence_records,
    load_recurrence_scenarios,
    recurrence_risk_score,
    simulate_recurrence,
    summarize_trajectory,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the discrete models and recurrence relations workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/recurrence_model_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/recurrence_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    recurrence_records = load_recurrence_records(args.register_file)
    scenarios = load_recurrence_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_recurrence(scenario)
        all_rows.extend(rows)
        summary = summarize_trajectory(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    register_rows = [
        {
            **asdict(item),
            "recurrence_risk_score": recurrence_risk_score(item),
        }
        for item in recurrence_records
    ]

    write_csv(tables_dir / "recurrence_timeseries.csv", all_rows)
    write_csv(tables_dir / "recurrence_summary.csv", summary_rows)
    write_csv(tables_dir / "recurrence_model_register.csv", register_rows)
    write_json(json_dir / "recurrence_model_audit_card.json", build_recurrence_audit_card(recurrence_records, summary_rows))

    print("Discrete models and recurrence relations workflow complete.")
    print(f"Recurrence records: {len(recurrence_records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
