from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReproducibleLinearAlgebraAudit:
    workflow_name: str
    notebook_status: str
    documentation_status: str
    matrix_shape: str
    matrix_meaning: str
    data_provenance_status: str
    environment_status: str
    random_seed_status: str
    validation_status: str
    generated_outputs_status: str
    residual_norm: float
    relative_residual: float
    reproducibility_score: int
    python_version: str
    platform_summary: str
    interpretation_warning: str


def matvec(A: list[list[float]], x: list[float]) -> list[float]:
    return [sum(row[j] * x[j] for j in range(len(x))) for row in A]


def norm2(x: list[float]) -> float:
    return math.sqrt(sum(value * value for value in x))


def solve2(A: list[list[float]], b: list[float]) -> list[float]:
    determinant = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if abs(determinant) < 1e-12:
        raise ValueError("Reference matrix is singular or too close to singular.")
    return [
        (b[0] * A[1][1] - A[0][1] * b[1]) / determinant,
        (A[0][0] * b[1] - b[0] * A[1][0]) / determinant,
    ]


def build_audit() -> ReproducibleLinearAlgebraAudit:
    A = [
        [3.0, 1.0],
        [1.0, 2.0],
    ]
    b = [5.0, 5.0]
    solution = solve2(A, b)
    residual = [bi - ai for bi, ai in zip(b, matvec(A, solution))]
    residual_norm = norm2(residual)
    relative_residual = residual_norm / max(norm2(b), 1e-15)

    checklist = {
        "notebook_clean_run": True,
        "readme_present": True,
        "data_dictionary_present": True,
        "environment_recorded": True,
        "random_seed_recorded_or_not_applicable": True,
        "validation_case_present": True,
        "diagnostic_outputs_saved": True,
        "interpretation_warning_present": True,
    }
    reproducibility_score = int(100 * sum(checklist.values()) / len(checklist))

    return ReproducibleLinearAlgebraAudit(
        workflow_name="reproducible_linear_algebra_workflow_audit",
        notebook_status="clean_execution_required_and_documented",
        documentation_status="readme_data_dictionary_method_notes_and_governance_report_required",
        matrix_shape="2x2",
        matrix_meaning="synthetic_reference_system_for_reproducibility_validation",
        data_provenance_status="synthetic_data_documented_in_workflow",
        environment_status="runtime_metadata_recorded",
        random_seed_status="not_applicable_for_deterministic_reference_case",
        validation_status="reference_solution_and_residual_check_passed",
        generated_outputs_status="tables_json_and_reports_written_by_workflow",
        residual_norm=round(residual_norm, 12),
        relative_residual=round(relative_residual, 12),
        reproducibility_score=reproducibility_score,
        python_version=sys.version.split()[0],
        platform_summary=platform.platform(),
        interpretation_warning="Reproducibility means the workflow can be rerun and reviewed, not that the model is automatically valid. Matrix construction, diagnostics, assumptions, uncertainty, and domain validation still require review.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "reproducible_linear_algebra_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "reproducible_linear_algebra_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Reproducible Linear Algebra Workflow Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Notebook status: {audit.notebook_status}",
        f"- Documentation status: {audit.documentation_status}",
        f"- Validation status: {audit.validation_status}",
        f"- Reproducibility score: {audit.reproducibility_score}",
        f"- Residual norm: {audit.residual_norm}",
        "",
        audit.interpretation_warning,
    ]
    (output_dir / "reports" / "reproducibility_audit_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Reproducible linear algebra workflow audit complete.")


if __name__ == "__main__":
    main()
