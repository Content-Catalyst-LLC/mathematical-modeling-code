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

def exposure_field(x: float, y: float) -> float:
    return 10.0 + 2.0*x + 0.5*y*y

def population_density(x: float, y: float) -> float:
    return 100.0 + 10.0*y + 5.0*math.sin(x)

def in_region(x: float, y: float) -> bool:
    return x*x + y*y <= 9.0

def grid_values(step: float) -> list[float]:
    return [round(-3.0 + i*step, 10) for i in range(int(6.0 / step) + 1)]

def compute_grid(step: float) -> dict:
    cell_area = step * step
    cells = 0
    total = 0.0
    population_total = 0.0
    population_burden = 0.0
    for x in grid_values(step):
        for y in grid_values(step):
            if in_region(x, y):
                exposure = exposure_field(x, y)
                pop = population_density(x, y)
                cells += 1
                total += exposure * cell_area
                population_total += pop * cell_area
                population_burden += exposure * pop * cell_area
    area = cells * cell_area
    return {
        "cells_in_region": cells,
        "cell_area": cell_area,
        "total_area": area,
        "total_density_accumulation": total,
        "area_weighted_average": total / area,
        "population_total": population_total,
        "population_weighted_burden": population_burden,
        "population_weighted_average_exposure": population_burden / population_total,
    }

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("rectangle-total")
    p.add_argument("--density", type=float, default=12)
    p.add_argument("--width", type=float, default=4)
    p.add_argument("--height", type=float, default=3)

    p = sub.add_parser("volume-total")
    p.add_argument("--density", type=float, default=5)
    p.add_argument("--length", type=float, default=4)
    p.add_argument("--width", type=float, default=3)
    p.add_argument("--height", type=float, default=2)

    p = sub.add_parser("polar-area")
    p.add_argument("--radius", type=float, default=3)

    p = sub.add_parser("polar-density-total")
    p.add_argument("--density", type=float, default=2)
    p.add_argument("--radius", type=float, default=3)

    for name in ("grid-total", "area-average", "population-weighted"):
        p = sub.add_parser(name)
        p.add_argument("--step", type=float, default=0.5)

    p = sub.add_parser("cell-sum")
    p.add_argument("--values", type=float, nargs="+", default=[1,2,3,4])
    p.add_argument("--cell-area", type=float, default=0.25)

    p = sub.add_parser("weighted-average")
    p.add_argument("--values", type=float, nargs="+", default=[10,20,30])
    p.add_argument("--weights", type=float, nargs="+", default=[1,2,3])

    p = sub.add_parser("resolution-scan")
    p.add_argument("--steps", type=float, nargs="+", default=[1.0,0.5,0.25])

    return parser

def main():
    args = build_parser().parse_args()

    if args.command == "rectangle-total":
        area = args.width * args.height
        emit("rectangle-total", args, {"area": area, "total": args.density * area}, "Computes density times rectangular area.")
    elif args.command == "volume-total":
        volume = args.length * args.width * args.height
        emit("volume-total", args, {"volume": volume, "total": args.density * volume}, "Computes density times rectangular volume.")
    elif args.command == "polar-area":
        emit("polar-area", args, {"area": math.pi * args.radius * args.radius}, "Computes circular area using the polar area element.")
    elif args.command == "polar-density-total":
        area = math.pi * args.radius * args.radius
        emit("polar-density-total", args, {"area": area, "total": args.density * area}, "Computes constant density over a circular polar region.")
    elif args.command == "grid-total":
        data = compute_grid(args.step)
        emit("grid-total", args, data, "Approximates spatial accumulation by summing gridded cells.", "Coarse grid may smooth local variation." if args.step > 0.5 else "")
    elif args.command == "area-average":
        data = compute_grid(args.step)
        emit("area-average", args, {"area_weighted_average": data["area_weighted_average"], "total_area": data["total_area"]}, "Computes an area-weighted spatial average.")
    elif args.command == "population-weighted":
        data = compute_grid(args.step)
        emit("population-weighted", args, {"population_weighted_average_exposure": data["population_weighted_average_exposure"], "population_weighted_burden": data["population_weighted_burden"], "population_total": data["population_total"]}, "Computes population-weighted exposure and total burden.")
    elif args.command == "cell-sum":
        total = sum(args.values) * args.cell_area
        emit("cell-sum", args, {"cell_count": len(args.values), "total": total}, "Computes a simple cell-value sum multiplied by cell area.")
    elif args.command == "weighted-average":
        if len(args.values) != len(args.weights):
            raise ValueError("values and weights must have equal length")
        denom = sum(args.weights)
        value = sum(v*w for v,w in zip(args.values,args.weights)) / denom
        emit("weighted-average", args, {"weighted_average": value, "weight_total": denom}, "Computes a weighted average.")
    elif args.command == "resolution-scan":
        rows = [{"step": step, **compute_grid(step)} for step in args.steps]
        emit("resolution-scan", args, {"cases": len(rows), "scan": rows}, "Scans spatial accumulation across grid resolutions.", "Resolution can materially change totals.")
    else:
        raise ValueError(args.command)

if __name__ == "__main__":
    main()
