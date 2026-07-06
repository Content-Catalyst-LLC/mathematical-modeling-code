from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepresentationAssumptionAudit:
    workflow_name: str
    matrix_shape: str
    row_meaning: str
    column_meaning: str
    value_meaning: str
    zero_meaning: str
    missing_value_rule: str
    raw_column_norm_1: float
    raw_column_norm_2: float
    standardized_column_norm_1: float
    standardized_column_norm_2: float
    representation_change_warning: str
    interpretation_warning: str


def column(values: list[list[float]], index: int) -> list[float]:
    return [row[index] for row in values]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def std(values: list[float]) -> float:
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def norm2(values: list[float]) -> float:
    return math.sqrt(sum(x * x for x in values))


def standardize_matrix(A: list[list[float]]) -> list[list[float]]:
    cols = list(zip(*A))
    means = [mean(list(col)) for col in cols]
    stds = [std(list(col)) or 1.0 for col in cols]
    return [[(row[j] - means[j]) / stds[j] for j in range(len(row))] for row in A]


def build_audit() -> RepresentationAssumptionAudit:
    A_raw = [
        [1200.0, 0.08],
        [1800.0, 0.15],
        [900.0, 0.04],
    ]
    A_standardized = standardize_matrix(A_raw)

    return RepresentationAssumptionAudit(
        workflow_name="representation_assumption_audit",
        matrix_shape="3x2",
        row_meaning="infrastructure_zones",
        column_meaning="annual_demand_and_outage_exposure",
        value_meaning="mixed_units_before_standardization",
        zero_meaning="zero_would_mean_measured_absence_not_missingness",
        missing_value_rule="missing_values_must_not_be_encoded_as_zero_without_flag",
        raw_column_norm_1=round(norm2(column(A_raw, 0)), 12),
        raw_column_norm_2=round(norm2(column(A_raw, 1)), 12),
        standardized_column_norm_1=round(norm2(column(A_standardized, 0)), 12),
        standardized_column_norm_2=round(norm2(column(A_standardized, 1)), 12),
        representation_change_warning="Standardization improves comparability but changes interpretation from original units to relative position.",
        interpretation_warning="Representation choices define what the model can compare, reveal, and hide. Rows, columns, units, zeros, scaling, missingness, and boundaries should be documented before computation.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "representation_assumption_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "representation_assumption_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Representation Assumption Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Matrix shape: {audit.matrix_shape}",
        f"- Row meaning: {audit.row_meaning}",
        f"- Column meaning: {audit.column_meaning}",
        f"- Value meaning: {audit.value_meaning}",
        f"- Zero meaning: {audit.zero_meaning}",
        f"- Representation warning: {audit.representation_change_warning}",
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "representation_assumption_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Representation assumption audit complete.")


if __name__ == "__main__":
    main()
