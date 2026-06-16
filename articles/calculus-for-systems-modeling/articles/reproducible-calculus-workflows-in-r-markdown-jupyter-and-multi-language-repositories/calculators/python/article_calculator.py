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

    p = sub.add_parser("artifact-count")
    p.add_argument("--source", type=int, default=2)
    p.add_argument("--generated", type=int, default=4)

    p = sub.add_parser("clean-run-status")
    p.add_argument("--expected", type=int, default=6)
    p.add_argument("--found", type=int, default=6)

    p = sub.add_parser("output-register-score")
    p.add_argument("--documented", type=int, default=6)
    p.add_argument("--total", type=int, default=6)

    p = sub.add_parser("notebook-drift-risk")
    p.add_argument("--executed-out-of-order", default="false")

    p = sub.add_parser("governance-queue-count")
    p.add_argument("--warnings", type=int, default=3)

    p = sub.add_parser("reproducibility-warning")
    p.add_argument("--pattern", default="validity")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "artifact-count":
        total = args.source + args.generated
        emit(cmd, args, {"total_artifacts": total, "source_share": args.source / total if total else 0}, "Counts source and generated workflow artifacts.", "Artifact counts do not prove workflow quality.")
    elif cmd == "clean-run-status":
        passed = args.expected == args.found
        emit(cmd, args, {"passed": passed, "missing": max(args.expected - args.found, 0)}, "Checks whether expected artifacts were found after a clean run.", "A clean run does not prove mathematical validity.")
    elif cmd == "output-register-score":
        score = args.documented / args.total if args.total else 0
        emit(cmd, args, {"documentation_score": score, "complete": score >= 1.0}, "Scores output-register completeness.", "Documented outputs should remain traceable to source scripts.")
    elif cmd == "notebook-drift-risk":
        drift = str(args.executed_out_of_order).lower() in {"true", "1", "yes"}
        emit(cmd, args, {"drift_risk": "high" if drift else "lower", "clean_rerun_needed": True}, "Flags notebook drift risk.", "Notebook outputs should match a clean rerun.")
    elif cmd == "governance-queue-count":
        emit(cmd, args, {"warnings": args.warnings, "review_required": args.warnings > 0}, "Counts warnings in a governance queue.", "Governance queues support review but do not replace judgment.")
    elif cmd == "reproducibility-warning":
        notes = {
            "validity": "Reproducibility does not prove model validity.",
            "notebook": "Notebook state can drift without clean-run checks.",
            "outputs": "Generated outputs should be traceable to source code.",
            "parameters": "Parameter records do not prove empirical correctness.",
            "governance": "Governance queues support review but do not replace judgment."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document reproducibility limits and interpretation boundaries.")}, "Creates a reproducibility interpretation warning.", "Reproducibility is a foundation for review, not a substitute for review.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
