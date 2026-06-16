from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class UnitRecord:
    quantity_name: str
    value: float
    unit: str
    dimension: str
    source_note: str
    warning: str

@dataclass(frozen=True)
class ScaleRecord:
    scale_name: str
    scale_value: float
    unit: str
    interpretation: str
    warning: str

@dataclass(frozen=True)
class NondimensionalRecord:
    quantity_name: str
    dimensional_value: float
    scale_value: float
    dimensionless_value: float
    interpretation: str

def build_unit_records() -> list[UnitRecord]:
    return [
        UnitRecord("population_stock", 40.0, "state units", "stock", "synthetic teaching value", "Synthetic value; do not treat as empirical measurement."),
        UnitRecord("carrying_capacity", 100.0, "state units", "stock", "synthetic teaching capacity", "Capacity scale controls normalized interpretation."),
        UnitRecord("growth_rate", 0.35, "per time unit", "inverse time", "synthetic teaching rate", "Rate units must match the time variable."),
    ]

def build_scale_records() -> list[ScaleRecord]:
    return [
        ScaleRecord("stock_scale", 100.0, "state units", "carrying capacity used to normalize population stock", "Changing the capacity scale changes dimensionless stock."),
        ScaleRecord("time_scale", 1 / 0.35, "time units", "inverse growth rate used as characteristic response time", "Changing the growth-rate scale changes dimensionless time."),
    ]

def build_nondimensional_records() -> list[NondimensionalRecord]:
    stock = 40.0
    capacity = 100.0
    time = 20.0
    growth_rate = 0.35
    return [
        NondimensionalRecord("scaled_stock", stock, capacity, stock / capacity, "population stock as fraction of carrying capacity"),
        NondimensionalRecord("scaled_time", time, 1 / growth_rate, growth_rate * time, "time measured in characteristic growth-time units"),
    ]

def write_csv(path: Path, records: list) -> None:
    rows = [asdict(record) for record in records]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    unit_records = build_unit_records()
    scale_records = build_scale_records()
    nondimensional_records = build_nondimensional_records()

    write_csv(output_dir / "tables" / "unit_records.csv", unit_records)
    write_csv(output_dir / "tables" / "scale_records.csv", scale_records)
    write_csv(output_dir / "tables" / "nondimensional_records.csv", nondimensional_records)

    audit = {
        "unit_records": [asdict(record) for record in unit_records],
        "scale_records": [asdict(record) for record in scale_records],
        "nondimensional_records": [asdict(record) for record in nondimensional_records],
        "interpretation_warning": "Scaling improves comparability but does not prove empirical validity.",
    }
    (output_dir / "json" / "scaling_unit_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Scaling and Unit Audit", "", "## Unit Records"]
    for record in unit_records:
        report_lines.append(f"- **{record.quantity_name}** = {record.value} {record.unit}; dimension: {record.dimension}. {record.warning}")
    report_lines.extend(["", "## Scale Records"])
    for record in scale_records:
        report_lines.append(f"- **{record.scale_name}** = {record.scale_value:.6f} {record.unit}; {record.interpretation}. {record.warning}")
    report_lines.extend(["", "## Nondimensional Records"])
    for record in nondimensional_records:
        report_lines.append(f"- **{record.quantity_name}** = {record.dimensionless_value:.6f}; {record.interpretation}")
    report_lines.extend(["", "Scaling improves comparability but does not prove empirical validity."])

    (output_dir / "reports" / "scaling_unit_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Scaling and unit audit outputs generated.")

if __name__ == "__main__":
    main()
