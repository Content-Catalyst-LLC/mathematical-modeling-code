from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class PDEGridRecord:
    step: int
    time: float
    center_value: float
    total_mass: float
    max_value: float
    min_value: float
    stability_ratio: float
    warning: str

def stability_ratio(diffusivity: float, dt: float, dx: float) -> float:
    if dx <= 0:
        raise ValueError("dx must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if diffusivity < 0:
        raise ValueError("diffusivity must be nonnegative")
    return diffusivity * dt / (dx ** 2)

def initialize_field(grid_points: int) -> list[float]:
    if grid_points < 3:
        raise ValueError("grid_points must be at least 3")
    field = [0.0 for _ in range(grid_points)]
    field[grid_points // 2] = 1.0
    return field

def diffusion_step(field: list[float], ratio: float) -> list[float]:
    updated = field[:]
    for i in range(1, len(field) - 1):
        updated[i] = field[i] + ratio * (field[i + 1] - 2 * field[i] + field[i - 1])
    updated[0] = 0.0
    updated[-1] = 0.0
    return updated

def simulate_diffusion(grid_points: int, diffusivity: float, dx: float, dt: float, steps: int) -> list[PDEGridRecord]:
    ratio = stability_ratio(diffusivity, dt, dx)
    field = initialize_field(grid_points)
    records: list[PDEGridRecord] = []
    for step in range(steps + 1):
        records.append(PDEGridRecord(
            step=step,
            time=step * dt,
            center_value=field[grid_points // 2],
            total_mass=sum(field) * dx,
            max_value=max(field),
            min_value=min(field),
            stability_ratio=ratio,
            warning="Explicit diffusion schemes require stability checks; boundary and grid assumptions shape results."
        ))
        field = diffusion_step(field, ratio)
    return records

def write_outputs(output_dir: Path, records: list[PDEGridRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "pde_diffusion_grid_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "pde_diffusion_grid_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "pde_diffusion_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "pde_diffusion_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--grid-points", type=int, default=51)
    parser.add_argument("--diffusivity", type=float, default=0.1)
    parser.add_argument("--dx", type=float, default=1.0)
    parser.add_argument("--dt", type=float, default=0.25)
    parser.add_argument("--steps", type=int, default=100)
    args = parser.parse_args()
    ratio = stability_ratio(args.diffusivity, args.dt, args.dx)
    records = simulate_diffusion(args.grid_points, args.diffusivity, args.dx, args.dt, args.steps)
    summary = {
        "grid_points": args.grid_points,
        "diffusivity": args.diffusivity,
        "dx": args.dx,
        "dt": args.dt,
        "stability_ratio": ratio,
        "stability_rule_of_thumb": "For this explicit one-dimensional diffusion scheme, the stability ratio should usually be no greater than 0.5.",
        "final_center_value": records[-1].center_value,
        "interpretation": "The grid audit records how a concentrated initial field spreads under diffusion-like dynamics."
    }
    write_outputs(args.output_dir, records, summary)
    print("PDE diffusion grid audit complete.")

if __name__ == "__main__":
    main()
