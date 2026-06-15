from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class DynamicAuditRecord:
    scenario: str
    model_type: str
    time: float
    state: float
    rate: float
    growth_rate: float
    carrying_capacity: float | None
    method: str
    warning: str

def exponential_rate(x: float, r: float) -> float:
    return r * x

def logistic_rate(x: float, r: float, capacity: float) -> float:
    return r * x * (1.0 - x / capacity)

def simulate_exponential(x0: float, r: float, dt: float, steps: int) -> list[DynamicAuditRecord]:
    x = x0
    records: list[DynamicAuditRecord] = []
    for n in range(steps + 1):
        t = n * dt
        rate = exponential_rate(x, r)
        records.append(DynamicAuditRecord(
            scenario="exponential_growth",
            model_type="dx_dt_equals_r_x",
            time=t,
            state=x,
            rate=rate,
            growth_rate=r,
            carrying_capacity=None,
            method="explicit_euler",
            warning="Exponential growth assumes no capacity constraint."
        ))
        x = x + dt * rate
    return records

def simulate_logistic(x0: float, r: float, capacity: float, dt: float, steps: int) -> list[DynamicAuditRecord]:
    x = x0
    records: list[DynamicAuditRecord] = []
    for n in range(steps + 1):
        t = n * dt
        rate = logistic_rate(x, r, capacity)
        records.append(DynamicAuditRecord(
            scenario="logistic_growth",
            model_type="dx_dt_equals_r_x_one_minus_x_over_K",
            time=t,
            state=x,
            rate=rate,
            growth_rate=r,
            carrying_capacity=capacity,
            method="explicit_euler",
            warning="Logistic growth assumes a fixed carrying capacity."
        ))
        x = x + dt * rate
    return records

def write_outputs(output_dir: Path, records: list[DynamicAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "dynamic_system_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "dynamic_system_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records: list[DynamicAuditRecord] = []
    records.extend(simulate_exponential(x0=10.0, r=0.35, dt=0.1, steps=100))
    records.extend(simulate_logistic(x0=10.0, r=0.35, capacity=100.0, dt=0.1, steps=100))
    write_outputs(args.output_dir, records)
    print("Dynamic system audit complete.")

if __name__ == "__main__":
    main()
