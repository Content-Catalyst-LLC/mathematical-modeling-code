from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScalingNormalizationAudit:
    workflow_name: str
    matrix_shape: str
    row_meaning: str
    column_meaning: str
    raw_column_norm_1: float
    raw_column_norm_2: float
    standardized_column_norm_1: float
    standardized_column_norm_2: float
    minmax_column_min_1: float
    minmax_column_max_1: float
    first_row_sum_after_row_normalization: float
    first_row_norm_after_unit_normalization: float
    raw_condition_proxy: float
    standardized_condition_proxy: float
    comparison_warning: str
    interpretation_warning: str


def column(A: list[list[float]], j: int) -> list[float]:
    return [row[j] for row in A]


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def std(values: list[float]) -> float:
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / len(values))


def norm2(values: list[float]) -> float:
    return math.sqrt(sum(x * x for x in values))


def transpose(A: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*A)]


def standardize_columns(A: list[list[float]]) -> list[list[float]]:
    cols = transpose(A)
    means = [mean(col) for col in cols]
    stds = [std(col) or 1.0 for col in cols]
    return [[(row[j] - means[j]) / stds[j] for j in range(len(row))] for row in A]


def minmax_columns(A: list[list[float]]) -> list[list[float]]:
    cols = transpose(A)
    mins = [min(col) for col in cols]
    maxs = [max(col) for col in cols]
    ranges = [(maxs[j] - mins[j]) or 1.0 for j in range(len(cols))]
    return [[(row[j] - mins[j]) / ranges[j] for j in range(len(row))] for row in A]


def row_sum_normalize(A: list[list[float]]) -> list[list[float]]:
    normalized = []
    for row in A:
        total = sum(row) or 1.0
        normalized.append([x / total for x in row])
    return normalized


def unit_row_normalize(A: list[list[float]]) -> list[list[float]]:
    normalized = []
    for row in A:
        length = norm2(row) or 1.0
        normalized.append([x / length for x in row])
    return normalized


def condition_proxy(A: list[list[float]]) -> float:
    column_norms = [norm2(column(A, j)) for j in range(len(A[0]))]
    return max(column_norms) / max(min(column_norms), 1e-15)


def build_audit() -> ScalingNormalizationAudit:
    A_raw = [
        [1200.0, 0.08],
        [1800.0, 0.15],
        [900.0, 0.04],
    ]
    A_standardized = standardize_columns(A_raw)
    A_minmax = minmax_columns(A_raw)
    A_row_sum = row_sum_normalize(A_raw)
    A_unit_rows = unit_row_normalize(A_raw)

    return ScalingNormalizationAudit(
        workflow_name="scaling_normalization_audit",
        matrix_shape="3x2",
        row_meaning="infrastructure_zones",
        column_meaning="annual_demand_and_outage_exposure",
        raw_column_norm_1=round(norm2(column(A_raw, 0)), 12),
        raw_column_norm_2=round(norm2(column(A_raw, 1)), 12),
        standardized_column_norm_1=round(norm2(column(A_standardized, 0)), 12),
        standardized_column_norm_2=round(norm2(column(A_standardized, 1)), 12),
        minmax_column_min_1=round(min(column(A_minmax, 0)), 12),
        minmax_column_max_1=round(max(column(A_minmax, 0)), 12),
        first_row_sum_after_row_normalization=round(sum(A_row_sum[0]), 12),
        first_row_norm_after_unit_normalization=round(norm2(A_unit_rows[0]), 12),
        raw_condition_proxy=round(condition_proxy(A_raw), 12),
        standardized_condition_proxy=round(condition_proxy(A_standardized), 12),
        comparison_warning="Raw units compare magnitude; standardized columns compare relative position; row normalization compares composition; unit-vector normalization compares direction.",
        interpretation_warning="Scaling and normalization change what comparison means. Every transformed matrix should record original units, transformation rule, purpose, and interpretation limits.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "scaling_normalization_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "scaling_normalization_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Scaling and Normalization Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Matrix shape: {audit.matrix_shape}",
        f"- Raw column norm 1: {audit.raw_column_norm_1}",
        f"- Raw column norm 2: {audit.raw_column_norm_2}",
        f"- Standardized column norm 1: {audit.standardized_column_norm_1}",
        f"- Standardized column norm 2: {audit.standardized_column_norm_2}",
        f"- Raw condition proxy: {audit.raw_condition_proxy}",
        f"- Standardized condition proxy: {audit.standardized_condition_proxy}",
        "",
        audit.comparison_warning,
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "scaling_normalization_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Scaling and normalization audit complete.")


if __name__ == "__main__":
    main()
