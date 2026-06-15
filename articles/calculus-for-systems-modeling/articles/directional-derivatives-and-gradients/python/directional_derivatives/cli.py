from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class DirectionalDerivativeRecord:
    x: float
    y: float
    direction_x: float
    direction_y: float
    unit_x: float
    unit_y: float
    gradient_x: float
    gradient_y: float
    directional_derivative: float
    step_size: float
    estimated_change: float
    actual_change: float
    absolute_error: float
    feasible_direction: bool
    warning: str

def f(x: float, y: float) -> float:
    return 3.0 * x + 2.0 * y + 0.5 * x * y

def gradient(x: float, y: float) -> tuple[float, float]:
    return (3.0 + 0.5 * y, 2.0 + 0.5 * x)

def normalize(vx: float, vy: float) -> tuple[float, float]:
    norm = math.sqrt(vx * vx + vy * vy)
    if norm == 0:
        raise ValueError("Direction vector must be nonzero.")
    return (vx / norm, vy / norm)

def directional_derivative(x: float, y: float, ux: float, uy: float) -> float:
    gx, gy = gradient(x, y)
    return gx * ux + gy * uy

def feasible_direction(x: float, y: float, ux: float, uy: float, step: float, budget: float = 10.0) -> bool:
    return x >= 0 and y >= 0 and x + y <= budget and x + step * ux >= 0 and y + step * uy >= 0 and x + step * ux + y + step * uy <= budget

def audit_direction(x: float, y: float, vx: float, vy: float, step: float) -> DirectionalDerivativeRecord:
    ux, uy = normalize(vx, vy)
    gx, gy = gradient(x, y)
    derivative = directional_derivative(x, y, ux, uy)
    baseline = f(x, y)
    actual = f(x + step * ux, y + step * uy)
    actual_change = actual - baseline
    estimated_change = step * derivative
    feasible = feasible_direction(x, y, ux, uy, step)
    return DirectionalDerivativeRecord(
        x=x, y=y,
        direction_x=vx, direction_y=vy,
        unit_x=ux, unit_y=uy,
        gradient_x=gx, gradient_y=gy,
        directional_derivative=derivative,
        step_size=step,
        estimated_change=estimated_change,
        actual_change=actual_change,
        absolute_error=abs(actual_change - estimated_change),
        feasible_direction=feasible,
        warning="" if feasible else "Direction and step move outside the feasible region.",
    )

def write_outputs(output_dir: Path, records: list[DirectionalDerivativeRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "directional_derivative_gradient_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "directional_derivative_gradient_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_direction(4.0, 3.0, 1.0, 1.0, 0.25),
        audit_direction(4.0, 3.0, 2.0, -1.0, 0.25),
        audit_direction(8.0, 1.0, 1.0, 1.0, 1.0),
    ]
    write_outputs(args.output_dir, records)
    print("Directional derivative and gradient audit complete.")

if __name__ == "__main__":
    main()
