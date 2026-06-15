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

def height(x: float, y: float) -> float:
    return 0.1*x*x + 0.05*y*y

def scalar_field(x: float, y: float, z: float | None = None) -> float:
    if z is None:
        z = height(x, y)
    return 1.0 + 0.2*z

def vector_field(x: float, y: float, z: float | None = None) -> tuple[float, float, float]:
    return (0.1*x, 0.1*y, 1.0)

def normal_area_vector(x: float, y: float, step: float) -> tuple[float, float, float]:
    area = step*step
    return (-0.2*x*area, -0.1*y*area, area)

def norm3(v: tuple[float, float, float]) -> float:
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def dot3(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def grid_values(step: float) -> list[float]:
    return [round(-1.0 + i*step, 10) for i in range(int(2.0/step))]

def surface_summary(step: float) -> dict:
    surface_area = 0.0
    scalar_total = 0.0
    flux_total = 0.0
    patch_count = 0
    for x in grid_values(step):
        for y in grid_values(step):
            z = height(x,y)
            area_vector = normal_area_vector(x,y,step)
            patch_area = norm3(area_vector)
            flux = dot3(vector_field(x,y,z), area_vector)
            patch_count += 1
            surface_area += patch_area
            scalar_total += scalar_field(x,y,z) * patch_area
            flux_total += flux
    return {
        "patch_count": patch_count,
        "approximate_surface_area": surface_area,
        "scalar_surface_integral": scalar_total,
        "vector_flux_integral": flux_total,
    }

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("height", "scalar-field", "vector-field"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=1.0)

    for name in ("normal-area-vector", "patch-area", "scalar-patch", "flux-patch"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=1.0)
        p.add_argument("--step", type=float, default=0.25)

    for name in ("surface-audit", "surface-area", "flux-approx"):
        p = sub.add_parser(name)
        p.add_argument("--step", type=float, default=0.25)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "height":
        emit(cmd, args, {"z": height(args.x,args.y)}, "Evaluates graph surface height z=0.1x^2+0.05y^2.")
    elif cmd == "scalar-field":
        emit(cmd, args, {"scalar_value": scalar_field(args.x,args.y)}, "Evaluates scalar field on the graph surface.")
    elif cmd == "vector-field":
        vx, vy, vz = vector_field(args.x,args.y)
        emit(cmd, args, {"vx": vx, "vy": vy, "vz": vz}, "Evaluates the vector field used for flux.")
    elif cmd == "normal-area-vector":
        nx, ny, nz = normal_area_vector(args.x,args.y,args.step)
        emit(cmd, args, {"nx": nx, "ny": ny, "nz": nz}, "Computes oriented normal area vector for a graph-surface patch.")
    elif cmd == "patch-area":
        area = norm3(normal_area_vector(args.x,args.y,args.step))
        emit(cmd, args, {"patch_area": area}, "Computes actual surface patch area.")
    elif cmd == "scalar-patch":
        z = height(args.x,args.y)
        area = norm3(normal_area_vector(args.x,args.y,args.step))
        emit(cmd, args, {"contribution": scalar_field(args.x,args.y,z)*area, "patch_area": area}, "Computes scalar surface-integral patch contribution.")
    elif cmd == "flux-patch":
        z = height(args.x,args.y)
        av = normal_area_vector(args.x,args.y,args.step)
        flux = dot3(vector_field(args.x,args.y,z), av)
        emit(cmd, args, {"flux_contribution": flux}, "Computes vector flux patch contribution.")
    elif cmd == "surface-audit":
        warning = "Grid step is coarse." if args.step > 0.5 else ""
        emit(cmd, args, surface_summary(args.step), "Audits surface area, scalar accumulation, and flux.", warning)
    elif cmd == "surface-area":
        emit(cmd, args, {"approximate_surface_area": surface_summary(args.step)["approximate_surface_area"]}, "Approximates total surface area.")
    elif cmd == "flux-approx":
        emit(cmd, args, {"vector_flux_integral": surface_summary(args.step)["vector_flux_integral"]}, "Approximates vector flux through the surface.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
