from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class StokesAuditRecord:
    scenario: str
    radius: float
    boundary_segments: int
    radial_steps: int
    boundary_circulation: float
    surface_curl_flux: float
    absolute_gap: float
    field_description: str
    surface_description: str
    orientation_note: str
    warning: str

def vector_field(x: float, y: float, z: float = 0.0) -> tuple[float, float, float]:
    return (-y, x, 0.0)

def curl_field(x: float, y: float, z: float = 0.0) -> tuple[float, float, float]:
    return (0.0, 0.0, 2.0)

def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def boundary_circulation_circle(radius: float, segments: int) -> float:
    total = 0.0
    for i in range(segments):
        theta0 = 2*math.pi*i/segments
        theta1 = 2*math.pi*(i+1)/segments
        x0, y0 = radius*math.cos(theta0), radius*math.sin(theta0)
        x1, y1 = radius*math.cos(theta1), radius*math.sin(theta1)
        xm, ym = 0.5*(x0+x1), 0.5*(y0+y1)
        dx, dy = x1-x0, y1-y0
        total += dot(vector_field(xm, ym), (dx, dy, 0.0))
    return total

def surface_curl_flux_disk(radius: float, radial_steps: int) -> float:
    total = 0.0
    normal = (0.0, 0.0, 1.0)
    for i in range(radial_steps):
        r0 = radius*i/radial_steps
        r1 = radius*(i+1)/radial_steps
        ring_area = math.pi*(r1*r1 - r0*r0)
        rm = 0.5*(r0+r1)
        total += dot(curl_field(rm, 0.0, 0.0), normal)*ring_area
    return total

def audit_stokes(radius: float, segments: int, radial_steps: int, scenario: str) -> StokesAuditRecord:
    circulation = boundary_circulation_circle(radius, segments)
    curl_flux = surface_curl_flux_disk(radius, radial_steps)
    warning = (
        "Coarse boundary or surface sampling; refine before interpreting the theorem comparison."
        if segments < 64 or radial_steps < 16
        else "Synthetic Stokes theorem audit; document field, surface, boundary, orientation, units, and numerical method."
    )
    return StokesAuditRecord(
        scenario=scenario,
        radius=radius,
        boundary_segments=segments,
        radial_steps=radial_steps,
        boundary_circulation=circulation,
        surface_curl_flux=curl_flux,
        absolute_gap=abs(circulation-curl_flux),
        field_description="F=<-y,x,0>; curl F=<0,0,2>",
        surface_description="horizontal disk with upward normal",
        orientation_note="counterclockwise boundary orientation viewed from positive z",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[StokesAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "stokes_theorem_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "stokes_theorem_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_stokes(1.0, 32, 8, "coarse_audit"),
        audit_stokes(1.0, 128, 32, "medium_audit"),
        audit_stokes(1.0, 512, 128, "fine_audit"),
    ]
    write_outputs(args.output_dir, records)
    print("Stokes theorem audit complete.")

if __name__ == "__main__":
    main()
