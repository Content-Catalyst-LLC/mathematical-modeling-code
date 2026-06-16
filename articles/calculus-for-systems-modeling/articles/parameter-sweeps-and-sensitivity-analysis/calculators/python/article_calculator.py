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

def logistic(t: float, x0: float, r: float, k: float) -> float:
    return k / (1 + ((k - x0) / x0) * math.exp(-r * t))

def final_output(r: float, k: float, x0: float = 10.0, stop_time: float = 20.0) -> float:
    return logistic(stop_time, x0, r, k)

def local_sensitivity(parameter: str) -> tuple[float, float, float, float]:
    baseline_r, baseline_k = 0.35, 100.0
    h = 0.01 if parameter == "growth_rate" else 1.0
    baseline = final_output(baseline_r, baseline_k)
    if parameter == "growth_rate":
        forward = final_output(baseline_r + h, baseline_k)
        backward = final_output(baseline_r - h, baseline_k)
        baseline_value = baseline_r
    elif parameter == "carrying_capacity":
        forward = final_output(baseline_r, baseline_k + h)
        backward = final_output(baseline_r, baseline_k - h)
        baseline_value = baseline_k
    else:
        raise ValueError("parameter must be growth_rate or carrying_capacity")
    sensitivity = (forward - backward) / (2 * h)
    elasticity = sensitivity * baseline_value / baseline
    return baseline_value, sensitivity, elasticity, baseline

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("logistic-final")
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--carrying-capacity", type=float, default=100.0)
    p.add_argument("--initial-value", type=float, default=10.0)
    p.add_argument("--stop-time", type=float, default=20.0)

    p = sub.add_parser("local-sensitivity")
    p.add_argument("--parameter", choices=["growth_rate", "carrying_capacity"], default="growth_rate")

    p = sub.add_parser("elasticity")
    p.add_argument("--parameter", choices=["growth_rate", "carrying_capacity"], default="growth_rate")

    sub.add_parser("grid-sweep")

    p = sub.add_parser("robustness-range")
    p.add_argument("--low", type=float, default=80.0)
    p.add_argument("--high", type=float, default=100.0)

    p = sub.add_parser("fragility-note")
    p.add_argument("--pattern", default="threshold")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-final":
        value = logistic(args.stop_time, args.initial_value, args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"final_value": value}, "Computes final logistic-model output for one parameter set.", "A single parameter set does not show robustness.")
    elif cmd == "local-sensitivity":
        baseline_value, sensitivity, elasticity, baseline = local_sensitivity(args.parameter)
        emit(cmd, args, {"baseline_value": baseline_value, "baseline_output": baseline, "finite_difference_sensitivity": sensitivity, "elasticity_estimate": elasticity}, "Computes local finite-difference sensitivity.", "Local sensitivity depends on baseline and perturbation size.")
    elif cmd == "elasticity":
        baseline_value, sensitivity, elasticity, baseline = local_sensitivity(args.parameter)
        emit(cmd, args, {"baseline_value": baseline_value, "baseline_output": baseline, "elasticity_estimate": elasticity, "raw_sensitivity": sensitivity}, "Computes an elasticity-style sensitivity estimate.", "Elasticity helps compare units but remains local.")
    elif cmd == "grid-sweep":
        rows = []
        for r in [0.18, 0.25, 0.35, 0.45, 0.55]:
            for k in [80.0, 100.0, 125.0, 150.0]:
                rows.append({"growth_rate": r, "carrying_capacity": k, "final_value": final_output(r, k)})
        write_series("grid_sweep", rows)
        emit(cmd, args, {"records": len(rows), "min_final_value": min(row["final_value"] for row in rows), "max_final_value": max(row["final_value"] for row in rows)}, "Generates a two-parameter grid sweep.", "Grid-sweep evidence only applies to tested ranges.")
    elif cmd == "robustness-range":
        span = args.high - args.low
        emit(cmd, args, {"range_width": span, "relative_width": span / ((args.high + args.low) / 2)}, "Summarizes a tested robustness range.", "Robustness only applies within the tested parameter range.")
    elif cmd == "fragility-note":
        notes = {
            "threshold": "Threshold-dependent conclusions require boundary mapping and uncertainty disclosure.",
            "interaction": "Interaction-dependent conclusions need grid, global, or scenario ensemble review.",
            "solver": "Solver-dependent sensitivity should trigger numerical reliability diagnostics.",
            "dominant_parameter": "Dominant-parameter sensitivity should guide data collection and calibration review."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document fragility and narrow the claim.")}, "Creates a fragility interpretation note.", "Fragility is a warning for interpretation, not automatic model rejection.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
