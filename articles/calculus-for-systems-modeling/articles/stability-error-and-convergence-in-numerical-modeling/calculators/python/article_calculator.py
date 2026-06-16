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

def rate(t: float, y: float, k: float) -> float:
    return -k * y

def exact(t: float, y0: float, k: float) -> float:
    return y0 * math.exp(-k * t)

def rk4_step(t: float, y: float, h: float, k: float) -> float:
    k1 = rate(t, y, k)
    k2 = rate(t + h / 2, y + h * k1 / 2, k)
    k3 = rate(t + h / 2, y + h * k2 / 2, k)
    k4 = rate(t + h, y + h * k3, k)
    return y + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def simulate(h: float, y0: float = 100.0, decay_rate: float = 0.35, stop_time: float = 20.0) -> float:
    y = y0
    steps = int(round(stop_time / h))
    for step in range(steps):
        y = rk4_step(step * h, y, h, decay_rate)
    return y

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("absolute-error")
    p.add_argument("--numeric", type=float, required=True)
    p.add_argument("--exact", type=float, required=True)

    p = sub.add_parser("relative-error")
    p.add_argument("--numeric", type=float, required=True)
    p.add_argument("--exact", type=float, required=True)

    p = sub.add_parser("euler-stability-factor")
    p.add_argument("--step-size", type=float, default=0.1)
    p.add_argument("--eigenvalue", type=float, default=-1.0)

    p = sub.add_parser("convergence-ratio")
    p.add_argument("--previous-error", type=float, required=True)
    p.add_argument("--current-error", type=float, required=True)

    p = sub.add_parser("rk4-final-error")
    p.add_argument("--step-size", type=float, default=0.5)

    sub.add_parser("refinement-table")
    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "absolute-error":
        err = abs(args.numeric - args.exact)
        emit(cmd, args, {"absolute_error": err}, "Computes absolute numerical error.", "Small numerical error does not imply empirical validity.")
    elif cmd == "relative-error":
        if args.exact == 0:
            raise ValueError("exact value must be nonzero for relative error")
        err = abs(args.numeric - args.exact) / abs(args.exact)
        emit(cmd, args, {"relative_error": err}, "Computes relative numerical error.", "Relative error can be misleading near zero.")
    elif cmd == "euler-stability-factor":
        factor = abs(1 + args.step_size * args.eigenvalue)
        status = "stable_for_linear_test" if factor <= 1 else "unstable_for_linear_test"
        emit(cmd, args, {"amplification_factor": factor, "status": status}, "Computes a simple Euler amplification factor for a linear test problem.", "This is a test-problem diagnostic, not a full stability proof.")
    elif cmd == "convergence-ratio":
        if args.current_error == 0:
            raise ValueError("current_error must be nonzero")
        ratio = args.previous_error / args.current_error
        emit(cmd, args, {"error_ratio": ratio}, "Compares error reduction between refinements.", "Convergence evidence supports numerical reliability, not empirical validity.")
    elif cmd == "rk4-final-error":
        numeric = simulate(args.step_size)
        exact_final = exact(20.0, 100.0, 0.35)
        emit(cmd, args, {"final_numeric_value": numeric, "final_exact_value": exact_final, "final_absolute_error": abs(numeric - exact_final)}, "Computes final RK4 benchmark error for exponential decay.", "Benchmark accuracy does not validate model assumptions.")
    elif cmd == "refinement-table":
        rows = []
        exact_final = exact(20.0, 100.0, 0.35)
        previous = None
        for h in [1.0, 0.5, 0.25, 0.125]:
            numeric = simulate(h)
            err = abs(numeric - exact_final)
            rows.append({"step_size": h, "steps": int(round(20.0 / h)), "final_numeric_value": numeric, "final_exact_value": exact_final, "final_absolute_error": err, "error_ratio_to_previous": "" if previous is None else previous / err})
            previous = err
        write_series("refinement_table", rows)
        emit(cmd, args, {"records": len(rows), "smallest_step_error": rows[-1]["final_absolute_error"]}, "Generates a step-size refinement table.", "A refinement table tests numerical behavior, not real-world truth.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
