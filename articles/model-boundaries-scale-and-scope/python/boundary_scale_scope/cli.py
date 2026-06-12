from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from boundary_scale_scope.core import (
    boundary_risk_score,
    build_boundary_card,
    load_boundaries,
    load_scenarios,
    simulate_resource,
    summarize_resource,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the boundary, scale, and scope companion workflow.")
    parser.add_argument("--boundary-file", type=Path, default=Path("data/boundary_register.csv"))
    parser.add_argument("--scenario-file", type=Path, default=Path("data/boundary_scenarios.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    boundaries = load_boundaries(args.boundary_file)
    scenarios = load_scenarios(args.scenario_file)

    all_rows = []
    summary_rows = []

    for scenario in scenarios:
        rows = simulate_resource(scenario)
        all_rows.extend(rows)
        summary = summarize_resource(rows)
        summary["description"] = scenario.description
        summary_rows.append(summary)

    boundary_rows = [
        {
            **asdict(item),
            "boundary_risk_score": boundary_risk_score(item),
        }
        for item in boundaries
    ]

    write_csv(tables_dir / "boundary_scenario_timeseries.csv", all_rows)
    write_csv(tables_dir / "boundary_scenario_summary.csv", summary_rows)
    write_csv(tables_dir / "boundary_register.csv", boundary_rows)
    write_json(json_dir / "boundary_scale_scope_card.json", build_boundary_card(boundaries, summary_rows))

    print("Boundary, scale, and scope workflow complete.")
    print(f"Boundary choices: {len(boundaries)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
