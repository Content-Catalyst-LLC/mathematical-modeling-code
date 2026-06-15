from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class LineIntegralAuditRecord:
    scenario: str
    time_step: float
    point_count: int
    path_length: float
    scalar_line_integral: float
    vector_line_integral: float
    average_alignment: float
    maximum_segment_length: float
    path_description: str
    warning: str

def path(t: float) -> tuple[float, float]:
    return (t, math.sin(t))

def scalar_field(x: float, y: float) -> float:
    return 1.0 + y * y

def vector_field(x: float, y: float) -> tuple[float, float]:
    return (1.0, x)

def distance(p: tuple[float, float], q: tuple[float, float]) -> float:
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)

def dot(a: tuple[float, float], b: tuple[float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1]

def sample_times(start: float, stop: float, step: float) -> list[float]:
    count = int((stop - start) / step)
    return [start + i * step for i in range(count + 1)]

def audit_line_integral(step: float, scenario: str) -> LineIntegralAuditRecord:
    times = sample_times(0.0, 2.0 * math.pi, step)
    points = [path(t) for t in times]
    path_length = 0.0
    scalar_total = 0.0
    vector_total = 0.0
    alignments: list[float] = []
    segment_lengths: list[float] = []

    for i in range(len(points) - 1):
        p = points[i]
        q = points[i + 1]
        dx = q[0] - p[0]
        dy = q[1] - p[1]
        segment_length = distance(p, q)
        field_scalar = scalar_field(p[0], p[1])
        field_vector = vector_field(p[0], p[1])
        path_length += segment_length
        scalar_total += field_scalar * segment_length
        vector_total += dot(field_vector, (dx, dy))
        alignments.append(dot(field_vector, (dx, dy)) / max(segment_length, 1e-12))
        segment_lengths.append(segment_length)

    warning = (
        "Time step is coarse; path turns and field variation may be undersampled."
        if step > 0.5
        else "Synthetic line-integral audit; document path, field, units, and interpolation."
    )
    return LineIntegralAuditRecord(
        scenario=scenario,
        time_step=step,
        point_count=len(points),
        path_length=path_length,
        scalar_line_integral=scalar_total,
        vector_line_integral=vector_total,
        average_alignment=sum(alignments) / len(alignments),
        maximum_segment_length=max(segment_lengths),
        path_description="path r(t) = <t, sin(t)> for 0 <= t <= 2pi",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[LineIntegralAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "line_integral_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "line_integral_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_line_integral(1.0, "coarse_path"),
        audit_line_integral(0.5, "medium_path"),
        audit_line_integral(0.25, "fine_path"),
    ]
    write_outputs(args.output_dir, records)
    print("Line-integral audit complete.")

if __name__ == "__main__":
    main()
