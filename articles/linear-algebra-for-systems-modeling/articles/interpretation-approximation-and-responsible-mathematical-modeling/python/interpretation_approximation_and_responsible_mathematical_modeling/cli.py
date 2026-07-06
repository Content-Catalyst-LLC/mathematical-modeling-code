from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ResponsibleModelingAudit:
    workflow_name: str
    model_purpose: str
    claim_type: str
    approximation_form: str
    representation_status: str
    numerical_status: str
    diagnostic_status: str
    validation_status: str
    uncertainty_sources: str
    sensitivity_status: str
    interpretation_boundary: str
    governance_warning: str
    responsible_use_statement: str


def build_audit() -> ResponsibleModelingAudit:
    return ResponsibleModelingAudit(
        workflow_name="responsible_modeling_audit",
        model_purpose="interpret_linear_algebra_output_for_systems_modeling",
        claim_type="exploratory_decision_support_not_causal_proof",
        approximation_form="linear_or_low_rank_approximation_with_explicit_assumptions",
        representation_status="rows_columns_units_zeros_scaling_and_boundaries_documented",
        numerical_status="residuals_conditioning_solver_tolerance_and_reproducibility_checked",
        diagnostic_status="residuals_sensitivity_and_alternative_representations_reviewed",
        validation_status="validated_only_for_stated_data_range_operating_context_and_model_purpose",
        uncertainty_sources="data_uncertainty_model_uncertainty_numerical_uncertainty_interpretive_uncertainty",
        sensitivity_status="conclusions_compared_across_reasonable_representation_scaling_and_model_form_variants",
        interpretation_boundary="Outputs support structured interpretation within the stated assumptions, not universal claims, causal proof, or unreviewed decision authority.",
        governance_warning="Model use requires documented assumptions, validation evidence, review status, uncertainty communication, and stop-use conditions.",
        responsible_use_statement="Use the model as an interpretive and diagnostic aid. Do not use it as the sole basis for high-stakes decisions without domain review, uncertainty disclosure, and accountability.",
    )


def write_outputs(output_dir: Path) -> None:
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    audit = build_audit()
    row = asdict(audit)

    with (output_dir / "tables" / "responsible_modeling_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)

    (output_dir / "json" / "responsible_modeling_audit.json").write_text(
        json.dumps(row, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report = [
        "# Responsible Modeling Audit",
        "",
        f"- Workflow: {audit.workflow_name}",
        f"- Model purpose: {audit.model_purpose}",
        f"- Claim type: {audit.claim_type}",
        f"- Approximation form: {audit.approximation_form}",
        f"- Representation status: {audit.representation_status}",
        f"- Numerical status: {audit.numerical_status}",
        f"- Diagnostic status: {audit.diagnostic_status}",
        f"- Validation status: {audit.validation_status}",
        f"- Uncertainty sources: {audit.uncertainty_sources}",
        f"- Sensitivity status: {audit.sensitivity_status}",
        "",
        f"**Interpretation boundary:** {audit.interpretation_boundary}",
        "",
        f"**Governance warning:** {audit.governance_warning}",
        "",
        f"**Responsible use statement:** {audit.responsible_use_statement}",
    ]
    (output_dir / "reports" / "responsible_modeling_audit.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Responsible modeling audit complete.")


if __name__ == "__main__":
    main()
