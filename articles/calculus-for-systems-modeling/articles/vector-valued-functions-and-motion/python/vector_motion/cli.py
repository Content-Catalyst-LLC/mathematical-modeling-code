from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class TrajectoryAuditRecord:
    scenario: str
    time_step: float
    point_count: int
    approximate_arc_length: float
    displacement_magnitude: float
    path_efficiency: float
    average_speed: float
    maximum_speed: float
    domain_description: str
    warning: str

def position(t: float) -> tuple[float, float]:
    return (t, math.sin(t))

def velocity(t: float) -> tuple[float, float]:
    return (1.0, math.cos(t))

def acceleration(t: float) -> tuple[float, float]:
    return (0.0, -math.sin(t))

def distance(p: tuple[float, float], q: tuple[float, float]) -> float:
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)

def sample_times(start: float, stop: float, step: float) -> list[float]:
    count = int((stop - start) / step)
    return [start + i * step for i in range(count + 1)]

def audit_trajectory(step: float, scenario: str) -> TrajectoryAuditRecord:
    times = sample_times(0.0, 2.0 * math.pi, step)
    points = [position(t) for t in times]
    segment_lengths = [distance(points[i], points[i + 1]) for i in range(len(points) - 1)]
    speeds = [segment_lengths[i] / (times[i + 1] - times[i]) for i in range(len(segment_lengths))]
    arc_length = sum(segment_lengths)
    displacement = distance(points[0], points[-1])
    efficiency = displacement / max(arc_length, 1e-12)
    warning = (
        "Time step is coarse; turns and speed variation may be undersampled."
        if step > 0.5
        else "Synthetic trajectory audit; document units, parameter meaning, and sampling."
    )
    return TrajectoryAuditRecord(
        scenario=scenario,
        time_step=step,
        point_count=len(points),
        approximate_arc_length=arc_length,
        displacement_magnitude=displacement,
        path_efficiency=efficiency,
        average_speed=sum(speeds) / len(speeds),
        maximum_speed=max(speeds),
        domain_description="trajectory r(t) = <t, sin(t)> for 0 <= t <= 2pi",
        warning=warning,
    )

def write_outputs(output_dir: Path, records: list[TrajectoryAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "trajectory_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "trajectory_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_trajectory(1.0, "coarse_time_step"),
        audit_trajectory(0.5, "medium_time_step"),
        audit_trajectory(0.25, "fine_time_step"),
    ]
    write_outputs(args.output_dir, records)
    print("Trajectory audit complete.")

if __name__ == "__main__":
    main()
