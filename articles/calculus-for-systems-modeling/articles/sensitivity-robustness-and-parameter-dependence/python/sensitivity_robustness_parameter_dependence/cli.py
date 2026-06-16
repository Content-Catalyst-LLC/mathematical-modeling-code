from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ParameterRecord:
    parameter_name: str
    baseline_value: float
    lower_bound: float
    upper_bound: float
    unit: str
    source_note: str

@dataclass(frozen=True)
class SensitivityRecord:
    parameter_name: str
    baseline_output: float
    low_output: float
    high_output: float
    finite_difference_sensitivity: float
    elasticity_estimate: float
    robustness_note: str
    warning: str

def logistic_final(initial_stock: float, growth_rate: float, carrying_capacity: float, horizon: float) -> float:
    return carrying_capacity / (1 + ((carrying_capacity - initial_stock) / initial_stock) * math.exp(-growth_rate * horizon))

def build_parameter_records() -> list[ParameterRecord]:
    return [
        ParameterRecord("growth_rate", 0.35, 0.20, 0.50, "per time unit", "synthetic teaching range"),
        ParameterRecord("carrying_capacity", 100.0, 75.0, 125.0, "state units", "synthetic teaching range"),
        ParameterRecord("initial_stock", 10.0, 5.0, 20.0, "state units", "synthetic teaching range"),
    ]

def evaluate_with(parameter_name: str, value: float) -> float:
    params = {"growth_rate": 0.35, "carrying_capacity": 100.0, "initial_stock": 10.0, "horizon": 20.0}
    params[parameter_name] = value
    return logistic_final(
        initial_stock=params["initial_stock"],
        growth_rate=params["growth_rate"],
        carrying_capacity=params["carrying_capacity"],
        horizon=params["horizon"],
    )

def build_sensitivity_records() -> list[SensitivityRecord]:
    records: list[SensitivityRecord] = []
    baseline_output = evaluate_with("growth_rate", 0.35)
    for parameter in build_parameter_records():
        low_output = evaluate_with(parameter.parameter_name, parameter.lower_bound)
        high_output = evaluate_with(parameter.parameter_name, parameter.upper_bound)
        sensitivity = (high_output - low_output) / (parameter.upper_bound - parameter.lower_bound)
        elasticity = sensitivity * parameter.baseline_value / baseline_output if baseline_output != 0 else float("nan")
        output_range = abs(high_output - low_output)
        robustness_note = "stable" if output_range < 10 else "sensitive"
        warning = "Conclusion may depend strongly on this parameter." if robustness_note == "sensitive" else "Output variation is limited across this synthetic range."
        records.append(
            SensitivityRecord(
                parameter_name=parameter.parameter_name,
                baseline_output=baseline_output,
                low_output=low_output,
                high_output=high_output,
                finite_difference_sensitivity=sensitivity,
                elasticity_estimate=elasticity,
                robustness_note=robustness_note,
                warning=warning,
            )
        )
    return records

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

    parameters = build_parameter_records()
    sensitivities = build_sensitivity_records()

    write_csv(output_dir / "tables" / "parameter_records.csv", parameters)
    write_csv(output_dir / "tables" / "sensitivity_records.csv", sensitivities)

    audit = {
        "parameters": [asdict(record) for record in parameters],
        "sensitivities": [asdict(record) for record in sensitivities],
        "interpretation_warning": "Sensitivity analysis supports model review but does not prove model validity.",
    }
    (output_dir / "json" / "sensitivity_robustness_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Sensitivity and Robustness Audit", "", "## Parameter Records"]
    for record in parameters:
        report_lines.append(f"- **{record.parameter_name}** = {record.baseline_value} {record.unit}; range: {record.lower_bound} to {record.upper_bound}; source: {record.source_note}")
    report_lines.extend(["", "## Sensitivity Records"])
    for record in sensitivities:
        report_lines.append(f"- **{record.parameter_name}**: sensitivity {record.finite_difference_sensitivity:.6f}; elasticity {record.elasticity_estimate:.6f}; status: {record.robustness_note}. {record.warning}")
    report_lines.extend(["", "Sensitivity analysis supports model review but does not prove model validity."])

    (output_dir / "reports" / "sensitivity_robustness_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Sensitivity and robustness audit outputs generated.")

if __name__ == "__main__":
    main()
