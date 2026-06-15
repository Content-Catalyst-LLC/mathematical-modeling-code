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

def fx(x: float, y: float) -> float:
    return 3.0 + 0.5 * y

def fy(x: float, y: float) -> float:
    return 2.0 + 0.5 * x

def total_differential(x: float, y: float, dx: float, dy: float) -> float:
    return fx(x, y) * dx + fy(x, y) * dy

def feasible_displacement(x: float, y: float, dx: float, dy: float, budget: float = 10.0) -> bool:
    return x >= 0 and y >= 0 and x + y <= budget and x + dx >= 0 and y + dy >= 0 and x + dx + y + dy <= budget

def payload(command: str, args, result: dict, interpretation: str, warning: str = ""):
    out = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), out)
    return out

def parse_pair(text: str) -> tuple[float, float]:
    parts = [float(p.strip()) for p in text.split(",")]
    if len(parts) != 2:
        raise ValueError("Expected two comma-separated values.")
    return parts[0], parts[1]

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("evaluate")
    p.add_argument("--x", type=float, default=4)
    p.add_argument("--y", type=float, default=3)

    for name in ("total-differential", "local-linear", "approximation-error"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=4)
        p.add_argument("--y", type=float, default=3)
        p.add_argument("--dx", type=float, default=0.2)
        p.add_argument("--dy", type=float, default=-0.1)

    p = sub.add_parser("gradient-dot")
    p.add_argument("--gradient", type=str, default="4.5,4")
    p.add_argument("--displacement", type=str, default="0.2,-0.1")

    p = sub.add_parser("feasible-displacement")
    p.add_argument("--x", type=float, default=8)
    p.add_argument("--y", type=float, default=1)
    p.add_argument("--dx", type=float, default=1)
    p.add_argument("--dy", type=float, default=1)
    p.add_argument("--budget", type=float, default=10)

    p = sub.add_parser("perturbation-sweep")
    p.add_argument("--x", type=float, default=4)
    p.add_argument("--y", type=float, default=3)
    p.add_argument("--scale-max", type=float, default=2)
    p.add_argument("--samples", type=int, default=10)

    p = sub.add_parser("uncertainty-propagation")
    p.add_argument("--x", type=float, default=4)
    p.add_argument("--y", type=float, default=3)
    p.add_argument("--dx-error", type=float, default=0.1)
    p.add_argument("--dy-error", type=float, default=0.2)

    p = sub.add_parser("tangent-plane")
    p.add_argument("--x0", type=float, default=4)
    p.add_argument("--y0", type=float, default=3)
    p.add_argument("--x", type=float, default=4.2)
    p.add_argument("--y", type=float, default=2.9)

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "evaluate":
        result = {"output": f(args.x, args.y), "partial_x": fx(args.x, args.y), "partial_y": fy(args.x, args.y)}
        out = payload("evaluate", args, result, "Evaluates the baseline function and local partial sensitivities.")
    elif args.command in ("total-differential", "local-linear", "approximation-error"):
        baseline = f(args.x, args.y)
        actual = f(args.x + args.dx, args.y + args.dy)
        change = actual - baseline
        estimate = total_differential(args.x, args.y, args.dx, args.dy)
        result = {
            "baseline_output": baseline,
            "actual_output": actual,
            "actual_change": change,
            "differential_estimate": estimate,
            "local_linear_output": baseline + estimate,
            "absolute_error": abs(change - estimate),
            "feasible_displacement": feasible_displacement(args.x, args.y, args.dx, args.dy),
        }
        warning = "" if result["feasible_displacement"] else "Displacement is outside the feasible region."
        out = payload(args.command, args, result, "Compares total differential approximation with actual function change.", warning)
    elif args.command == "gradient-dot":
        gx, gy = parse_pair(args.gradient)
        dx, dy = parse_pair(args.displacement)
        result = {"gradient_dot_displacement": gx * dx + gy * dy}
        out = payload("gradient-dot", args, result, "Computes the first-order dot product between a gradient and a displacement vector.")
    elif args.command == "feasible-displacement":
        feasible = feasible_displacement(args.x, args.y, args.dx, args.dy, args.budget)
        result = {"feasible_displacement": feasible, "start_sum": args.x + args.y, "end_sum": args.x + args.dx + args.y + args.dy}
        out = payload("feasible-displacement", args, result, "Checks whether a displacement stays within nonnegative and budget constraints.", "" if feasible else "Displacement is outside the feasible region.")
    elif args.command == "perturbation-sweep":
        if args.samples < 2:
            raise ValueError("samples must be at least 2")
        rows = []
        for i in range(args.samples):
            scale = args.scale_max * i / (args.samples - 1)
            dx = 0.2 * scale
            dy = -0.1 * scale
            baseline = f(args.x, args.y)
            actual = f(args.x + dx, args.y + dy)
            change = actual - baseline
            estimate = total_differential(args.x, args.y, dx, dy)
            rows.append({"sample": i+1, "scale": scale, "dx": dx, "dy": dy, "actual_change": change, "differential_estimate": estimate, "absolute_error": abs(change-estimate)})
        ensure_output_dir()
        with (OUTPUT_DIR / "perturbation_sweep.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["sample","scale","dx","dy","actual_change","differential_estimate","absolute_error"])
            writer.writeheader()
            writer.writerows(rows)
        out = payload("perturbation-sweep", args, {"rows_written": len(rows), "max_error": max(r["absolute_error"] for r in rows)}, "Perturbation sweeps show how local approximation error changes with displacement size.")
    elif args.command == "uncertainty-propagation":
        worst_case = abs(fx(args.x, args.y) * args.dx_error) + abs(fy(args.x, args.y) * args.dy_error)
        root_sum_square = math.sqrt((fx(args.x, args.y) * args.dx_error)**2 + (fy(args.x, args.y) * args.dy_error)**2)
        result = {"worst_case_output_error": worst_case, "root_sum_square_output_error": root_sum_square}
        out = payload("uncertainty-propagation", args, result, "Propagates small input uncertainty through local partial sensitivities.")
    elif args.command == "tangent-plane":
        dx = args.x - args.x0
        dy = args.y - args.y0
        estimate = f(args.x0, args.y0) + total_differential(args.x0, args.y0, dx, dy)
        result = {"tangent_plane_estimate": estimate, "actual_output": f(args.x,args.y), "absolute_error": abs(f(args.x,args.y)-estimate)}
        out = payload("tangent-plane", args, result, "Evaluates the tangent-plane approximation at a nearby point.")
    else:
        raise ValueError(args.command)

    print(json.dumps(asdict(out), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
