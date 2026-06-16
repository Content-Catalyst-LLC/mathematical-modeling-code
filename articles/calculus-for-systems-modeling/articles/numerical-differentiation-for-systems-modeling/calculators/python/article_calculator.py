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

def signal(x: float) -> float:
    return math.sin(x) + 0.1 * x * x

def true_derivative(x: float) -> float:
    return math.cos(x) + 0.2 * x

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("forward-difference")
    p.add_argument("--f-current", type=float, default=1.0)
    p.add_argument("--f-next", type=float, default=1.12)
    p.add_argument("--h", type=float, default=0.1)

    p = sub.add_parser("backward-difference")
    p.add_argument("--f-previous", type=float, default=0.89)
    p.add_argument("--f-current", type=float, default=1.0)
    p.add_argument("--h", type=float, default=0.1)

    p = sub.add_parser("central-difference")
    p.add_argument("--f-previous", type=float, default=0.89)
    p.add_argument("--f-next", type=float, default=1.12)
    p.add_argument("--h", type=float, default=0.1)

    p = sub.add_parser("second-central-difference")
    p.add_argument("--f-previous", type=float, default=0.89)
    p.add_argument("--f-current", type=float, default=1.0)
    p.add_argument("--f-next", type=float, default=1.12)
    p.add_argument("--h", type=float, default=0.1)

    p = sub.add_parser("benchmark-audit")
    p.add_argument("--start", type=float, default=0.0)
    p.add_argument("--stop", type=float, default=10.0)
    p.add_argument("--h", type=float, default=0.1)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command
    h = getattr(args, "h", 0.1)
    if h <= 0:
        raise ValueError("h must be positive")

    if cmd == "forward-difference":
        value = (args.f_next - args.f_current) / h
        emit(cmd, args, {"derivative_estimate": value}, "Estimates a derivative using current and next values.", "Forward differences are one-sided and step-size dependent.")
    elif cmd == "backward-difference":
        value = (args.f_current - args.f_previous) / h
        emit(cmd, args, {"derivative_estimate": value}, "Estimates a derivative using previous and current values.", "Backward differences are one-sided and step-size dependent.")
    elif cmd == "central-difference":
        value = (args.f_next - args.f_previous) / (2 * h)
        emit(cmd, args, {"derivative_estimate": value}, "Estimates a derivative using values on both sides.", "Central differences require neighboring values on both sides.")
    elif cmd == "second-central-difference":
        value = (args.f_next - 2 * args.f_current + args.f_previous) / (h * h)
        emit(cmd, args, {"second_derivative_estimate": value}, "Estimates a second derivative using a central stencil.", "Second derivatives are especially sensitive to noise.")
    elif cmd == "benchmark-audit":
        n = int(round((args.stop - args.start) / h))
        xs = [args.start + i * h for i in range(n + 1)]
        values = [signal(x) for x in xs]
        rows = []
        for i, x in enumerate(xs):
            central = None
            err = None
            if 0 < i < len(xs) - 1:
                central = (values[i + 1] - values[i - 1]) / (2 * h)
                err = abs(central - true_derivative(x))
            rows.append({"index": i, "x": x, "value": values[i], "true_derivative": true_derivative(x), "central_difference": central, "central_absolute_error": err, "h": h})
        write_series("benchmark_audit", rows)
        errors = [row["central_absolute_error"] for row in rows if row["central_absolute_error"] is not None]
        emit(cmd, args, {"records": len(rows), "mean_central_absolute_error": sum(errors)/len(errors), "max_central_absolute_error": max(errors)}, "Runs a smooth synthetic benchmark for central differences.", "Synthetic accuracy does not guarantee empirical derivative reliability.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
