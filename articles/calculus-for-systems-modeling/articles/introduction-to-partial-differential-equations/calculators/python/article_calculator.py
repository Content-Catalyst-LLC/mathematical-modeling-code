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

def ratio(diffusivity: float, dt: float, dx: float) -> float:
    return diffusivity * dt / (dx ** 2)

def diffusion_cell(left: float, center: float, right: float, stability_ratio: float) -> float:
    return center + stability_ratio * (right - 2 * center + left)

def explicit_diffusion(grid_points: int, diffusivity: float, dx: float, dt: float, steps: int) -> list[dict]:
    r = ratio(diffusivity, dt, dx)
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
            "stability_ratio": r
        })
        updated = field[:]
        for i in range(1, grid_points - 1):
            updated[i] = diffusion_cell(field[i - 1], field[i], field[i + 1], r)
        updated[0] = 0.0
        updated[-1] = 0.0
        field = updated
    return rows

def boundary_note(kind: str) -> str:
    notes = {
        "dirichlet": "A Dirichlet boundary fixes the field value at the domain edge.",
        "neumann": "A Neumann boundary fixes the normal derivative or flux at the domain edge.",
        "robin": "A Robin boundary combines field value and flux, often representing exchange with an environment.",
        "periodic": "A periodic boundary connects opposite edges of an idealized repeating domain."
    }
    return notes.get(kind.lower(), "Boundary kind not recognized; document value, flux, exchange, or periodicity explicitly.")

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("stability-ratio")
    p.add_argument("--diffusivity", type=float, default=0.1)
    p.add_argument("--dt", type=float, default=0.25)
    p.add_argument("--dx", type=float, default=1.0)

    p = sub.add_parser("diffusion-step")
    p.add_argument("--left", type=float, default=0.0)
    p.add_argument("--center", type=float, default=1.0)
    p.add_argument("--right", type=float, default=0.0)
    p.add_argument("--stability-ratio", type=float, default=0.025)

    p = sub.add_parser("explicit-diffusion")
    p.add_argument("--grid-points", type=int, default=51)
    p.add_argument("--diffusivity", type=float, default=0.1)
    p.add_argument("--dx", type=float, default=1.0)
    p.add_argument("--dt", type=float, default=0.25)
    p.add_argument("--steps", type=int, default=100)

    p = sub.add_parser("boundary-condition-note")
    p.add_argument("--kind", type=str, default="dirichlet")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "stability-ratio":
        value = ratio(args.diffusivity, args.dt, args.dx)
        emit(cmd, args, {"stability_ratio": value, "usually_stable_for_1d_explicit_diffusion": value <= 0.5}, "Computes the explicit one-dimensional diffusion stability ratio.", "This rule applies to a simple teaching scheme, not every PDE solver.")
    elif cmd == "diffusion-step":
        value = diffusion_cell(args.left, args.center, args.right, args.stability_ratio)
        emit(cmd, args, {"updated_center": value}, "Computes one finite-difference diffusion update for one grid cell.", "Boundary and grid assumptions shape finite-difference results.")
    elif cmd == "explicit-diffusion":
        rows = explicit_diffusion(args.grid_points, args.diffusivity, args.dx, args.dt, args.steps)
        write_series("explicit_diffusion", rows)
        emit(cmd, args, {"records": len(rows), "final_center_value": rows[-1]["center_value"], "stability_ratio": rows[0]["stability_ratio"]}, "Runs a simple finite-difference diffusion grid simulation.", "Use this as a teaching calculator; real PDE workflows require validation and stability checks.")
    elif cmd == "boundary-condition-note":
        emit(cmd, args, {"note": boundary_note(args.kind)}, "Returns a boundary-condition interpretation note.", "Boundary conditions should be justified and sensitivity-tested.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
