from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class IntegrationRecord:
    index: int
    time: float
    rate: float
    left_cumulative: float
    trapezoid_cumulative: float
    true_cumulative: float
    trapezoid_absolute_error: float
    step_size: float
    warning: str

def rate_function(t: float) -> float:
    return 2.0 + math.sin(t) + 0.1 * t

def true_integral(t: float) -> float:
    return 2.0 * t - math.cos(t) + 1.0 + 0.05 * t * t

def left_rectangle_step(rate_left: float, h: float) -> float:
    return rate_left * h

def trapezoid_step(rate_left: float, rate_right: float, h: float) -> float:
    return 0.5 * (rate_left + rate_right) * h

def simpson_one_third(f0: float, f1: float, f2: float, h: float) -> float:
    return (h / 3.0) * (f0 + 4.0 * f1 + f2)

def numerical_integration_audit(start: float, stop: float, step_size: float) -> list[IntegrationRecord]:
    n = int(round((stop - start) / step_size))
    times = [start + i * step_size for i in range(n + 1)]
    rates = [rate_function(t) for t in times]
    left_total = 0.0
    trapezoid_total = 0.0
    records = []
    for i, t in enumerate(times):
        if i > 0:
            left_total += left_rectangle_step(rates[i - 1], step_size)
            trapezoid_total += trapezoid_step(rates[i - 1], rates[i], step_size)
        true_total = true_integral(t) - true_integral(start)
        records.append(IntegrationRecord(i, t, rates[i], left_total, trapezoid_total, true_total, abs(trapezoid_total - true_total), step_size, "Numerical integration depends on spacing, integration rule, data quality, boundary endpoints, and missing-value handling."))
    return records

def write_outputs(output_dir: Path, records: list[IntegrationRecord], summary: dict) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(r) for r in records]
    with (output_dir / "tables" / "numerical_integration_audit.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "numerical_integration_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "numerical_integration_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir / "tables" / "numerical_integration_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--stop", type=float, default=10.0)
    parser.add_argument("--step-size", type=float, default=0.1)
    args = parser.parse_args()
    records = numerical_integration_audit(args.start, args.stop, args.step_size)
    summary = {
        "start": args.start,
        "stop": args.stop,
        "step_size": args.step_size,
        "records": len(records),
        "final_left_cumulative": records[-1].left_cumulative,
        "final_trapezoid_cumulative": records[-1].trapezoid_cumulative,
        "final_true_cumulative": records[-1].true_cumulative,
        "final_trapezoid_absolute_error": records[-1].trapezoid_absolute_error,
        "interpretation": "The trapezoidal rule estimates cumulative total from sampled rates while preserving an audit trail of error against a synthetic benchmark."
    }
    write_outputs(args.output_dir, records, summary)
    print("Numerical integration audit complete.")

if __name__ == "__main__":
    main()
