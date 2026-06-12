from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from calibration_estimation_parameter_fitting.core import (
    ParameterCandidate,
    build_calibration_audit_card,
    calibration_risk_score,
    candidate_grid,
    fit_model,
    load_grid,
    load_observations,
    load_records,
    simulate,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run calibration, estimation, and parameter fitting workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/calibration_register.csv"))
    parser.add_argument("--observations-file", type=Path, default=Path("data/calibration_observations.csv"))
    parser.add_argument("--grid-file", type=Path, default=Path("data/parameter_grid.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"

    records = load_records(args.register_file)
    observations = load_observations(args.observations_file)
    grid_config = load_grid(args.grid_file)
    candidates = candidate_grid(grid_config)

    best, scored = fit_model(observations, candidates)

    best_candidate = ParameterCandidate(
        growth_rate=float(best["growth_rate"]),
        carrying_capacity=float(best["carrying_capacity"]),
    )

    fitted_rows = simulate(best_candidate, observations)

    register_rows = [
        {**asdict(record), "calibration_risk_score": calibration_risk_score(record)}
        for record in records
    ]

    write_csv(tables_dir / "calibration_observations.csv", [asdict(obs) for obs in observations])
    write_csv(tables_dir / "parameter_candidate_scores.csv", scored)
    write_csv(tables_dir / "fitted_model_residuals.csv", fitted_rows)
    write_csv(tables_dir / "calibration_register.csv", register_rows)
    write_json(json_dir / "calibration_audit_card.json", build_calibration_audit_card(records, best, fitted_rows))

    print("Calibration workflow complete.")
    print(f"Best fit: {best}")
    print(f"Candidate count: {len(scored)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
