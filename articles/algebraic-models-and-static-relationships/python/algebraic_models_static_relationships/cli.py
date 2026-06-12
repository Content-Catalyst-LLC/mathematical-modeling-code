from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from algebraic_models_static_relationships.core import (
    build_algebraic_audit_card,
    evaluate_scenario,
    load_relationships,
    load_scenarios,
    relationship_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the algebraic models and static relationships workflow.")
    parser.add_argument("--relationship-file", type=Path, default=Path("data/algebraic_relationship_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/static_allocation_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    relationships = load_relationships(args.relationship_file)
    scenarios = load_scenarios(args.scenario_file)

    relationship_rows = [
        {
            **asdict(item),
            "relationship_risk_score": relationship_risk_score(item),
        }
        for item in relationships
    ]

    scenario_rows = [evaluate_scenario(scenario) for scenario in scenarios]

    write_csv(tables_dir / "algebraic_relationship_register.csv", relationship_rows)
    write_csv(tables_dir / "static_allocation_scenarios.csv", scenario_rows)
    write_json(json_dir / "algebraic_model_audit_card.json", build_algebraic_audit_card(relationships, scenario_rows))

    print("Algebraic models and static relationships workflow complete.")
    print(f"Relationships: {len(relationships)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
