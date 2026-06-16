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

    p = sub.add_parser("smoothness-risk")
    p.add_argument("--breaks", type=int, default=1)
    p.add_argument("--thresholds", type=int, default=1)
    p.add_argument("--heterogeneity", type=int, default=1)
    p.add_argument("--solver-warnings", type=int, default=0)

    p = sub.add_parser("threshold-warning")
    p.add_argument("--value", type=float, default=0.92)
    p.add_argument("--critical", type=float, default=1.0)
    p.add_argument("--margin", type=float, default=0.1)

    p = sub.add_parser("equilibrium-bias")
    p.add_argument("--has-equilibrium", type=int, default=1)
    p.add_argument("--path-analyzed", type=int, default=0)
    p.add_argument("--stability-tested", type=int, default=0)

    p = sub.add_parser("aggregation-risk")
    p.add_argument("--mean", type=float, default=50.0)
    p.add_argument("--maximum", type=float, default=95.0)
    p.add_argument("--threshold", type=float, default=80.0)

    p = sub.add_parser("solver-risk")
    p.add_argument("--step-check", type=int, default=0)
    p.add_argument("--convergence-flag", type=int, default=1)
    p.add_argument("--stiffness-warning", type=int, default=1)

    p = sub.add_parser("continuous-model-warning")
    p.add_argument("--pattern", default="false_smoothness")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "smoothness-risk":
        score = args.breaks + args.thresholds + args.heterogeneity + args.solver_warnings
        emit(cmd, args, {"risk_score": score, "risk": risk_label(score)}, "Scores whether smooth continuity assumptions may hide breaks, thresholds, heterogeneity, or solver warnings.", "Smooth mathematical output does not prove smooth system behavior.")
    elif cmd == "threshold-warning":
        distance = abs(args.critical - args.value)
        near = distance <= args.margin
        emit(cmd, args, {"distance_to_critical": distance, "near_threshold": near}, "Checks whether a value is near a critical threshold.", "A model without threshold review may understate fragility.")
    elif cmd == "equilibrium-bias":
        risk_score = args.has_equilibrium + (1 - args.path_analyzed) + (1 - args.stability_tested)
        emit(cmd, args, {"risk_score": risk_score, "risk": risk_label(risk_score)}, "Flags when equilibrium is emphasized without path or stability review.", "An equilibrium is a mathematical condition, not a complete interpretation.")
    elif cmd == "aggregation-risk":
        exceeds = args.maximum >= args.threshold and args.mean < args.threshold
        gap = args.maximum - args.mean
        emit(cmd, args, {"max_mean_gap": gap, "hidden_threshold_exceedance": exceeds}, "Checks whether an average hides threshold exceedance in a subgroup or location.", "An average can hide local stress, inequality, or bottlenecks.")
    elif cmd == "solver-risk":
        risk_score = (1 - args.step_check) + (1 - args.convergence_flag) + args.stiffness_warning
        emit(cmd, args, {"risk_score": risk_score, "risk": risk_label(risk_score)}, "Checks whether solver diagnostics are sufficient for continuous model interpretation.", "A successful solver run does not prove model validity.")
    elif cmd == "continuous-model-warning":
        notes = {
            "false_smoothness": "Smooth mathematical output does not prove smooth system behavior.",
            "threshold": "A model without threshold review may understate fragility.",
            "equilibrium": "An equilibrium is a mathematical condition, not a complete interpretation.",
            "aggregation": "An average can hide local stress, inequality, or bottlenecks.",
            "solver": "A successful solver run does not prove model validity.",
            "domain": "Continuous model claims must be tied to scope, evidence, and diagnostics."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document continuity assumptions and claim boundaries.")}, "Creates a continuous-model risk warning.", "Continuous models are approximations whose assumptions and diagnostics must be reviewed.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
