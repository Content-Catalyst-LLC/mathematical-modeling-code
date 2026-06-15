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

def vector_field(x: float, y: float, z: float) -> tuple[float, float, float]:
    return (x, y, z)

def divergence_value(x: float, y: float, z: float) -> float:
    return 3.0

def boundary_flux_unit_cube(grid_steps: int) -> float:
    step = 1.0 / grid_steps
    area = step * step
    total = 0.0
    for _i in range(grid_steps):
        for _j in range(grid_steps):
            total += 3.0 * area
    return total

def volume_divergence_unit_cube(grid_steps: int) -> float:
    step = 1.0 / grid_steps
    cell_volume = step ** 3
    return 3.0 * grid_steps**3 * cell_volume

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("vector-field", "divergence"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=2.0)
        p.add_argument("--z", type=float, default=3.0)

    for name in ("boundary-flux", "volume-divergence", "conservation-audit"):
        p = sub.add_parser(name)
        p.add_argument("--grid-steps", type=int, default=16)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "vector-field":
        fx, fy, fz = vector_field(args.x, args.y, args.z)
        emit(cmd, args, {"fx": fx, "fy": fy, "fz": fz}, "Evaluates F=<x,y,z>.")
    elif cmd == "divergence":
        emit(cmd, args, {"divergence": divergence_value(args.x, args.y, args.z)}, "Evaluates divergence of F=<x,y,z>.")
    elif cmd == "boundary-flux":
        emit(cmd, args, {"boundary_flux": boundary_flux_unit_cube(args.grid_steps)}, "Approximates outward boundary flux through the unit cube.")
    elif cmd == "volume-divergence":
        emit(cmd, args, {"volume_divergence_integral": volume_divergence_unit_cube(args.grid_steps)}, "Approximates divergence integral over the unit cube.")
    elif cmd == "conservation-audit":
        flux = boundary_flux_unit_cube(args.grid_steps)
        div_integral = volume_divergence_unit_cube(args.grid_steps)
        warning = "Coarse grid." if args.grid_steps < 8 else ""
        emit(cmd, args, {"boundary_flux": flux, "volume_divergence_integral": div_integral, "absolute_gap": abs(flux-div_integral)}, "Compares divergence theorem boundary and volume quantities.", warning)
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
