#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

@dataclass
class CalculatorResult:
    calculator: str
    inputs: dict
    result: dict
    interpretation: str
    warning: str = ""

def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def write_outputs(name: str, payload: CalculatorResult) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(asdict(payload), indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload.calculator, "interpretation": payload.interpretation, "warning": payload.warning}
    flat.update({f"input_{k}": v for k, v in payload.inputs.items() if not isinstance(v, list)})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, (list, dict))})
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def risk_label(score: int) -> str:
    return "high" if score >= 3 else "moderate" if score >= 1 else "low"

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("purpose-fit")
    p.add_argument("--teaching", type=int, default=1)
    p.add_argument("--exploratory", type=int, default=0)
    p.add_argument("--predictive", type=int, default=0)
    p.add_argument("--decision-support", type=int, default=0)

    p = sub.add_parser("assumption-risk")
    p.add_argument("--hidden-assumptions", type=int, default=2)
    p.add_argument("--normative-assumptions", type=int, default=1)
    p.add_argument("--solver-undocumented", type=int, default=1)

    p = sub.add_parser("claim-boundary")
    p.add_argument("--purpose", default="predictive")
    p.add_argument("--validated", type=int, default=0)
    p.add_argument("--uncertainty-recorded", type=int, default=1)
    p.add_argument("--scope-recorded", type=int, default=1)

    p = sub.add_parser("parameter-evidence")
    p.add_argument("--has-unit", type=int, default=1)
    p.add_argument("--has-source", type=int, default=1)
    p.add_argument("--has-range", type=int, default=0)
    p.add_argument("--has-uncertainty", type=int, default=0)

    p = sub.add_parser("communication-risk")
    p.add_argument("--overprecision", type=int, default=1)
    p.add_argument("--scenario-confusion", type=int, default=1)
    p.add_argument("--hidden-values", type=int, default=0)
    p.add_argument("--audience-mismatch", type=int, default=1)

    p = sub.add_parser("responsibility-warning")
    p.add_argument("--pattern", default="claim_boundary")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "purpose-fit":
        active = args.teaching + args.exploratory + args.predictive + args.decision_support
        status = "single_purpose" if active == 1 else "mixed_purpose" if active > 1 else "undefined_purpose"
        emit(cmd, args, {"active_purpose_count": active, "status": status}, "Checks whether model purpose is clear or mixed.", "A model should not be used for claims outside its stated purpose.")
    elif cmd == "assumption-risk":
        score = args.hidden_assumptions + args.normative_assumptions + args.solver_undocumented
        emit(cmd, args, {"risk_score": score, "risk": risk_label(score)}, "Scores risk from hidden assumptions, normative choices, and undocumented solver settings.", "Hidden assumptions can create false confidence.")
    elif cmd == "claim-boundary":
        support_score = args.validated + args.uncertainty_recorded + args.scope_recorded
        allowed = support_score >= 2 and (args.purpose != "predictive" or args.validated == 1)
        emit(cmd, args, {"support_score": support_score, "claim_supported": allowed}, "Checks whether a claim has validation, uncertainty, and scope support.", "Model conclusions should not exceed evidence, scope, and purpose.")
    elif cmd == "parameter-evidence":
        score = args.has_unit + args.has_source + args.has_range + args.has_uncertainty
        status = "complete" if score == 4 else "partial" if score >= 2 else "weak"
        emit(cmd, args, {"evidence_score": score, "status": status}, "Scores whether a parameter record includes unit, source, range, and uncertainty.", "A parameter value without evidence status is incomplete.")
    elif cmd == "communication-risk":
        score = args.overprecision + args.scenario_confusion + args.hidden_values + args.audience_mismatch
        emit(cmd, args, {"risk_score": score, "risk": risk_label(score)}, "Scores risk of model-output miscommunication.", "A model result can be technically correct and still miscommunicated.")
    elif cmd == "responsibility-warning":
        notes = {
            "purpose": "A model should not be used for claims outside its stated purpose.",
            "assumptions": "Hidden assumptions can create false confidence.",
            "parameter": "A parameter value without evidence status is incomplete.",
            "validation": "Validation is purpose-specific, not universal.",
            "communication": "A model result can be technically correct and still miscommunicated.",
            "claim_boundary": "Model conclusions should not exceed evidence, scope, and purpose."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document purpose, assumptions, evidence, and claim boundaries.")}, "Creates a responsible modeling warning.", "Mathematical modeling is responsible only when purpose, assumptions, evidence, uncertainty, and claim boundaries are documented.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
