from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class WorkflowArtifact:
    artifact_name: str
    artifact_type: str
    path: str
    source_or_generated: str
    review_role: str
    warning: str

@dataclass(frozen=True)
class RunRecord:
    workflow_name: str
    command: str
    expected_outputs: int
    diagnostic_status: str
    review_required: bool
    interpretation_warning: str

def build_artifacts() -> list[WorkflowArtifact]:
    return [
        WorkflowArtifact("parameter_records", "csv", "data/parameter_records.csv", "source", "documents parameter names, values, units, sources, and ranges", "Parameter records do not prove empirical correctness."),
        WorkflowArtifact("model_outputs", "csv", "outputs/tables/model_outputs.csv", "generated", "stores computed trajectory or summary outputs", "Generated outputs require diagnostics and interpretation limits."),
        WorkflowArtifact("diagnostics", "json", "outputs/json/diagnostics.json", "generated", "records validation, convergence, and warning status", "Diagnostics should remain attached to interpretation."),
        WorkflowArtifact("governance_queue", "markdown", "outputs/reports/governance_queue.md", "generated", "collects warnings requiring human review", "Governance queues support judgment but do not replace it."),
        WorkflowArtifact("notebook_placeholder", "ipynb", "notebooks/reproducible_calculus_workflows_walkthrough.ipynb", "source", "documents exploratory computational pathway", "Notebook state can drift; clean reruns are needed."),
        WorkflowArtifact("r_markdown_report", "Rmd", "rmarkdown/reproducible_calculus_workflow.Rmd", "source", "keeps executable prose and code together", "Rendered reports should be regenerated from source."),
    ]

def build_run_record(artifacts: list[WorkflowArtifact]) -> RunRecord:
    review_required = any("warning" in artifact.warning.lower() or "not" in artifact.warning.lower() for artifact in artifacts)
    return RunRecord(
        workflow_name="reproducible_calculus_workflow",
        command="make smoke",
        expected_outputs=len(artifacts),
        diagnostic_status="review_required" if review_required else "converged",
        review_required=review_required,
        interpretation_warning="Reproducibility supports auditability but does not prove model validity.",
    )

def write_outputs(output_dir: Path) -> None:
    artifacts = build_artifacts()
    run_record = build_run_record(artifacts)

    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    artifact_rows = [asdict(artifact) for artifact in artifacts]

    with (output_dir / "tables" / "workflow_artifacts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(artifact_rows[0].keys()))
        writer.writeheader()
        writer.writerows(artifact_rows)

    with (output_dir / "tables" / "workflow_run_record.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(run_record).keys()))
        writer.writeheader()
        writer.writerow(asdict(run_record))

    (output_dir / "json" / "workflow_artifacts.json").write_text(json.dumps(artifact_rows, indent=2, sort_keys=True), encoding="utf-8")
    (output_dir / "json" / "workflow_run_record.json").write_text(json.dumps(asdict(run_record), indent=2, sort_keys=True), encoding="utf-8")

    report_lines = [
        "# Reproducibility Audit",
        "",
        f"Workflow: {run_record.workflow_name}",
        f"Command: `{run_record.command}`",
        f"Diagnostic status: {run_record.diagnostic_status}",
        "",
        "## Artifacts",
    ]
    for artifact in artifacts:
        report_lines.append(f"- **{artifact.artifact_name}** ({artifact.artifact_type}): {artifact.review_role}. {artifact.warning}")
    report_lines.append("")
    report_lines.append(run_record.interpretation_warning)

    (output_dir / "reports" / "reproducibility_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Reproducibility audit outputs generated.")

if __name__ == "__main__":
    main()
