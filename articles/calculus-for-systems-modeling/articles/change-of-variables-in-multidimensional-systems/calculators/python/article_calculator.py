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

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def exposure_polar(r: float, theta: float) -> float:
    return 20.0 * math.exp(-0.4 * r)

def polar_total(radius: float, dr: float, dtheta: float) -> float:
    total = 0.0
    r = dr / 2.0
    while r < radius:
        theta = dtheta / 2.0
        while theta < 2.0 * math.pi:
            total += exposure_polar(r, theta) * r * dr * dtheta
            theta += dtheta
        r += dr
    return total

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("polar-jacobian")
    p.add_argument("--radius", type=float, default=3)

    p = sub.add_parser("polar-area-element")
    p.add_argument("--radius", type=float, default=3)
    p.add_argument("--dr", type=float, default=0.1)
    p.add_argument("--dtheta", type=float, default=0.05)

    p = sub.add_parser("circular-area")
    p.add_argument("--radius", type=float, default=3)

    p = sub.add_parser("polar-density-total")
    p.add_argument("--density", type=float, default=2)
    p.add_argument("--radius", type=float, default=3)

    p = sub.add_parser("cylindrical-volume")
    p.add_argument("--radius", type=float, default=3)
    p.add_argument("--height", type=float, default=4)

    p = sub.add_parser("spherical-volume")
    p.add_argument("--radius", type=float, default=3)

    p = sub.add_parser("linear-det")
    p.add_argument("--a", type=float, default=2)
    p.add_argument("--b", type=float, default=1)
    p.add_argument("--c", type=float, default=0)
    p.add_argument("--d", type=float, default=3)

    p = sub.add_parser("orientation-check")
    p.add_argument("--determinant", type=float, default=-2)

    p = sub.add_parser("singularity-check")
    p.add_argument("--determinant", type=float, default=1e-6)
    p.add_argument("--tolerance", type=float, default=1e-5)

    p = sub.add_parser("polar-audit")
    p.add_argument("--radius", type=float, default=3)
    p.add_argument("--dr", type=float, default=0.25)
    p.add_argument("--dtheta", type=float, default=math.pi / 48)

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "polar-jacobian":
        emit("polar-jacobian", args, {"jacobian_factor": args.radius}, "In polar coordinates, dA = r dr dtheta.")
    elif args.command == "polar-area-element":
        emit("polar-area-element", args, {"area_element": args.radius * args.dr * args.dtheta}, "Computes local polar area element r dr dtheta.")
    elif args.command == "circular-area":
        emit("circular-area", args, {"area": math.pi * args.radius * args.radius}, "Computes circular area using the polar Jacobian factor.")
    elif args.command == "polar-density-total":
        area = math.pi * args.radius * args.radius
        emit("polar-density-total", args, {"area": area, "total": args.density * area}, "Computes constant density over a disk using transformed area.")
    elif args.command == "cylindrical-volume":
        volume = math.pi * args.radius * args.radius * args.height
        emit("cylindrical-volume", args, {"volume": volume}, "Computes cylinder volume using cylindrical-coordinate scaling.")
    elif args.command == "spherical-volume":
        volume = 4.0 / 3.0 * math.pi * args.radius ** 3
        emit("spherical-volume", args, {"volume": volume}, "Computes sphere volume using spherical-coordinate scaling.")
    elif args.command == "linear-det":
        det = args.a * args.d - args.b * args.c
        emit("linear-det", args, {"determinant": det, "absolute_measure_factor": abs(det)}, "Computes determinant and absolute measure factor for a 2x2 linear transformation.")
    elif args.command == "orientation-check":
        if args.determinant < 0:
            status = "orientation reversed"
        elif args.determinant > 0:
            status = "orientation preserved"
        else:
            status = "singular"
        emit("orientation-check", args, {"status": status, "absolute_measure_factor": abs(args.determinant)}, "Classifies orientation and measure factor.")
    elif args.command == "singularity-check":
        singular = abs(args.determinant) <= args.tolerance
        warning = "Transformation is singular or near singular." if singular else ""
        emit("singularity-check", args, {"singular_or_near_singular": singular, "absolute_measure_factor": abs(args.determinant)}, "Checks determinant against singularity tolerance.", warning)
    elif args.command == "polar-audit":
        total = polar_total(args.radius, args.dr, args.dtheta)
        emit("polar-audit", args, {"polar_total": total, "jacobian_rule": "dA = r dr dtheta"}, "Performs a radial polar accumulation using the Jacobian factor.", "Resolution is coarse." if args.dr > 0.5 else "")
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
