from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from numerical_methods_for_mathematical_models.core import (
    build_numerical_audit_card,
    convergence_summary,
    load_records,
    load_scenarios,
    numerical_risk_score,
    run_euler,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run numerical method diagnostics.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/solver_scenarios.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/numerical_method_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    scenarios = load_scenarios(args.scenario_file)
    records = load_records(args.register_file)

    trajectories: list[dict[str, object]] = []
    for scenario in scenarios:
        trajectories.extend(run_euler(scenario))

    convergence = convergence_summary(trajectories)

    register_rows = [
        {**asdict(record), "numerical_risk_score": numerical_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "numerical_method_register.csv", register_rows)
    write_csv(tables_dir / "euler_resource_trajectories.csv", trajectories)
    write_csv(tables_dir / "step_size_convergence_summary.csv", convergence)
    write_json(json_dir / "numerical_method_audit_card.json", build_numerical_audit_card(records, scenarios, convergence))

    print("Numerical methods workflow complete.")
    print(f"Numerical records: {len(records)}")
    print(f"Solver scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
