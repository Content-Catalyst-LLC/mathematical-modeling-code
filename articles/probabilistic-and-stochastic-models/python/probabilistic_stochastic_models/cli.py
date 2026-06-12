from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from probabilistic_stochastic_models.core import (
    build_probability_audit_card,
    load_probability_records,
    load_risk_scenarios,
    probability_risk_score,
    simulate_risk,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the probabilistic and stochastic models workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/probability_model_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/risk_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    probability_records = load_probability_records(args.register_file)
    scenarios = load_risk_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows, summary = simulate_risk(scenario)
        all_rows.extend(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    register_rows = [
        {
            **asdict(item),
            "probability_risk_score": probability_risk_score(item),
        }
        for item in probability_records
    ]

    write_csv(tables_dir / "probabilistic_simulation_runs.csv", all_rows)
    write_csv(tables_dir / "probabilistic_risk_summary.csv", summary_rows)
    write_csv(tables_dir / "probability_model_register.csv", register_rows)
    write_json(json_dir / "probabilistic_model_audit_card.json", build_probability_audit_card(probability_records, summary_rows))

    print("Probabilistic and stochastic models workflow complete.")
    print(f"Probability records: {len(probability_records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
