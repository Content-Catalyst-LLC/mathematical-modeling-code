from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from equations_inequalities_model_logic.core import (
    build_logic_audit_card,
    load_scenarios,
    load_statements,
    simulate_logic,
    statement_risk_score,
    summarize_logic,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the equations, inequalities, and model logic workflow.")
    parser.add_argument("--statement-file", type=Path, default=Path("data/formal_statement_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/logic_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    statements = load_statements(args.statement_file)
    scenarios = load_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_logic(scenario)
        all_rows.extend(rows)
        summary = summarize_logic(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    statement_rows = [
        {
            **asdict(item),
            "statement_risk_score": statement_risk_score(item),
        }
        for item in statements
    ]

    write_csv(tables_dir / "logic_scenario_timeseries.csv", all_rows)
    write_csv(tables_dir / "logic_scenario_summary.csv", summary_rows)
    write_csv(tables_dir / "formal_statement_register.csv", statement_rows)
    write_json(json_dir / "equation_inequality_logic_audit_card.json", build_logic_audit_card(statements, summary_rows))

    print("Equations, inequalities, and model logic workflow complete.")
    print(f"Formal statements: {len(statements)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
