from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from agent_based_models_emergent_behavior.core import (
    build_abm_audit_card,
    load_records,
    load_scenarios,
    rule_risk_score,
    run_replication,
    summarize_runs,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the ABM adoption and emergence workflow.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/abm_scenarios.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/abm_model_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    scenarios = load_scenarios(args.scenario_file)
    records = load_records(args.register_file)

    all_rows = []
    for scenario in scenarios:
        for seed in range(1, scenario.replications + 1):
            all_rows.extend(run_replication(scenario, seed))

    summary_rows = summarize_runs(all_rows)

    register_rows = [
        {
            **asdict(item),
            "rule_risk_score": rule_risk_score(item),
        }
        for item in records
    ]

    write_csv(tables_dir / "abm_adoption_trajectories.csv", all_rows)
    write_csv(tables_dir / "abm_ensemble_summary.csv", summary_rows)
    write_csv(tables_dir / "abm_model_register.csv", register_rows)
    write_json(json_dir / "abm_audit_card.json", build_abm_audit_card(records, scenarios, summary_rows))

    print("Agent-based models and emergent behavior workflow complete.")
    print(f"ABM records: {len(records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
