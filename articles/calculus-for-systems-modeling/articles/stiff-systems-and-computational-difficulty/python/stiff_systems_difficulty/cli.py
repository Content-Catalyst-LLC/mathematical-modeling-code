from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class StiffnessAuditRecord:
    step_size: float
    eigenvalue: float
    method: str
    amplification_factor: float
    stability_status: str
    final_value: float
    exact_final_value: float
    absolute_error: float
    warning: str

def exact_solution(t: float, y0: float, eigenvalue: float) -> float:
    return y0 * math.exp(eigenvalue * t)

def explicit_euler(y0: float, eigenvalue: float, h: float, stop_time: float) -> tuple[float, float]:
    if h <= 0:
        raise ValueError("step size must be positive")
    steps = int(round(stop_time / h))
    amplification = 1.0 + h * eigenvalue
    y = y0
    for _ in range(steps):
        y = amplification * y
    return y, abs(amplification)

def implicit_euler(y0: float, eigenvalue: float, h: float, stop_time: float) -> tuple[float, float]:
    if h <= 0:
        raise ValueError("step size must be positive")
    steps = int(round(stop_time / h))
    amplification = 1.0 / (1.0 - h * eigenvalue)
    y = y0
    for _ in range(steps):
        y = amplification * y
    return y, abs(amplification)

def stiffness_audit(y0: float = 1.0, eigenvalue: float = -50.0, stop_time: float = 1.0) -> list[StiffnessAuditRecord]:
    exact_final = exact_solution(stop_time, y0, eigenvalue)
    step_sizes = [0.1, 0.05, 0.025, 0.01]
    records: list[StiffnessAuditRecord] = []

    for h in step_sizes:
        explicit_value, explicit_amp = explicit_euler(y0, eigenvalue, h, stop_time)
        implicit_value, implicit_amp = implicit_euler(y0, eigenvalue, h, stop_time)

        records.append(StiffnessAuditRecord(
            step_size=h,
            eigenvalue=eigenvalue,
            method="explicit_euler",
            amplification_factor=explicit_amp,
            stability_status="stable_for_test_problem" if explicit_amp <= 1 else "unstable_for_test_problem",
            final_value=explicit_value,
            exact_final_value=exact_final,
            absolute_error=abs(explicit_value - exact_final),
            warning="Explicit methods may require very small steps on stiff systems."
        ))

        records.append(StiffnessAuditRecord(
            step_size=h,
            eigenvalue=eigenvalue,
            method="implicit_euler",
            amplification_factor=implicit_amp,
            stability_status="stable_for_test_problem" if implicit_amp <= 1 else "unstable_for_test_problem",
            final_value=implicit_value,
            exact_final_value=exact_final,
            absolute_error=abs(implicit_value - exact_final),
            warning="Implicit stability does not remove the need for accuracy and interpretation review."
        ))

    return records

def stiffness_ratio(eigenvalues: list[float]) -> float:
    magnitudes = [abs(v) for v in eigenvalues if abs(v) > 0]
    if not magnitudes:
        raise ValueError("at least one nonzero eigenvalue is required")
    return max(magnitudes) / min(magnitudes)

def write_outputs(output_dir: Path, records: list[StiffnessAuditRecord]) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    rows = [asdict(record) for record in records]

    with (output_dir / "tables" / "stiffness_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    (output_dir / "json" / "stiffness_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = [
        "# Stiffness Diagnostic Audit",
        "",
        "| Step size | Method | Amplification factor | Status | Absolute error |",
        "|---:|---|---:|---|---:|",
    ]
    for record in records:
        report_lines.append(f"| {record.step_size} | {record.method} | {record.amplification_factor:.6f} | {record.stability_status} | {record.absolute_error:.12e} |")
    report_lines.append("")
    report_lines.append("Stiffness diagnostics support numerical review, not empirical validation.")
    (output_dir / "reports" / "stiffness_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    records = stiffness_audit()
    write_outputs(args.output_dir, records)
    print("Stiff systems diagnostic audit outputs generated.")

if __name__ == "__main__":
    main()
