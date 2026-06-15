from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class DivergenceAuditRecord:
    scenario: str
    grid_steps: int
    boundary_flux: float
    volume_divergence_integral: float
    absolute_gap: float
    field_description: str
    volume_description: str
    normal_note: str
    warning: str

def vector_field(x: float, y: float, z: float) -> tuple[float, float, float]:
    return (x, y, z)

def divergence(x: float, y: float, z: float) -> float:
    return 3.0

def boundary_flux_unit_cube(grid_steps: int) -> float:
    step = 1.0 / grid_steps
    area = step * step
    total = 0.0
    for i in range(grid_steps):
        for j in range(grid_steps):
            y = (i + 0.5) * step
            z = (j + 0.5) * step
            fx, fy, fz = vector_field(0.0, y, z)
            total += fx * (-1.0) * area
            fx, fy, fz = vector_field(1.0, y, z)
            total += fx * 1.0 * area

            x = (i + 0.5) * step
            z = (j + 0.5) * step
            fx, fy, fz = vector_field(x, 0.0, z)
            total += fy * (-1.0) * area
            fx, fy, fz = vector_field(x, 1.0, z)
            total += fy * 1.0 * area

            x = (i + 0.5) * step
            y = (j + 0.5) * step
            fx, fy, fz = vector_field(x, y, 0.0)
            total += fz * (-1.0) * area
            fx, fy, fz = vector_field(x, y, 1.0)
            total += fz * 1.0 * area
    return total

def volume_divergence_unit_cube(grid_steps: int) -> float:
    step = 1.0 / grid_steps
    cell_volume = step ** 3
    total = 0.0
    for i in range(grid_steps):
        for j in range(grid_steps):
            for k in range(grid_steps):
                x = (i + 0.5) * step
                y = (j + 0.5) * step
                z = (k + 0.5) * step
                total += divergence(x, y, z) * cell_volume
    return total

def audit_divergence_theorem(grid_steps: int, scenario: str) -> DivergenceAuditRecord:
    flux = boundary_flux_unit_cube(grid_steps)
    div_integral = volume_divergence_unit_cube(grid_steps)
    warning = (
        "Coarse grid; refine before interpreting the boundary-volume comparison."
        if grid_steps < 8
        else "Synthetic divergence theorem audit; document field, volume, boundary, normals, units, and numerical method."
    )
    return DivergenceAuditRecord(
        scenario=scenario,
        grid_steps=grid_steps,
        boundary_flux=flux,
        volume_divergence_integral=div_integral,
        absolute_gap=abs(flux - div_integral),
        field_description="F=<x,y,z>; divergence = 3",
        volume_description="unit cube [0,1] x [0,1] x [0,1]",
        normal_note="all six cube faces use outward normals",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[DivergenceAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "divergence_theorem_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "divergence_theorem_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_divergence_theorem(4, "coarse_audit"),
        audit_divergence_theorem(16, "medium_audit"),
        audit_divergence_theorem(64, "fine_audit"),
    ]
    write_outputs(args.output_dir, records)
    print("Divergence theorem audit complete.")

if __name__ == "__main__":
    main()
