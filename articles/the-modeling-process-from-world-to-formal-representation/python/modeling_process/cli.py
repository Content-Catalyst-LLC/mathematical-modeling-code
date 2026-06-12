from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from modeling_process.core import (
    ModelingQuestion,
    build_modeling_process_card,
    compare_to_observations,
    load_assumptions,
    load_observations,
    load_scenarios,
    residual_summary,
    scenario_stress_index,
    simulate_reservoir,
    summarize_scenario,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the modeling process companion workflow.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/scenario_definitions.csv"))
    parser.add_argument("--assumption-file", type=Path, default=Path("data/assumption_register.csv"))
    parser.add_argument("--observed-file", type=Path, default=Path("data/observed_storage.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    question = ModelingQuestion(
        article_slug="the-modeling-process-from-world-to-formal-representation",
        real_world_context="Reservoir storage under changing inflow, demand, losses, and capacity limits.",
        modeling_purpose="Demonstrate how a real-world question becomes a formal mathematical model.",
        central_question="How does storage evolve under different inflow, demand, loss, and capacity assumptions?",
        intended_use="Educational modeling-process demonstration and reproducible companion workflow.",
        decision_context="Scenario comparison, sensitivity awareness, validation planning, and model revision.",
    )

    scenarios = load_scenarios(args.scenario_file)
    assumptions = load_assumptions(args.assumption_file)

    all_rows = []
    summary_rows = []
    residual_rows = []

    observations = load_observations(args.observed_file) if args.observed_file.exists() else []

    for scenario in scenarios:
        rows = simulate_reservoir(scenario)
        all_rows.extend(rows)
        summary = summarize_scenario(rows)
        summary["stress_index"] = scenario_stress_index(summary)
        summary["description"] = scenario.description
        summary_rows.append(summary)

        if observations and scenario.name == "baseline":
            residual_rows.extend(compare_to_observations(rows, observations))

    write_csv(tables_dir / "reservoir_scenario_timeseries.csv", all_rows)
    write_csv(tables_dir / "reservoir_scenario_summary.csv", summary_rows)
    write_csv(tables_dir / "assumption_log.csv", [asdict(item) for item in assumptions])

    if residual_rows:
        write_csv(tables_dir / "baseline_residuals.csv", residual_rows)
        write_json(json_dir / "baseline_residual_summary.json", residual_summary(residual_rows))

    write_json(json_dir / "modeling_question.json", asdict(question))
    write_json(json_dir / "modeling_process_card.json", build_modeling_process_card(question, assumptions, summary_rows))

    print("Modeling process workflow complete.")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Assumptions: {len(assumptions)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
