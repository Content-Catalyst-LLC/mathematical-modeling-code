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

def system_response(x: float, y: float) -> float:
    return 3.0 * x + 2.0 * y + 0.5 * x * y

def interaction_component(x: float, y: float) -> float:
    return 0.5 * x * y

def is_feasible(x: float, y: float, budget: float = 10.0) -> bool:
    return x >= 0 and y >= 0 and x + y <= budget

def calc_evaluate(args):
    feasible = is_feasible(args.x, args.y, args.budget)
    payload = CalculatorResult("evaluate", vars(args), {"output": system_response(args.x, args.y), "feasible": feasible}, "The output is computed from a two-input response function with an interaction term.", "" if feasible else "Input combination is outside the feasible region.")
    write_outputs("evaluate", payload); return payload

def calc_feasible(args):
    feasible = is_feasible(args.x, args.y, args.budget)
    payload = CalculatorResult("feasible", vars(args), {"feasible": feasible, "remaining_budget": args.budget - args.x - args.y}, "Feasible-region checks prevent impossible input combinations from being treated as valid scenarios.", "" if feasible else "Input combination violates constraints.")
    write_outputs("feasible", payload); return payload

def calc_grid(args):
    rows = []
    for i in range(int(args.max_x / args.step) + 1):
        x = i * args.step
        for j in range(int(args.max_y / args.step) + 1):
            y = j * args.step
            feasible = is_feasible(x, y, args.budget)
            rows.append({"x": x, "y": y, "output": system_response(x, y), "feasible": feasible, "warning": "" if feasible else "Input combination is outside the feasible region."})
    ensure_output_dir()
    with (OUTPUT_DIR / "multivariable_grid.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["x","y","output","feasible","warning"])
        writer.writeheader(); writer.writerows(rows)
    payload = CalculatorResult("grid", vars(args), {"rows_written": len(rows), "feasible_rows": sum(1 for r in rows if r["feasible"])}, "A structured grid supports surface, contour, and feasibility review.")
    write_outputs("grid_summary", payload); return payload

def calc_level_curve(args):
    rows = []
    for i in range(int(args.max_x / args.step) + 1):
        x = i * args.step
        for j in range(int(args.max_y / args.step) + 1):
            y = j * args.step
            output = system_response(x, y)
            if abs(output - args.target) <= args.tolerance:
                rows.append({"x": x, "y": y, "output": output, "difference_from_target": output - args.target})
    ensure_output_dir()
    with (OUTPUT_DIR / "level_curve_candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["x","y","output","difference_from_target"])
        writer.writeheader(); writer.writerows(rows)
    payload = CalculatorResult("level-curve", vars(args), {"candidate_count": len(rows)}, "Level-curve candidates identify input combinations that produce approximately equal output.")
    write_outputs("level_curve_summary", payload); return payload

def calc_interaction(args):
    additive = 3.0 * args.x + 2.0 * args.y
    interaction = interaction_component(args.x, args.y)
    total = additive + interaction
    payload = CalculatorResult("interaction", vars(args), {"additive_component": additive, "interaction_component": interaction, "total_output": total, "interaction_share": interaction / total if total else None}, "The interaction term shows how combined effects differ from purely additive structure.")
    write_outputs("interaction", payload); return payload

def calc_local(args):
    distance = math.sqrt((args.x - args.center_x)**2 + (args.y - args.center_y)**2)
    inside = distance <= args.radius
    payload = CalculatorResult("local-neighborhood", vars(args), {"distance": distance, "inside_neighborhood": inside}, "Local-neighborhood checks help distinguish local interpretation from broader extrapolation.", "" if inside else "Input point is outside the stated local neighborhood.")
    write_outputs("local_neighborhood", payload); return payload

def calc_partial(args, variable):
    if variable == "x":
        derivative = (system_response(args.x + args.h, args.y) - system_response(args.x - args.h, args.y)) / (2 * args.h)
        name = "partial-x"
    else:
        derivative = (system_response(args.x, args.y + args.h) - system_response(args.x, args.y - args.h)) / (2 * args.h)
        name = "partial-y"
    payload = CalculatorResult(name, vars(args), {"central_difference_partial": derivative}, "Numerical partial derivatives approximate local sensitivity along one axis while holding the other input fixed.")
    write_outputs(name.replace("-", "_"), payload); return payload

def calc_sensitivity(args):
    rows = []
    step = (args.x_max - args.x_min) / (args.samples - 1)
    for i in range(args.samples):
        x = args.x_min + i * step
        rows.append({"sample": i+1, "x": x, "y": args.y, "output": system_response(x, args.y)})
    ensure_output_dir()
    with (OUTPUT_DIR / "sensitivity_sweep.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sample","x","y","output"])
        writer.writeheader(); writer.writerows(rows)
    payload = CalculatorResult("sensitivity", vars(args), {"rows_written": len(rows), "min_output": rows[0]["output"], "max_output": rows[-1]["output"]}, "A one-input sensitivity sweep varies x while holding y fixed.")
    write_outputs("sensitivity_summary", payload); return payload

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("evaluate", "feasible"):
        p = sub.add_parser(name); p.add_argument("--x", type=float, default=4); p.add_argument("--y", type=float, default=3); p.add_argument("--budget", type=float, default=10)
    p = sub.add_parser("grid"); p.add_argument("--max-x", type=float, default=10); p.add_argument("--max-y", type=float, default=10); p.add_argument("--step", type=float, default=2); p.add_argument("--budget", type=float, default=10)
    p = sub.add_parser("level-curve"); p.add_argument("--target", type=float, default=30); p.add_argument("--max-x", type=float, default=10); p.add_argument("--max-y", type=float, default=10); p.add_argument("--step", type=float, default=1); p.add_argument("--tolerance", type=float, default=1)
    p = sub.add_parser("interaction"); p.add_argument("--x", type=float, default=4); p.add_argument("--y", type=float, default=3)
    p = sub.add_parser("local-neighborhood"); p.add_argument("--x", type=float, default=4); p.add_argument("--y", type=float, default=3); p.add_argument("--center-x", type=float, default=3); p.add_argument("--center-y", type=float, default=3); p.add_argument("--radius", type=float, default=2)
    for name in ("partial-x", "partial-y"):
        p = sub.add_parser(name); p.add_argument("--x", type=float, default=4); p.add_argument("--y", type=float, default=3); p.add_argument("--h", type=float, default=0.001)
    p = sub.add_parser("sensitivity"); p.add_argument("--x-min", type=float, default=0); p.add_argument("--x-max", type=float, default=10); p.add_argument("--y", type=float, default=3); p.add_argument("--samples", type=int, default=10)
    return parser

def main():
    args = build_parser().parse_args()
    if args.command == "evaluate": payload = calc_evaluate(args)
    elif args.command == "feasible": payload = calc_feasible(args)
    elif args.command == "grid": payload = calc_grid(args)
    elif args.command == "level-curve": payload = calc_level_curve(args)
    elif args.command == "interaction": payload = calc_interaction(args)
    elif args.command == "local-neighborhood": payload = calc_local(args)
    elif args.command == "partial-x": payload = calc_partial(args, "x")
    elif args.command == "partial-y": payload = calc_partial(args, "y")
    elif args.command == "sensitivity": payload = calc_sensitivity(args)
    else: raise ValueError(args.command)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
