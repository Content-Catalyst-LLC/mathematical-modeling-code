from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class FlowAuditRecord:
    scenario: str
    segment_count: int
    approximate_flux: float
    approximate_circulation: float
    mean_tangential_alignment: float
    mean_normal_alignment: float
    field_description: str
    geometry_description: str
    warning: str

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (-y, x)

def dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0]*b[0] + a[1]*b[1]

def circle_points(radius: float, segments: int) -> list[tuple[float, float]]:
    return [(radius*math.cos(2*math.pi*i/segments), radius*math.sin(2*math.pi*i/segments)) for i in range(segments + 1)]

def audit_circle_flow(radius: float, segments: int, scenario: str) -> FlowAuditRecord:
    points = circle_points(radius, segments)
    flux_total = 0.0
    circulation_total = 0.0
    tangential_alignments: list[float] = []
    normal_alignments: list[float] = []

    for i in range(segments):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        xm = 0.5*(x0 + x1)
        ym = 0.5*(y0 + y1)
        dx = x1 - x0
        dy = y1 - y0
        segment_length = math.sqrt(dx*dx + dy*dy)
        tangent = (dx/segment_length, dy/segment_length)
        normal = (xm/radius, ym/radius)
        field = vector_field(xm, ym)

        circulation_contribution = dot(field, (dx, dy))
        flux_contribution = dot(field, normal) * segment_length

        circulation_total += circulation_contribution
        flux_total += flux_contribution
        tangential_alignments.append(dot(field, tangent))
        normal_alignments.append(dot(field, normal))

    warning = (
        "Coarse path sampling; circulation and flux should be checked with more segments."
        if segments < 32
        else "Synthetic flow audit; document field meaning, orientation, units, and boundary choice."
    )

    return FlowAuditRecord(
        scenario=scenario,
        segment_count=segments,
        approximate_flux=flux_total,
        approximate_circulation=circulation_total,
        mean_tangential_alignment=sum(tangential_alignments)/len(tangential_alignments),
        mean_normal_alignment=sum(normal_alignments)/len(normal_alignments),
        field_description="rotating field F=<-y,x>",
        geometry_description=f"counterclockwise circle with radius {radius}",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[FlowAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "flux_circulation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "flux_circulation_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_circle_flow(1.0, 16, "coarse_circle"),
        audit_circle_flow(1.0, 64, "medium_circle"),
        audit_circle_flow(1.0, 256, "fine_circle"),
    ]
    write_outputs(args.output_dir, records)
    print("Flux and circulation audit complete.")

if __name__ == "__main__":
    main()
