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

def rate(t: float, y: float, decay_rate: float) -> float:
    return -decay_rate * y

def exact(t: float, y0: float, decay_rate: float) -> float:
    return y0 * math.exp(-decay_rate * t)

def rk4_step(t: float, y: float, h: float, decay_rate: float) -> float:
    k1 = rate(t, y, decay_rate)
    k2 = rate(t + h / 2, y + h * k1 / 2, decay_rate)
    k3 = rate(t + h / 2, y + h * k2 / 2, decay_rate)
    k4 = rate(t + h, y + h * k3, decay_rate)
    return y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def solver_rows(y0: float, decay_rate: float, h: float, stop_time: float) -> list[dict]:
    steps = int(round(stop_time / h))
    y = y0
    rows = []
    for step in range(steps + 1):
        t = step * h
        exact_value = exact(t, y0, decay_rate)
        rows.append({
            "step": step,
            "time": t,
            "solver_value": y,
            "exact_value": exact_value,
            "absolute_error": abs(y - exact_value),
            "solver_method": "fixed_step_rk4",
            "step_size": h
        })
        y = rk4_step(t, y, h, decay_rate)
    return rows

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("rk4-solver-step")
    p.add_argument("--t", type=float, default=0.0)
    p.add_argument("--y", type=float, default=100.0)
    p.add_argument("--h", type=float, default=0.5)
    p.add_argument("--decay-rate", type=float, default=0.35)

    p = sub.add_parser("solver-benchmark")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--decay-rate", type=float, default=0.35)
    p.add_argument("--h", type=float, default=0.5)
    p.add_argument("--stop-time", type=float, default=20.0)

    p = sub.add_parser("step-size-comparison")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--decay-rate", type=float, default=0.35)
    p.add_argument("--stop-time", type=float, default=20.0)

    p = sub.add_parser("tolerance-threshold")
    p.add_argument("--atol", type=float, default=1e-8)
    p.add_argument("--rtol", type=float, default=1e-6)
    p.add_argument("--state", type=float, default=100.0)

    p = sub.add_parser("stiffness-indicator")
    p.add_argument("--fast-rate", type=float, default=100.0)
    p.add_argument("--slow-rate", type=float, default=1.0)

    p = sub.add_parser("solver-config-record")
    p.add_argument("--method", default="fixed_step_rk4")
    p.add_argument("--h", type=float, default=0.5)
    p.add_argument("--atol", type=float, default=1e-8)
    p.add_argument("--rtol", type=float, default=1e-6)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "rk4-solver-step":
        updated = rk4_step(args.t, args.y, args.h, args.decay_rate)
        emit(cmd, args, {"updated_value": updated}, "Computes one fixed-step RK4 solver update.", "Solver output depends on equation, initial condition, method, step size, stiffness, and diagnostics.")
    elif cmd == "solver-benchmark":
        rows = solver_rows(args.y0, args.decay_rate, args.h, args.stop_time)
        write_series("solver_benchmark", rows)
        emit(cmd, args, {"records": len(rows), "final_solver_value": rows[-1]["solver_value"], "final_exact_value": rows[-1]["exact_value"], "final_absolute_error": rows[-1]["absolute_error"]}, "Benchmarks a fixed-step RK4 solver against an exact decay solution.", "Benchmarks test numerical behavior but do not validate empirical assumptions.")
    elif cmd == "step-size-comparison":
        comparison = []
        for h in [1.0, 0.5, 0.25, 0.1]:
            rows = solver_rows(args.y0, args.decay_rate, h, args.stop_time)
            comparison.append({"step_size": h, "records": len(rows), "final_solver_value": rows[-1]["solver_value"], "final_exact_value": rows[-1]["exact_value"], "final_absolute_error": rows[-1]["absolute_error"]})
        write_series("step_size_comparison", comparison)
        emit(cmd, args, {"tested_step_sizes": 4, "smallest_step_final_error": comparison[-1]["final_absolute_error"]}, "Compares solver output across step sizes.", "Step-size sensitivity should be reviewed before interpretation.")
    elif cmd == "tolerance-threshold":
        threshold = args.atol + args.rtol * abs(args.state)
        emit(cmd, args, {"tolerance_threshold": threshold}, "Computes an absolute-plus-relative tolerance threshold.", "Tolerance settings are numerical controls, not empirical uncertainty estimates.")
    elif cmd == "stiffness-indicator":
        ratio = abs(args.fast_rate / args.slow_rate)
        level = "possible_stiffness_review_needed" if ratio >= 100 else "mild_or_moderate_scale_separation"
        emit(cmd, args, {"rate_scale_ratio": ratio, "review_status": level}, "Computes a simple rate-scale ratio as a stiffness review prompt.", "This is a screening heuristic, not a formal stiffness proof.")
    elif cmd == "solver-config-record":
        emit(cmd, args, {"solver_method": args.method, "step_size": args.h, "absolute_tolerance": args.atol, "relative_tolerance": args.rtol}, "Creates a solver configuration record.", "Solver settings should be preserved with outputs.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
