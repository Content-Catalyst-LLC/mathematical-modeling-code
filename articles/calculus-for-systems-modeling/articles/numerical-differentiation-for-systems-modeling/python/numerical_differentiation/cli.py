from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class DifferentiationRecord:
    index: int
    x: float
    value: float
    true_derivative: float
    forward_difference: float | None
    backward_difference: float | None
    central_difference: float | None
    central_absolute_error: float | None
    step_size: float
    warning: str

def signal(x: float) -> float:
    return math.sin(x) + 0.1 * x * x

def true_derivative(x: float) -> float:
    return math.cos(x) + 0.2 * x

def forward_difference(fx: float, fx_plus_h: float, h: float) -> float:
    return (fx_plus_h - fx) / h

def backward_difference(fx: float, fx_minus_h: float, h: float) -> float:
    return (fx - fx_minus_h) / h

def central_difference(fx_plus_h: float, fx_minus_h: float, h: float) -> float:
    return (fx_plus_h - fx_minus_h) / (2 * h)

def second_central_difference(fx_plus_h: float, fx: float, fx_minus_h: float, h: float) -> float:
    return (fx_plus_h - 2 * fx + fx_minus_h) / (h * h)

def finite_difference_audit(start: float, stop: float, step_size: float) -> list[DifferentiationRecord]:
    if step_size <= 0:
        raise ValueError("step_size must be positive")
    n = int(round((stop - start) / step_size))
    xs = [start + i * step_size for i in range(n + 1)]
    values = [signal(x) for x in xs]
    records: list[DifferentiationRecord] = []

    for i, x in enumerate(xs):
        forward = None
        backward = None
        central = None
        central_error = None

        if i < len(xs) - 1:
            forward = forward_difference(values[i], values[i + 1], step_size)
        if i > 0:
            backward = backward_difference(values[i], values[i - 1], step_size)
        if 0 < i < len(xs) - 1:
            central = central_difference(values[i + 1], values[i - 1], step_size)
            central_error = abs(central - true_derivative(x))

        records.append(DifferentiationRecord(
            index=i,
            x=x,
            value=values[i],
            true_derivative=true_derivative(x),
            forward_difference=forward,
            backward_difference=backward,
            central_difference=central,
            central_absolute_error=central_error,
            step_size=step_size,
            warning="Numerical derivatives depend on step size, formula choice, boundary handling, smoothness, and noise."
        ))

    return records

def write_outputs(output_dir: Path, records: list[DifferentiationRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]
    with (output_dir / "tables" / "numerical_differentiation_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "numerical_differentiation_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "numerical_differentiation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "numerical_differentiation_summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--stop", type=float, default=10.0)
    parser.add_argument("--step-size", type=float, default=0.1)
    args = parser.parse_args()

    records = finite_difference_audit(args.start, args.stop, args.step_size)
    valid_errors = [record.central_absolute_error for record in records if record.central_absolute_error is not None]
    summary = {
        "start": args.start,
        "stop": args.stop,
        "step_size": args.step_size,
        "records": len(records),
        "mean_central_absolute_error": sum(valid_errors) / len(valid_errors),
        "max_central_absolute_error": max(valid_errors),
        "interpretation": "Central differences provide a useful derivative estimate for smooth synthetic data, but boundary and noise behavior require separate review."
    }
    write_outputs(args.output_dir, records, summary)
    print("Numerical differentiation audit complete.")

if __name__ == "__main__":
    main()
