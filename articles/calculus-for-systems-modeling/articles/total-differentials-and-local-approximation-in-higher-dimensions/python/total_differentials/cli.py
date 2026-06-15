from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class TotalDifferentialRecord:
    x: float
    y: float
    dx: float
    dy: float
    baseline_output: float
    actual_output: float
    actual_change: float
    differential_estimate: float
    absolute_error: float
    feasible_displacement: bool
    warning: str

def f(x: float, y: float) -> float:
    return 3.0 * x + 2.0 * y + 0.5 * x * y

def fx(x: float, y: float) -> float:
    return 3.0 + 0.5 * y

def fy(x: float, y: float) -> float:
    return 2.0 + 0.5 * x

def total_differential(x: float, y: float, dx: float, dy: float) -> float:
    return fx(x, y) * dx + fy(x, y) * dy

def feasible_displacement(x: float, y: float, dx: float, dy: float, budget: float = 10.0) -> bool:
    return x >= 0 and y >= 0 and x + y <= budget and x + dx >= 0 and y + dy >= 0 and x + dx + y + dy <= budget

def audit_case(x: float, y: float, dx: float, dy: float) -> TotalDifferentialRecord:
    baseline = f(x, y)
    actual = f(x + dx, y + dy)
    actual_change = actual - baseline
    estimate = total_differential(x, y, dx, dy)
    feasible = feasible_displacement(x, y, dx, dy)
    return TotalDifferentialRecord(
        x=x,
        y=y,
        dx=dx,
        dy=dy,
        baseline_output=baseline,
        actual_output=actual,
        actual_change=actual_change,
        differential_estimate=estimate,
        absolute_error=abs(actual_change - estimate),
        feasible_displacement=feasible,
        warning="" if feasible else "Displacement is outside the feasible region.",
    )

def write_outputs(output_dir: Path, records: list[TotalDifferentialRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "total_differential_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "total_differential_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = [
        audit_case(4.0, 3.0, 0.2, -0.1),
        audit_case(4.0, 3.0, 1.0, 1.0),
        audit_case(8.0, 1.0, 1.0, 1.0),
    ]
    write_outputs(args.output_dir, records)
    print("Total differential audit complete.")

if __name__ == "__main__":
    main()
