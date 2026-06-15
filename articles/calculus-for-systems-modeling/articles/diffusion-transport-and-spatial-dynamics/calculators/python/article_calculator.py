#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
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

def diffusion_ratio(diffusivity: float, dt: float, dx: float) -> float:
    return diffusivity * dt / (dx ** 2)

def transport_ratio(velocity: float, dt: float, dx: float) -> float:
    return velocity * dt / dx

def advection_diffusion_cell(left: float, center: float, right: float, d_ratio: float, t_ratio: float) -> float:
    diffusion_part = d_ratio * (right - 2 * center + left)
    transport_part = -t_ratio * (center - left)
    return center + diffusion_part + transport_part

def simulate(grid_points: int, diffusivity: float, velocity: float, dx: float, dt: float, steps: int) -> list[dict]:
    d_ratio = diffusion_ratio(diffusivity, dt, dx)
    t_ratio = transport_ratio(velocity, dt, dx)
    field = [0.0 for _ in range(grid_points)]
    field[grid_points // 2] = 1.0
    rows = []
    for step in range(steps + 1):
        rows.append({
            "step": step,
            "time": step * dt,
            "center_value": field[grid_points // 2],
            "total_mass": sum(field) * dx,
            "max_value": max(field),
            "min_value": min(field),
            "diffusion_ratio": d_ratio,
            "transport_ratio": t_ratio
        })
        updated = field[:]
        for i in range(1, grid_points - 1):
            updated[i] = advection_diffusion_cell(field[i - 1], field[i], field[i + 1], d_ratio, t_ratio)
        updated[0] = 0.0
        updated[-1] = 0.0
        field = updated
    return rows

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("diffusion-ratio")
    p.add_argument("--diffusivity", type=float, default=0.08)
    p.add_argument("--dt", type=float, default=0.2)
    p.add_argument("--dx", type=float, default=1.0)

    p = sub.add_parser("transport-ratio")
    p.add_argument("--velocity", type=float, default=0.4)
    p.add_argument("--dt", type=float, default=0.2)
    p.add_argument("--dx", type=float, default=1.0)

    p = sub.add_parser("advection-diffusion-step")
    p.add_argument("--left", type=float, default=0.0)
    p.add_argument("--center", type=float, default=1.0)
    p.add_argument("--right", type=float, default=0.0)
    p.add_argument("--diffusion-ratio", type=float, default=0.016)
    p.add_argument("--transport-ratio", type=float, default=0.08)

    p = sub.add_parser("advection-diffusion-simulation")
    p.add_argument("--grid-points", type=int, default=61)
    p.add_argument("--diffusivity", type=float, default=0.08)
    p.add_argument("--velocity", type=float, default=0.4)
    p.add_argument("--dx", type=float, default=1.0)
    p.add_argument("--dt", type=float, default=0.2)
    p.add_argument("--steps", type=int, default=120)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "diffusion-ratio":
        value = diffusion_ratio(args.diffusivity, args.dt, args.dx)
        emit(cmd, args, {"diffusion_ratio": value}, "Computes a finite-difference diffusion ratio.", "Check scheme-specific stability before interpretation.")
    elif cmd == "transport-ratio":
        value = transport_ratio(args.velocity, args.dt, args.dx)
        emit(cmd, args, {"transport_ratio": value}, "Computes a finite-difference transport ratio.", "Velocity direction, units, and boundary behavior should be documented.")
    elif cmd == "advection-diffusion-step":
        value = advection_diffusion_cell(args.left, args.center, args.right, args.diffusion_ratio, args.transport_ratio)
        emit(cmd, args, {"updated_center": value}, "Computes one one-cell advection-diffusion update.", "Use as a teaching calculator; real workflows need stability and validation.")
    elif cmd == "advection-diffusion-simulation":
        rows = simulate(args.grid_points, args.diffusivity, args.velocity, args.dx, args.dt, args.steps)
        write_series("advection_diffusion_simulation", rows)
        emit(cmd, args, {"records": len(rows), "final_center_value": rows[-1]["center_value"], "diffusion_ratio": rows[0]["diffusion_ratio"], "transport_ratio": rows[0]["transport_ratio"]}, "Runs a simple advection-diffusion grid simulation.", "Boundary, grid, source, sink, and numerical assumptions shape results.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
