from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from monte_carlo_uncertainty_propagation.core import (
    build_monte_carlo_audit_card,
    convergence_rows,
    load_records,
    load_scenarios,
    monte_carlo_risk_score,
    run_monte_carlo,
    simple_sensitivity_rows,
    summarize,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Monte Carlo uncertainty propagation workflow.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/monte_carlo_scenarios.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/monte_carlo_model_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    scenarios = load_scenarios(args.scenario_file)
    records = load_records(args.register_file)

    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        rows.extend(run_monte_carlo(scenario))

    summary = summarize(rows)
    convergence = convergence_rows(rows, checkpoints=[50, 100, 250, 500, 1000])
    sensitivity = simple_sensitivity_rows(rows)

    register_rows = [
        {**asdict(record), "monte_carlo_risk_score": monte_carlo_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "monte_carlo_model_register.csv", register_rows)
    write_csv(tables_dir / "monte_carlo_replications.csv", rows)
    write_csv(tables_dir / "monte_carlo_output_summary.csv", summary)
    write_csv(tables_dir / "monte_carlo_convergence_diagnostics.csv", convergence)
    write_csv(tables_dir / "monte_carlo_sensitivity_screen.csv", sensitivity)
    write_json(json_dir / "monte_carlo_audit_card.json", build_monte_carlo_audit_card(records, scenarios, summary, convergence))

    print("Monte Carlo uncertainty propagation workflow complete.")
    print(f"Monte Carlo records: {len(records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Replications: {len(rows)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
