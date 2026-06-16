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

def euler_step(t: float, y: float, h: float, decay_rate: float) -> float:
    return y + h * rate(t, y, decay_rate)

def midpoint_step(t: float, y: float, h: float, decay_rate: float) -> float:
    k1 = rate(t, y, decay_rate)
    k2 = rate(t + h / 2, y + h * k1 / 2, decay_rate)
    return y + h * k2

def heun_step(t: float, y: float, h: float, decay_rate: float) -> float:
    k1 = rate(t, y, decay_rate)
    k2 = rate(t + h, y + h * k1, decay_rate)
    return y + h * 0.5 * (k1 + k2)

def stage_values(t: float, y: float, h: float, decay_rate: float) -> dict:
    k1 = rate(t, y, decay_rate)
    k2 = rate(t + h / 2, y + h * k1 / 2, decay_rate)
    k3 = rate(t + h / 2, y + h * k2 / 2, decay_rate)
    k4 = rate(t + h, y + h * k3, decay_rate)
    return {"k1": k1, "k2": k2, "k3": k3, "k4": k4}

def rk4_step(t: float, y: float, h: float, decay_rate: float) -> float:
    stages = stage_values(t, y, h, decay_rate)
    return y + (h / 6.0) * (stages["k1"] + 2 * stages["k2"] + 2 * stages["k3"] + stages["k4"])

def audit_rows(y0: float, decay_rate: float, h: float, stop_time: float) -> list[dict]:
    steps = int(round(stop_time / h))
    y_euler = y0
    y_rk4 = y0
    rows = []
    for step in range(steps + 1):
        t = step * h
        exact_value = exact(t, y0, decay_rate)
        rows.append({
            "step": step,
            "time": t,
            "euler_value": y_euler,
            "rk4_value": y_rk4,
            "exact_value": exact_value,
            "euler_absolute_error": abs(y_euler - exact_value),
            "rk4_absolute_error": abs(y_rk4 - exact_value),
            "step_size": h
        })
        y_euler = euler_step(t, y_euler, h, decay_rate)
        y_rk4 = rk4_step(t, y_rk4, h, decay_rate)
    return rows

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ["rk4-step", "midpoint-step", "heun-step", "stage-values"]:
        p = sub.add_parser(command)
        p.add_argument("--t", type=float, default=0.0)
        p.add_argument("--y", type=float, default=100.0)
        p.add_argument("--h", type=float, default=0.5)
        p.add_argument("--decay-rate", type=float, default=0.35)
    p = sub.add_parser("euler-vs-rk4-audit")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--decay-rate", type=float, default=0.35)
    p.add_argument("--h", type=float, default=0.5)
    p.add_argument("--stop-time", type=float, default=20.0)
    p = sub.add_parser("step-size-comparison")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--decay-rate", type=float, default=0.35)
    p.add_argument("--stop-time", type=float, default=20.0)
    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "rk4-step":
        updated = rk4_step(args.t, args.y, args.h, args.decay_rate)
        emit(cmd, args, {"updated_value": updated}, "Computes one classical RK4 update.", "RK4 still depends on rate function, step size, smoothness, and stiffness.")
    elif cmd == "midpoint-step":
        updated = midpoint_step(args.t, args.y, args.h, args.decay_rate)
        emit(cmd, args, {"updated_value": updated}, "Computes one midpoint Runge-Kutta update.", "Midpoint methods sample one interior slope but still require step-size review.")
    elif cmd == "heun-step":
        updated = heun_step(args.t, args.y, args.h, args.decay_rate)
        emit(cmd, args, {"updated_value": updated}, "Computes one Heun-style RK2 update.", "Heun's method averages beginning and predicted endpoint slopes.")
    elif cmd == "stage-values":
        stages = stage_values(args.t, args.y, args.h, args.decay_rate)
        emit(cmd, args, stages, "Returns RK4 stage slopes.", "Wrong stage formulas silently change the method.")
    elif cmd == "euler-vs-rk4-audit":
        rows = audit_rows(args.y0, args.decay_rate, args.h, args.stop_time)
        write_series("euler_vs_rk4_audit", rows)
        emit(cmd, args, {"records": len(rows), "final_euler_error": rows[-1]["euler_absolute_error"], "final_rk4_error": rows[-1]["rk4_absolute_error"]}, "Compares Euler and RK4 against an exact decay solution.", "Synthetic benchmarks do not guarantee empirical model validity.")
    elif cmd == "step-size-comparison":
        comparison = []
        for h in [1.0, 0.5, 0.25, 0.1]:
            rows = audit_rows(args.y0, args.decay_rate, h, args.stop_time)
            comparison.append({"step_size": h, "records": len(rows), "final_euler_error": rows[-1]["euler_absolute_error"], "final_rk4_error": rows[-1]["rk4_absolute_error"]})
        write_series("step_size_comparison", comparison)
        emit(cmd, args, {"tested_step_sizes": 4, "smallest_step_rk4_error": comparison[-1]["final_rk4_error"]}, "Compares RK4 results across step sizes.", "Step-size sensitivity should be reviewed before interpretation.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
