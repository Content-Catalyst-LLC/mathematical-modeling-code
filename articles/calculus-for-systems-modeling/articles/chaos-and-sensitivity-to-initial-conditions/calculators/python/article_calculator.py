#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

@dataclass
class CalculatorResult:
    calculator: str
    inputs: dict
    result: dict
    interpretation: str
    warning: str = ""

def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def write_outputs(name: str, payload: CalculatorResult) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(asdict(payload), indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload.calculator, "interpretation": payload.interpretation, "warning": payload.warning}
    flat.update({f"input_{k}": v for k, v in payload.inputs.items() if not isinstance(v, list)})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, (list, dict))})
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

def write_series(name: str, rows: list[dict]) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def logistic_map(x: float, r: float) -> float:
    return r * x * (1.0 - x)

def logistic_derivative(x: float, r: float) -> float:
    return r * (1.0 - 2.0 * x)

def estimate_lyapunov(x0: float, r: float, burn_in: int, sample_steps: int) -> float:
    x = x0
    for _ in range(burn_in):
        x = logistic_map(x, r)
    values = []
    for _ in range(sample_steps):
        d = abs(logistic_derivative(x, r))
        if d > 0:
            values.append(math.log(d))
        x = logistic_map(x, r)
    return sum(values) / len(values)

def forecast_horizon(initial_uncertainty: float, acceptable_error: float, lyapunov_value: float) -> float | None:
    if initial_uncertainty <= 0 or acceptable_error <= 0 or lyapunov_value <= 0:
        return None
    return math.log(acceptable_error / initial_uncertainty) / lyapunov_value

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("logistic-next")
    p.add_argument("--x", type=float, default=0.2)
    p.add_argument("--r", type=float, default=3.9)

    p = sub.add_parser("trajectory-divergence")
    p.add_argument("--x0", type=float, default=0.2)
    p.add_argument("--perturbation", type=float, default=1e-8)
    p.add_argument("--r", type=float, default=3.9)
    p.add_argument("--steps", type=int, default=30)

    p = sub.add_parser("lyapunov-estimate")
    p.add_argument("--x0", type=float, default=0.2)
    p.add_argument("--r", type=float, default=3.9)
    p.add_argument("--burn-in", type=int, default=100)
    p.add_argument("--sample-steps", type=int, default=1000)

    p = sub.add_parser("forecast-horizon")
    p.add_argument("--initial-uncertainty", type=float, default=1e-8)
    p.add_argument("--acceptable-error", type=float, default=1e-2)
    p.add_argument("--lyapunov", type=float, default=0.5)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-next":
        emit(cmd, args, {"next_state": logistic_map(args.x, args.r)}, "Computes one logistic-map update.", "The logistic map is an illustrative nonlinear model.")
    elif cmd == "trajectory-divergence":
        rows = []
        x_ref = args.x0
        x_per = args.x0 + args.perturbation
        for step in range(args.steps + 1):
            difference = abs(x_ref - x_per)
            rows.append({"step": step, "x_reference": x_ref, "x_perturbed": x_per, "absolute_difference": difference})
            x_ref = logistic_map(x_ref, args.r)
            x_per = logistic_map(x_per, args.r)
        write_series("trajectory_divergence", rows)
        emit(cmd, args, {"records": len(rows), "final_difference": rows[-1]["absolute_difference"]}, "Compares two nearby initial conditions.", "Divergence depends on parameter value, perturbation size, and numerical precision.")
    elif cmd == "lyapunov-estimate":
        value = estimate_lyapunov(args.x0, args.r, args.burn_in, args.sample_steps)
        emit(cmd, args, {"lyapunov_estimate": value}, "Estimates average local trajectory divergence.", "Lyapunov estimates depend on burn-in, sample length, and precision.")
    elif cmd == "forecast-horizon":
        horizon = forecast_horizon(args.initial_uncertainty, args.acceptable_error, args.lyapunov)
        emit(cmd, args, {"forecast_horizon": horizon}, "Estimates a rough forecast horizon from uncertainty growth.", "Forecast horizons depend on acceptable error and the validity of the divergence estimate.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
