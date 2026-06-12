from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from what_is_mathematical_modeling.core import (
    build_model_card,
    calibrate_grid_search,
    load_scenarios,
    monte_carlo_uncertainty,
    read_observations,
    residual_diagnostics,
    residuals_against_observations,
    run_scenarios,
    sensitivity_oat,
    simulate_rk4,
    summarize_results,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the What Is Mathematical Modeling companion workflow.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/scenario_definitions.csv"))
    parser.add_argument("--observation-file", type=Path, default=Path("data/synthetic_observations.csv"))
    parser.add_argument("--monte-carlo-runs", type=int, default=300)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    scenarios = load_scenarios(args.scenario_file)
    if not scenarios:
        raise ValueError("No scenarios loaded.")

    base = scenarios[0]
    results = run_scenarios(scenarios)
    timeseries = [row for result in results for row in result.rows]
    summary = summarize_results(results)

    write_csv(tables_dir / "scenario_timeseries.csv", timeseries)
    write_csv(tables_dir / "scenario_summary.csv", summary)

    if args.observation_file.exists():
        observations = read_observations(args.observation_file)
        baseline_result = simulate_rk4(base)
        residual_rows = residuals_against_observations(baseline_result, observations)
        write_csv(tables_dir / "residuals.csv", residual_rows)
        write_json(json_dir / "residual_diagnostics.json", residual_diagnostics(residual_rows))

        growth_rates = [0.25, 0.30, 0.35, 0.40, 0.45]
        capacities = [85.0, 95.0, 100.0, 105.0, 115.0]
        calibration = calibrate_grid_search(base, observations, growth_rates, capacities)
        write_csv(tables_dir / "calibration_grid_search.csv", calibration)

    write_csv(tables_dir / "sensitivity_oat.csv", sensitivity_oat(base))
    write_csv(tables_dir / "monte_carlo_uncertainty.csv", monte_carlo_uncertainty(base, n=args.monte_carlo_runs))
    write_json(json_dir / "model_card.json", build_model_card(base, scenarios))

    print("Workflow complete.")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Wrote outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()
