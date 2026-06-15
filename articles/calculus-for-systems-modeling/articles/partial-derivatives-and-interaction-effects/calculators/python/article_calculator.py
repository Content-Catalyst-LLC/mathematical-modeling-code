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
    flat.update({f"input_{k}": v for k, v in payload.inputs.items()})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, (list, dict))})
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

def f(x: float, y: float) -> float:
    return 3.0 * x + 2.0 * y + 0.5 * x * y

def partial_x(x: float, y: float) -> float:
    return 3.0 + 0.5 * y

def partial_y(x: float, y: float) -> float:
    return 2.0 + 0.5 * x

def cross_partial_xy(x: float, y: float) -> float:
    return 0.5

def interaction_component(x: float, y: float) -> float:
    return 0.5 * x * y

def is_feasible(x: float, y: float, budget: float = 10.0) -> bool:
    return x >= 0 and y >= 0 and x + y <= budget

def result_payload(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    return payload

def calc_grid(args):
    rows = []
    for i in range(int(args.max_x / args.step) + 1):
        x = i * args.step
        for j in range(int(args.max_y / args.step) + 1):
            y = j * args.step
            feasible = is_feasible(x, y, args.budget)
            rows.append({"x": x, "y": y, "output": f(x,y), "partial_x": partial_x(x,y), "partial_y": partial_y(x,y), "cross_partial_xy": cross_partial_xy(x,y), "feasible": feasible, "warning": "" if feasible else "Input combination is outside the feasible region."})
    ensure_output_dir()
    with (OUTPUT_DIR / "partial_derivative_grid.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["x","y","output","partial_x","partial_y","cross_partial_xy","feasible","warning"])
        writer.writeheader()
        writer.writerows(rows)
    return result_payload("grid", args, {"rows_written": len(rows), "feasible_rows": sum(1 for r in rows if r["feasible"])}, "A derivative grid maps local sensitivities and interactions across input space.")

def calc_numeric_partial(args, variable):
    if variable == "x":
        estimate = (f(args.x + args.h, args.y) - f(args.x - args.h, args.y)) / (2 * args.h)
        analytic = partial_x(args.x, args.y)
        name = "numeric-partial-x"
    else:
        estimate = (f(args.x, args.y + args.h) - f(args.x, args.y - args.h)) / (2 * args.h)
        analytic = partial_y(args.x, args.y)
        name = "numeric-partial-y"
    return result_payload(name, args, {"numeric_estimate": estimate, "analytic_reference": analytic, "absolute_error": abs(analytic-estimate)}, "A central difference estimates the partial derivative numerically and compares it with the analytic value.")

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("evaluate", "partial-x", "partial-y", "cross-partial", "interaction"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=4)
        p.add_argument("--y", type=float, default=3)

    p = sub.add_parser("grid")
    p.add_argument("--max-x", type=float, default=10)
    p.add_argument("--max-y", type=float, default=10)
    p.add_argument("--step", type=float, default=2)
    p.add_argument("--budget", type=float, default=10)

    for name in ("numeric-partial-x", "numeric-partial-y"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=4)
        p.add_argument("--y", type=float, default=3)
        p.add_argument("--h", type=float, default=0.001)

    p = sub.add_parser("feasible")
    p.add_argument("--x", type=float, default=8)
    p.add_argument("--y", type=float, default=4)
    p.add_argument("--budget", type=float, default=10)

    p = sub.add_parser("local-neighborhood")
    p.add_argument("--x", type=float, default=4)
    p.add_argument("--y", type=float, default=3)
    p.add_argument("--center-x", type=float, default=3)
    p.add_argument("--center-y", type=float, default=3)
    p.add_argument("--radius", type=float, default=2)

    p = sub.add_parser("sensitivity")
    p.add_argument("--x-min", type=float, default=0)
    p.add_argument("--x-max", type=float, default=10)
    p.add_argument("--y", type=float, default=3)
    p.add_argument("--samples", type=int, default=10)

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "evaluate":
        payload = result_payload("evaluate", args, {"output": f(args.x,args.y)}, "The function output includes additive and interaction components.")
    elif args.command == "partial-x":
        payload = result_payload("partial-x", args, {"partial_x": partial_x(args.x,args.y)}, "Partial x measures local sensitivity to x while y is held fixed.")
    elif args.command == "partial-y":
        payload = result_payload("partial-y", args, {"partial_y": partial_y(args.x,args.y)}, "Partial y measures local sensitivity to y while x is held fixed.")
    elif args.command == "cross-partial":
        payload = result_payload("cross-partial", args, {"cross_partial_xy": cross_partial_xy(args.x,args.y)}, "The cross partial measures how one partial derivative changes with the other variable.")
    elif args.command == "interaction":
        additive = 3.0 * args.x + 2.0 * args.y
        interaction = interaction_component(args.x,args.y)
        total = additive + interaction
        payload = result_payload("interaction", args, {"additive_component": additive, "interaction_component": interaction, "total_output": total, "interaction_share": interaction / total if total else None}, "The interaction term shows how combined effects differ from a purely additive model.")
    elif args.command == "grid":
        payload = calc_grid(args)
    elif args.command == "numeric-partial-x":
        payload = calc_numeric_partial(args, "x")
    elif args.command == "numeric-partial-y":
        payload = calc_numeric_partial(args, "y")
    elif args.command == "feasible":
        feasible = is_feasible(args.x,args.y,args.budget)
        payload = result_payload("feasible", args, {"feasible": feasible, "remaining_budget": args.budget - args.x - args.y}, "Feasible-change checks separate coordinate sensitivity from practical intervention.", "" if feasible else "Input combination violates constraints.")
    elif args.command == "local-neighborhood":
        distance = math.sqrt((args.x-args.center_x)**2 + (args.y-args.center_y)**2)
        inside = distance <= args.radius
        payload = result_payload("local-neighborhood", args, {"distance": distance, "inside_neighborhood": inside}, "Local-neighborhood checks show whether derivative interpretation is near the stated reference state.", "" if inside else "Input point is outside the stated local neighborhood.")
    elif args.command == "sensitivity":
        if args.samples < 2:
            raise ValueError("samples must be at least 2")
        step = (args.x_max - args.x_min) / (args.samples - 1)
        rows = []
        for i in range(args.samples):
            x = args.x_min + i * step
            rows.append({"sample": i+1, "x": x, "y": args.y, "output": f(x,args.y), "partial_x": partial_x(x,args.y), "partial_y": partial_y(x,args.y)})
        ensure_output_dir()
        with (OUTPUT_DIR / "sensitivity_sweep.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["sample","x","y","output","partial_x","partial_y"])
            writer.writeheader()
            writer.writerows(rows)
        payload = result_payload("sensitivity", args, {"rows_written": len(rows), "min_output": rows[0]["output"], "max_output": rows[-1]["output"]}, "A sensitivity sweep varies one input while holding another fixed.")
    else:
        raise ValueError(args.command)

    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
