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

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("mechanism-score")
    p.add_argument("--entities", type=int, default=1)
    p.add_argument("--activities", type=int, default=1)
    p.add_argument("--relations", type=int, default=1)
    p.add_argument("--evidence", type=int, default=0)
    p.add_argument("--scope", type=int, default=1)

    p = sub.add_parser("formalism-risk")
    p.add_argument("--parameter-meaning", type=int, default=0)
    p.add_argument("--evidence-link", type=int, default=0)
    p.add_argument("--validation-scope", type=int, default=1)
    p.add_argument("--claim-boundary", type=int, default=0)

    p = sub.add_parser("claim-type")
    p.add_argument("--mechanism-evidence", type=int, default=1)
    p.add_argument("--validation-data", type=int, default=0)
    p.add_argument("--scenario-only", type=int, default=0)

    p = sub.add_parser("parameter-interpretation")
    p.add_argument("--source", default="calibrated")
    p.add_argument("--has-unit", type=int, default=1)
    p.add_argument("--has-range", type=int, default=1)

    p = sub.add_parser("black-box-risk")
    p.add_argument("--opaque-steps", type=int, default=2)
    p.add_argument("--hidden-parameters", type=int, default=1)
    p.add_argument("--missing-diagnostics", type=int, default=1)

    p = sub.add_parser("explanation-warning")
    p.add_argument("--pattern", default="formal_precision")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "mechanism-score":
        total = args.entities + args.activities + args.relations + args.evidence + args.scope
        score = int(round(100 * total / 5))
        status = "strong" if score >= 80 else "partial" if score >= 50 else "weak"
        emit(cmd, args, {"score": score, "status": status}, "Scores whether a mechanism record contains parts, activities, relations, evidence, and scope.", "A score is a review aid, not proof of explanatory validity.")
    elif cmd == "formalism-risk":
        missing = 4 - (args.parameter_meaning + args.evidence_link + args.validation_scope + args.claim_boundary)
        risk = "high" if missing >= 3 else "moderate" if missing >= 1 else "low"
        emit(cmd, args, {"missing_items": missing, "risk": risk}, "Flags risk when formal models lack interpretation, evidence, validation scope, or claim boundaries.", "Formal consistency does not guarantee explanatory validity.")
    elif cmd == "claim-type":
        if args.scenario_only:
            claim = "exploratory"
        elif args.mechanism_evidence and args.validation_data:
            claim = "mechanistic_and_predictive"
        elif args.mechanism_evidence:
            claim = "mechanistic_candidate"
        elif args.validation_data:
            claim = "predictive"
        else:
            claim = "descriptive"
        emit(cmd, args, {"claim_type": claim}, "Classifies the kind of claim supported by evidence status.", "Do not treat exploratory output as confirmed mechanism.")
    elif cmd == "parameter-interpretation":
        complete = bool(args.has_unit and args.has_range)
        causal_caution = args.source in {"calibrated", "synthetic", "scenario"}
        emit(cmd, args, {"complete_record": complete, "causal_caution": causal_caution}, "Checks whether a parameter record has minimum interpretive support.", "Calibrated, synthetic, or scenario parameters are not automatically causal quantities.")
    elif cmd == "black-box-risk":
        score = args.opaque_steps + args.hidden_parameters + args.missing_diagnostics
        risk = "high" if score >= 4 else "moderate" if score >= 2 else "low"
        emit(cmd, args, {"risk_score": score, "risk": risk}, "Scores black-box risk from opaque steps, hidden parameters, and missing diagnostics.", "Complexity should not substitute for reviewable mechanism and diagnostics.")
    elif cmd == "explanation-warning":
        notes = {
            "formal_precision": "Formal precision does not guarantee explanatory validity.",
            "causal_claim": "Functional dependence does not automatically imply causal explanation.",
            "calibration": "Calibrated parameters are not automatically causal quantities.",
            "black_box": "Black-box transformations require workflow and diagnostic records.",
            "scope": "A model can be valid for one purpose and invalid for another."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document mechanism, evidence, and claim boundaries.")}, "Creates an explanation governance warning.", "Formal structure supports explanation only when mechanism, evidence, and scope are documented.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
