from __future__ import annotations

import argparse
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from what_is_mathematical_modeling.core import (
    LogisticModel,
    calibrate_grid_search,
    model_card,
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
    parser.add_argument("--initial-state", type=float, default=10.0)
    parser.add_argument("--growth-rate", type=float, default=0.35)
    parser.add_argument("--carrying-capacity", type=float, default=100.0)
    parser.add_argument("--time-step", type=float, default=0.1)
    parser.add_argument("--steps", type=int, default=160)
    parser.add_argument("--monte-carlo-runs", type=int, default=300)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    tables_dir = output_dir / "tables"
    json_dir = output_dir / "json"

    base = LogisticModel(
        name="baseline",
        initial_state=args.initial_state,
        growth_rate=args.growth_rate,
        carrying_capacity=args.carrying_capacity,
        time_step=args.time_step,
        steps=args.steps,
    )

    results = run_scenarios(base)
    timeseries = [row for result in results for row in result.rows]
    summary = summarize_results(results)

    write_csv(tables_dir / "scenario_timeseries.csv", timeseries)
    write_csv(tables_dir / "scenario_summary.csv", summary)

    observation_path = Path("data") / "synthetic_observations.csv"
    if observation_path.exists():
        observations = read_observations(observation_path)
        baseline_result = simulate_rk4(base)
        residual_rows = residuals_against_observations(baseline_result, observations)
        write_csv(tables_dir / "residuals.csv", residual_rows)
        write_json(json_dir / "residual_diagnostics.json", residual_diagnostics(residual_rows))

        growth_rates = [0.25, 0.30, 0.35, 0.40, 0.45]
        capacities = [85.0, 95.0, 100.0, 105.0, 115.0]
        calibration = calibrate_grid_search(base, observations, growth_rates, capacities)
        write_csv(tables_dir / "calibration_grid_search.csv", calibration)

    sensitivity = sensitivity_oat(base)
    write_csv(tables_dir / "sensitivity_oat.csv", sensitivity)

    mc_rows = monte_carlo_uncertainty(base, n=args.monte_carlo_runs)
    write_csv(tables_dir / "monte_carlo_uncertainty.csv", mc_rows)

    write_json(json_dir / "model_card.json", model_card(base))

    print("Workflow complete.")
    print(f"Wrote outputs to: {output_dir}")


if __name__ == "__main__":
    main()
