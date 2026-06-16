from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class PurposeRecord:
    model_name: str
    purpose_type: str
    supported_use: str
    unsupported_use: str
    warning: str

@dataclass(frozen=True)
class AssumptionRecord:
    assumption_name: str
    assumption_type: str
    description: str
    evidence_status: str
    risk_if_hidden: str

@dataclass(frozen=True)
class ClaimBoundaryRecord:
    claim_type: str
    permitted_claim: str
    prohibited_claim: str
    required_evidence: str
    governance_status: str

def build_purpose_records() -> list[PurposeRecord]:
    return [
        PurposeRecord("synthetic_logistic_growth", "teaching", "illustrates growth, saturation, and carrying capacity", "empirical forecast for a real population", "Synthetic teaching models should not be communicated as empirical evidence."),
        PurposeRecord("scenario_sweep", "exploratory", "compares behavior across plausible parameter scenarios", "single-point prediction", "Scenario outputs should not be confused with forecasts."),
        PurposeRecord("decision_support_model", "decision support", "frames tradeoffs under documented assumptions", "replacement for judgment or accountability", "Models inform decisions; they do not remove responsibility from decision makers."),
    ]

def build_assumption_records() -> list[AssumptionRecord]:
    return [
        AssumptionRecord("continuous_growth", "mathematical", "state changes continuously over modeled time", "teaching assumption", "smooth model may hide shocks, thresholds, or discrete events"),
        AssumptionRecord("fixed_parameter_values", "empirical", "parameters remain fixed across the scenario", "synthetic assumption", "output appears more certain than parameter evidence supports"),
        AssumptionRecord("solver_configuration", "computational", "numerical method and tolerance are adequate for the model", "requires diagnostic record", "numerical artifact may appear as model insight"),
        AssumptionRecord("objective_function_weights", "normative", "optimization weights reflect a chosen priority structure", "requires stakeholder and governance review", "value judgments are hidden inside mathematics"),
    ]

def build_claim_boundary_records() -> list[ClaimBoundaryRecord]:
    return [
        ClaimBoundaryRecord("descriptive", "the model summarizes a specified structure or dataset", "the model proves a mechanism", "definition of variables, data source, and scope", "active"),
        ClaimBoundaryRecord("mechanistic", "the model represents a plausible process under stated assumptions", "the mechanism is proven solely by formal structure", "process evidence, parameter interpretation, and sensitivity review", "review"),
        ClaimBoundaryRecord("predictive", "the model forecasts within validated domain and time horizon", "the model predicts outside validation scope", "validation data, uncertainty, and robustness analysis", "review"),
        ClaimBoundaryRecord("decision_support", "the model frames tradeoffs under documented assumptions", "the model replaces judgment or accountability", "stakeholder review, uncertainty, and claim boundaries", "review"),
    ]

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

    purposes = build_purpose_records()
    assumptions = build_assumption_records()
    claim_boundaries = build_claim_boundary_records()

    write_csv(output_dir / "tables" / "purpose_records.csv", purposes)
    write_csv(output_dir / "tables" / "assumption_records.csv", assumptions)
    write_csv(output_dir / "tables" / "claim_boundary_records.csv", claim_boundaries)

    audit = {
        "purpose_records": [asdict(record) for record in purposes],
        "assumption_records": [asdict(record) for record in assumptions],
        "claim_boundary_records": [asdict(record) for record in claim_boundaries],
        "interpretation_warning": "Mathematical modeling is responsible only when purpose, assumptions, evidence, uncertainty, and claim boundaries are documented.",
    }
    (output_dir / "json" / "responsible_modeling_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Responsible Mathematical Modeling Audit", "", "## Purpose Records"]
    for record in purposes:
        report_lines.append(f"- **{record.model_name}** ({record.purpose_type}): supports {record.supported_use}; does not support {record.unsupported_use}. {record.warning}")
    report_lines.extend(["", "## Assumption Records"])
    for record in assumptions:
        report_lines.append(f"- **{record.assumption_name}** ({record.assumption_type}): {record.description}. Evidence: {record.evidence_status}. Risk if hidden: {record.risk_if_hidden}.")
    report_lines.extend(["", "## Claim Boundary Records"])
    for record in claim_boundaries:
        report_lines.append(f"- **{record.claim_type}**: permitted: {record.permitted_claim}; prohibited: {record.prohibited_claim}; status: {record.governance_status}.")
    report_lines.extend(["", "Mathematical modeling is responsible only when purpose, assumptions, evidence, uncertainty, and claim boundaries are documented."])

    (output_dir / "reports" / "responsible_modeling_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Responsible modeling audit outputs generated.")

if __name__ == "__main__":
    main()
