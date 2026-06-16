from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class MechanismRecord:
    mechanism_name: str
    represented_process: str
    entities: str
    activities: str
    evidence_status: str
    warning: str

@dataclass(frozen=True)
class FormalRepresentationRecord:
    formal_element: str
    symbol_or_structure: str
    model_role: str
    interpretation_requirement: str
    warning: str

@dataclass(frozen=True)
class ExplanationClaimRecord:
    claim_type: str
    supported_use: str
    evidence_need: str
    scope_limit: str
    governance_status: str

def build_mechanism_records() -> list[MechanismRecord]:
    return [
        MechanismRecord("stock_flow_accumulation", "stock changes through inflow and outflow", "stock, inflow, outflow", "accumulation, depletion, replacement", "synthetic teaching example", "A stock-flow equation is mechanistic only when flows represent real processes."),
        MechanismRecord("balancing_feedback", "state-dependent adjustment limits growth or change", "state variable, feedback coefficient, constraint", "adjustment, saturation, stabilization", "formal teaching example", "Feedback parameters require process interpretation and evidence."),
        MechanismRecord("threshold_transition", "behavior changes after a critical value is crossed", "state variable, threshold, response rule", "activation, failure, transition", "scenario-based example", "Threshold claims require careful scope and uncertainty notes."),
    ]

def build_formal_records() -> list[FormalRepresentationRecord]:
    return [
        FormalRepresentationRecord("differential_equation", "dx/dt = f(x,t,theta)", "describes state change over time", "identify what process f represents", "A rate equation without process interpretation may be descriptive only."),
        FormalRepresentationRecord("parameter", "theta", "controls model behavior", "record unit, source, range, and mechanism meaning", "Calibrated parameters are not automatically causal quantities."),
        FormalRepresentationRecord("constraint", "x <= K", "bounds system behavior", "explain whether K is physical, institutional, ecological, or assumed", "Constraints can hide strong assumptions."),
    ]

def build_claim_records() -> list[ExplanationClaimRecord]:
    return [
        ExplanationClaimRecord("mechanistic", "explains how an organized process can produce behavior", "process evidence, structural plausibility, sensitivity review", "applies only where the mechanism and assumptions hold", "review"),
        ExplanationClaimRecord("predictive", "forecasts output under specified conditions", "validation data and uncertainty assessment", "limited to validated domain and time horizon", "review"),
        ExplanationClaimRecord("exploratory", "investigates possible system behavior", "clear scenario assumptions and limitation notes", "not a confirmed mechanism or forecast", "active"),
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

    mechanisms = build_mechanism_records()
    formal_records = build_formal_records()
    claims = build_claim_records()

    write_csv(output_dir / "tables" / "mechanism_records.csv", mechanisms)
    write_csv(output_dir / "tables" / "formal_representation_records.csv", formal_records)
    write_csv(output_dir / "tables" / "explanation_claim_records.csv", claims)

    audit = {
        "mechanism_records": [asdict(record) for record in mechanisms],
        "formal_representation_records": [asdict(record) for record in formal_records],
        "explanation_claim_records": [asdict(record) for record in claims],
        "interpretation_warning": "Formal structure supports explanation only when mechanism, evidence, and scope are documented.",
    }
    (output_dir / "json" / "mechanism_formalism_audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")

    report_lines = ["# Mechanism and Formalism Audit", "", "## Mechanism Records"]
    for record in mechanisms:
        report_lines.append(f"- **{record.mechanism_name}**: {record.represented_process}. Evidence: {record.evidence_status}. {record.warning}")
    report_lines.extend(["", "## Formal Representation Records"])
    for record in formal_records:
        report_lines.append(f"- **{record.formal_element}** ({record.symbol_or_structure}): {record.model_role}. Requirement: {record.interpretation_requirement}. {record.warning}")
    report_lines.extend(["", "## Explanation Claim Records"])
    for record in claims:
        report_lines.append(f"- **{record.claim_type}**: {record.supported_use}. Scope: {record.scope_limit}. Status: {record.governance_status}.")
    report_lines.extend(["", "Formal structure supports explanation only when mechanism, evidence, and scope are documented."])

    (output_dir / "reports" / "mechanism_formalism_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Mechanism and formalism audit outputs generated.")

if __name__ == "__main__":
    main()
