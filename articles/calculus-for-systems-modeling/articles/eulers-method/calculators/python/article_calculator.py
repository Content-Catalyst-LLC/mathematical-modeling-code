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

def stability_multiplier(h: float, decay_rate: float) -> float:
    return 1.0 - h * decay_rate

def status_from_multiplier(multiplier: float) -> str:
    return "stable_for_simple_decay" if abs(multiplier) <= 1.0 else "unstable_risk"

def decay_rows(y0: float, decay_rate: float, h: float, stop_time: float) -> list[dict]:
    steps = int(round(stop_time / h))
    y = y0
    multiplier = stability_multiplier(h, decay_rate)
    status = status_from_multiplier(multiplier)
    rows = []
    for step in range(steps + 1):
        t = step * h
        exact_value = exact(t, y0, decay_rate)
        rows.append({
            "step": step,
            "time": t,
            "euler_value": y,
            "exact_value": exact_value,
            "absolute_error": abs(y - exact_value),
            "step_size": h,
            "stability_multiplier": multiplier,
            "stability_status": status
        })
        y = euler_step(t, y, h, decay_rate)
    return rows

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("euler-step")
    p.add_argument("--t", type=float, default=0.0)
    p.add_argument("--y", type=float, default=100.0)
    p.add_argument("--h", type=float, default=0.1)
    p.add_argument("--decay-rate", type=float, default=0.35)

    p = sub.add_parser("decay-audit")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--decay-rate", type=float, default=0.35)
    p.add_argument("--h", type=float, default=0.1)
    p.add_argument("--stop-time", type=float, default=20.0)

    p = sub.add_parser("step-size-comparison")
    p.add_argument("--y0", type=float, default=100.0)
    p.add_argument("--decay-rate", type=float, default=0.35)
    p.add_argument("--stop-time", type=float, default=20.0)

    p = sub.add_parser("stability-check")
    p.add_argument("--h", type=float, default=0.1)
    p.add_argument("--decay-rate", type=float, default=0.35)

    p = sub.add_parser("logistic-step")
    p.add_argument("--y", type=float, default=10.0)
    p.add_argument("--r", type=float, default=0.2)
    p.add_argument("--k", type=float, default=100.0)
    p.add_argument("--h", type=float, default=1.0)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "euler-step":
        updated = euler_step(args.t, args.y, args.h, args.decay_rate)
        emit(cmd, args, {"updated_value": updated}, "Computes one Euler update for a simple decay equation.", "Euler updates depend on step size and rate function.")
    elif cmd == "decay-audit":
        rows = decay_rows(args.y0, args.decay_rate, args.h, args.stop_time)
        write_series("decay_audit", rows)
        emit(cmd, args, {"records": len(rows), "final_euler_value": rows[-1]["euler_value"], "final_exact_value": rows[-1]["exact_value"], "final_absolute_error": rows[-1]["absolute_error"], "stability_status": rows[0]["stability_status"]}, "Runs an Euler benchmark against the analytic decay solution.", "Synthetic benchmarks do not guarantee empirical model validity.")
    elif cmd == "step-size-comparison":
        comparison = []
        for h in [1.0, 0.5, 0.25, 0.1]:
            rows = decay_rows(args.y0, args.decay_rate, h, args.stop_time)
            comparison.append({"step_size": h, "records": len(rows), "final_euler_value": rows[-1]["euler_value"], "final_exact_value": rows[-1]["exact_value"], "final_absolute_error": rows[-1]["absolute_error"], "stability_status": rows[0]["stability_status"]})
        write_series("step_size_comparison", comparison)
        emit(cmd, args, {"tested_step_sizes": 4, "smallest_step_final_error": comparison[-1]["final_absolute_error"]}, "Compares Euler results across step sizes.", "Step-size sensitivity should be reviewed before interpretation.")
    elif cmd == "stability-check":
        multiplier = stability_multiplier(args.h, args.decay_rate)
        emit(cmd, args, {"stability_multiplier": multiplier, "stability_status": status_from_multiplier(multiplier)}, "Checks a simple decay stability multiplier.", "Stability conditions depend on equation and method.")
    elif cmd == "logistic-step":
        updated = args.y + args.h * args.r * args.y * (1.0 - args.y / args.k)
        emit(cmd, args, {"updated_value": updated}, "Computes one Euler update for logistic growth.", "Large time steps can distort nonlinear feedback.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
