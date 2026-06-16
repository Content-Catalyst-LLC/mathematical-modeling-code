from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class CalibrationDataPoint:
    time: float
    observed_value: float

@dataclass(frozen=True)
class CalibrationCandidate:
    growth_rate: float
    carrying_capacity: float
    loss: float
    mean_absolute_residual: float
    max_absolute_residual: float
    warning: str

@dataclass(frozen=True)
class ResidualRecord:
    time: float
    observed_value: float
    predicted_value: float
    residual: float
    squared_residual: float

def logistic_solution(t: float, x0: float, growth_rate: float, carrying_capacity: float) -> float:
    if x0 <= 0 or carrying_capacity <= 0:
        raise ValueError("x0 and carrying_capacity must be positive")
    return carrying_capacity / (1.0 + ((carrying_capacity - x0) / x0) * math.exp(-growth_rate * t))

def synthetic_data() -> list[CalibrationDataPoint]:
    return [
        CalibrationDataPoint(0.0, 10.0),
        CalibrationDataPoint(2.0, 17.5),
        CalibrationDataPoint(4.0, 29.2),
        CalibrationDataPoint(6.0, 44.1),
        CalibrationDataPoint(8.0, 60.5),
        CalibrationDataPoint(10.0, 74.0),
        CalibrationDataPoint(12.0, 83.2),
    ]

def residuals(data: list[CalibrationDataPoint], growth_rate: float, carrying_capacity: float, x0: float = 10.0) -> list[ResidualRecord]:
    records: list[ResidualRecord] = []
    for point in data:
        predicted = logistic_solution(point.time, x0, growth_rate, carrying_capacity)
        residual = point.observed_value - predicted
        records.append(ResidualRecord(point.time, point.observed_value, predicted, residual, residual * residual))
    return records

def evaluate_candidate(data: list[CalibrationDataPoint], growth_rate: float, carrying_capacity: float) -> CalibrationCandidate:
    residual_records = residuals(data, growth_rate, carrying_capacity)
    loss = sum(record.squared_residual for record in residual_records)
    absolute_residuals = [abs(record.residual) for record in residual_records]
    return CalibrationCandidate(
        growth_rate=growth_rate,
        carrying_capacity=carrying_capacity,
        loss=loss,
        mean_absolute_residual=sum(absolute_residuals) / len(absolute_residuals),
        max_absolute_residual=max(absolute_residuals),
        warning="Calibration fit does not prove model validity; validation and sensitivity review remain required."
    )

def grid_search(data: list[CalibrationDataPoint]) -> list[CalibrationCandidate]:
    growth_rates = [0.22, 0.26, 0.30, 0.34, 0.38, 0.42]
    capacities = [85.0, 95.0, 105.0, 115.0, 125.0]
    candidates: list[CalibrationCandidate] = []
    for r in growth_rates:
        for k in capacities:
            candidates.append(evaluate_candidate(data, r, k))
    return sorted(candidates, key=lambda candidate: candidate.loss)

def write_outputs(output_dir: Path) -> None:
    data = synthetic_data()
    candidates = grid_search(data)
    best = candidates[0]
    best_residuals = residuals(data, best.growth_rate, best.carrying_capacity)

    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    candidate_rows = [asdict(candidate) for candidate in candidates]
    residual_rows = [asdict(record) for record in best_residuals]

    with (output_dir / "tables" / "calibration_candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(candidate_rows[0].keys()))
        writer.writeheader()
        writer.writerows(candidate_rows)

    with (output_dir / "tables" / "best_fit_residuals.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(residual_rows[0].keys()))
        writer.writeheader()
        writer.writerows(residual_rows)

    (output_dir / "json" / "calibration_candidates.json").write_text(json.dumps(candidate_rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "best_fit_residuals.json").write_text(json.dumps(residual_rows, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = [
        "# Calibration Audit",
        "",
        f"Best growth rate: {best.growth_rate}",
        f"Best carrying capacity: {best.carrying_capacity}",
        f"Best loss: {best.loss:.6f}",
        f"Mean absolute residual: {best.mean_absolute_residual:.6f}",
        f"Maximum absolute residual: {best.max_absolute_residual:.6f}",
        "",
        "Calibration fit is not validation. Residual review, sensitivity analysis, and independent testing remain required.",
    ]
    (output_dir / "reports" / "calibration_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Model calibration audit outputs generated.")

if __name__ == "__main__":
    main()
