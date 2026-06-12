from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from functional_relationships_structure.core import (
    build_structural_diagnostics_card,
    load_relationships,
    load_scenarios,
    simulate_structure,
    structure_risk_score,
    summarize_structure,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the functional relationships companion workflow.")
    parser.add_argument("--relationship-file", type=Path, default=Path("data/relationship_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/structure_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    relationships = load_relationships(args.relationship_file)
    scenarios = load_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_structure(scenario)
        all_rows.extend(rows)
        summary = summarize_structure(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    relationship_rows = [
        {
            **asdict(item),
            "structure_risk_score": structure_risk_score(item),
        }
        for item in relationships
    ]

    write_csv(tables_dir / "structure_scenario_timeseries.csv", all_rows)
    write_csv(tables_dir / "structure_scenario_summary.csv", summary_rows)
    write_csv(tables_dir / "relationship_register.csv", relationship_rows)
    write_json(json_dir / "structural_diagnostics_card.json", build_structural_diagnostics_card(relationships, summary_rows))

    print("Functional relationships workflow complete.")
    print(f"Relationships: {len(relationships)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
