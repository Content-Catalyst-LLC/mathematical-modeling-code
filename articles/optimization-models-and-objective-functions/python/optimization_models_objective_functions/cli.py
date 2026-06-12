from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from optimization_models_objective_functions.core import (
    build_optimization_audit_card,
    best_feasible,
    enumerate_choices,
    load_optimization_records,
    load_programs,
    load_scenarios,
    optimization_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the optimization models and objective functions workflow.")
    parser.add_argument("--program-file", type=Path, default=Path("data/programs.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/optimization_scenarios.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/optimization_model_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    program_list = load_programs(args.program_file)
    scenarios = load_scenarios(args.scenario_file)
    optimization_records = load_optimization_records(args.register_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = enumerate_choices(program_list, scenario)
        all_rows.extend(rows)
        best = best_feasible(rows)
        summary = {
            "scenario": scenario.name,
            "description": scenario.description,
            "candidate_choices": len(rows),
            "feasible_choices": sum(1 for row in rows if bool(row["feasible"])),
            **best,
        }
        summary_rows.append(summary)

    register_rows = [
        {
            **asdict(item),
            "optimization_risk_score": optimization_risk_score(item),
        }
        for item in optimization_records
    ]

    write_csv(tables_dir / "optimization_feasible_choice_audit.csv", all_rows)
    write_csv(tables_dir / "optimization_solution_summary.csv", summary_rows)
    write_csv(tables_dir / "optimization_model_register.csv", register_rows)
    write_json(json_dir / "optimization_model_audit_card.json", build_optimization_audit_card(optimization_records, summary_rows))

    print("Optimization models and objective functions workflow complete.")
    print(f"Optimization records: {len(optimization_records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
