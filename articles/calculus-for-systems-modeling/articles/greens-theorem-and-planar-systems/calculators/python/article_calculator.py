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

def rotation_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def expansion_field(x: float, y: float) -> tuple[float, float]:
    return (x, y)

def square_boundary_points(n: int) -> list[tuple[float, float]]:
    points = []
    for i in range(n):
        t = -1.0 + 2.0*i/n
        points.append((t, -1.0))
    for i in range(n):
        t = -1.0 + 2.0*i/n
        points.append((1.0, t))
    for i in range(n):
        t = 1.0 - 2.0*i/n
        points.append((t, 1.0))
    for i in range(n):
        t = 1.0 - 2.0*i/n
        points.append((-1.0, t))
    points.append(points[0])
    return points

def boundary_circulation(n: int) -> float:
    points = square_boundary_points(n)
    total = 0.0
    for i in range(len(points)-1):
        x0,y0 = points[i]
        x1,y1 = points[i+1]
        xm,ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx,dy = x1-x0, y1-y0
        p,q = rotation_field(xm,ym)
        total += p*dx + q*dy
    return total

def boundary_flux(n: int) -> float:
    points = square_boundary_points(n)
    total = 0.0
    for i in range(len(points)-1):
        x0,y0 = points[i]
        x1,y1 = points[i+1]
        xm,ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx,dy = x1-x0, y1-y0
        p,q = expansion_field(xm,ym)
        total += p*dy + q*(-dx)
    return total

def interior_integral(step: float, value: float = 2.0) -> float:
    n = int(2.0/step)
    return value*n*n*step*step

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("rotation-field", "expansion-field", "planar-curl", "planar-divergence"):
        p = sub.add_parser(name)
        p.add_argument("--x", type=float, default=1.0)
        p.add_argument("--y", type=float, default=1.0)

    for name in ("boundary-circulation", "boundary-flux"):
        p = sub.add_parser(name)
        p.add_argument("--segments", type=int, default=32)

    for name in ("interior-curl", "interior-divergence"):
        p = sub.add_parser(name)
        p.add_argument("--step", type=float, default=0.25)

    p = sub.add_parser("greens-audit")
    p.add_argument("--segments", type=int, default=32)
    p.add_argument("--step", type=float, default=0.25)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "rotation-field":
        p, q = rotation_field(args.x, args.y)
        emit(cmd, args, {"P": p, "Q": q}, "Evaluates circulation-form field F=<-y,x>.")
    elif cmd == "expansion-field":
        p, q = expansion_field(args.x, args.y)
        emit(cmd, args, {"P": p, "Q": q}, "Evaluates flux-form field G=<x,y>.")
    elif cmd == "planar-curl":
        emit(cmd, args, {"planar_curl": 2.0}, "Computes planar curl for F=<-y,x>.")
    elif cmd == "planar-divergence":
        emit(cmd, args, {"planar_divergence": 2.0}, "Computes planar divergence for G=<x,y>.")
    elif cmd == "boundary-circulation":
        emit(cmd, args, {"boundary_circulation": boundary_circulation(args.segments)}, "Approximates boundary circulation around the square.")
    elif cmd == "boundary-flux":
        emit(cmd, args, {"boundary_flux": boundary_flux(args.segments)}, "Approximates outward boundary flux around the square.")
    elif cmd == "interior-curl":
        emit(cmd, args, {"interior_curl_integral": interior_integral(args.step)}, "Approximates interior curl integral over the square.")
    elif cmd == "interior-divergence":
        emit(cmd, args, {"interior_divergence_integral": interior_integral(args.step)}, "Approximates interior divergence integral over the square.")
    elif cmd == "greens-audit":
        bc = boundary_circulation(args.segments)
        ic = interior_integral(args.step)
        bf = boundary_flux(args.segments)
        idv = interior_integral(args.step)
        warning = "Coarse boundary or interior sampling." if args.segments < 16 or args.step > 0.25 else ""
        emit(cmd, args, {
            "boundary_circulation": bc,
            "interior_curl_integral": ic,
            "boundary_flux": bf,
            "interior_divergence_integral": idv,
            "circulation_gap": abs(bc-ic),
            "flux_gap": abs(bf-idv),
        }, "Compares Green's theorem boundary and interior quantities.", warning)
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
