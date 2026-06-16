#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
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

def explicit_amp(h: float, eigenvalue: float) -> float:
    return abs(1 + h * eigenvalue)

def implicit_amp(h: float, eigenvalue: float) -> float:
    return abs(1 / (1 - h * eigenvalue))

def parse_eigenvalues(text: str) -> list[float]:
    return [float(x.strip()) for x in text.split(",") if x.strip()]

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("explicit-amplification")
    p.add_argument("--step-size", type=float, default=0.1)
    p.add_argument("--eigenvalue", type=float, default=-50.0)

    p = sub.add_parser("implicit-amplification")
    p.add_argument("--step-size", type=float, default=0.1)
    p.add_argument("--eigenvalue", type=float, default=-50.0)

    p = sub.add_parser("stiffness-ratio")
    p.add_argument("--eigenvalues", default="-1,-50")

    p = sub.add_parser("stable-explicit-step-bound")
    p.add_argument("--eigenvalue", type=float, default=-50.0)

    p = sub.add_parser("method-comparison")
    p.add_argument("--step-size", type=float, default=0.1)
    p.add_argument("--eigenvalue", type=float, default=-50.0)

    p = sub.add_parser("stiffness-warning-note")
    p.add_argument("--symptom", default="step_rejection")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "explicit-amplification":
        amp = explicit_amp(args.step_size, args.eigenvalue)
        emit(cmd, args, {"amplification_factor": amp, "status": "stable_for_test_problem" if amp <= 1 else "unstable_for_test_problem"}, "Computes explicit Euler stability factor for a linear test problem.", "Explicit instability may be numerical artifact rather than real system instability.")
    elif cmd == "implicit-amplification":
        amp = implicit_amp(args.step_size, args.eigenvalue)
        emit(cmd, args, {"amplification_factor": amp, "status": "stable_for_test_problem" if amp <= 1 else "unstable_for_test_problem"}, "Computes implicit Euler stability factor for a linear test problem.", "Implicit stability does not remove accuracy or interpretation review.")
    elif cmd == "stiffness-ratio":
        vals = parse_eigenvalues(args.eigenvalues)
        mags = [abs(v) for v in vals if abs(v) > 0]
        ratio = max(mags) / min(mags)
        emit(cmd, args, {"stiffness_ratio": ratio, "eigenvalues_count": len(vals)}, "Computes a simple eigenvalue magnitude ratio.", "A stiffness ratio is a heuristic diagnostic, not a complete stiffness proof.")
    elif cmd == "stable-explicit-step-bound":
        if args.eigenvalue >= 0:
            raise ValueError("This simple bound expects a negative eigenvalue")
        bound = 2 / abs(args.eigenvalue)
        emit(cmd, args, {"maximum_stable_step_for_explicit_euler_test": bound}, "Computes the simple explicit Euler stability bound for y'=lambda y with negative lambda.", "Accuracy may require an even smaller step.")
    elif cmd == "method-comparison":
        eamp = explicit_amp(args.step_size, args.eigenvalue)
        iamp = implicit_amp(args.step_size, args.eigenvalue)
        emit(cmd, args, {"explicit_amplification": eamp, "implicit_amplification": iamp, "explicit_status": "stable_for_test_problem" if eamp <= 1 else "unstable_for_test_problem", "implicit_status": "stable_for_test_problem" if iamp <= 1 else "unstable_for_test_problem"}, "Compares explicit and implicit stability factors.", "Method comparison is a diagnostic, not empirical validation.")
    elif cmd == "stiffness-warning-note":
        notes = {
            "step_rejection": "Repeated rejected steps can indicate stiffness, discontinuity, or poor scaling.",
            "tiny_steps": "Very small accepted steps can indicate fast internal dynamics or tight tolerances.",
            "solver_failure": "Solver failure can indicate stiffness, bad scaling, discontinuity, or implementation error.",
            "method_disagreement": "Solver disagreement should trigger method comparison, tolerance review, and benchmark checks."
        }
        emit(cmd, args, {"symptom": args.symptom, "note": notes.get(args.symptom, "Document the symptom and review solver diagnostics.")}, "Creates a stiffness warning interpretation note.", "Warnings should be preserved, not suppressed.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
