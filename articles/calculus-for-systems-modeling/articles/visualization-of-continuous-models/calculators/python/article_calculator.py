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

def write_series(name: str, rows: list[dict]) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def logistic(t: float, x0: float, r: float, k: float) -> float:
    return k / (1.0 + ((k - x0) / x0) * math.exp(-r * t))

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("logistic-point")
    p.add_argument("--time", type=float, default=10.0)
    p.add_argument("--x0", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--carrying-capacity", type=float, default=100.0)

    p = sub.add_parser("trajectory-series")
    p.add_argument("--x0", type=float, default=10.0)
    p.add_argument("--growth-rate", type=float, default=0.35)
    p.add_argument("--carrying-capacity", type=float, default=100.0)

    sub.add_parser("scenario-comparison")

    p = sub.add_parser("figure-audit-record")
    p.add_argument("--visual-type", default="trajectory_plot")

    p = sub.add_parser("visualization-risk-score")
    p.add_argument("--axis-risk", type=int, default=2)
    p.add_argument("--uncertainty-risk", type=int, default=3)
    p.add_argument("--smoothing-risk", type=int, default=1)
    p.add_argument("--metadata-risk", type=int, default=2)

    p = sub.add_parser("uncertainty-band-note")
    p.add_argument("--band-type", default="scenario_range")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "logistic-point":
        value = logistic(args.time, args.x0, args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"value": value}, "Computes one point on a logistic trajectory.", "A plotted point is model-implied, not empirical evidence.")
    elif cmd == "trajectory-series":
        rows = [{"time": step * 0.25, "value": logistic(step * 0.25, args.x0, args.growth_rate, args.carrying_capacity)} for step in range(0, 81)]
        write_series("trajectory_series", rows)
        emit(cmd, args, {"records": len(rows), "final_value": rows[-1]["value"]}, "Generates a trajectory series for visualization.", "Preserve parameters, units, and solver/model assumptions with the figure.")
    elif cmd == "scenario-comparison":
        scenarios = [("low_growth", 0.18), ("baseline", 0.35), ("high_growth", 0.55)]
        rows = [{"scenario": name, "growth_rate": r, "value_at_time_20": logistic(20.0, 10.0, r, 100.0)} for name, r in scenarios]
        write_series("scenario_comparison", rows)
        emit(cmd, args, {"scenarios": len(rows)}, "Compares logistic scenario endpoints.", "Scenario lines are parameter contrasts, not probability intervals.")
    elif cmd == "figure-audit-record":
        emit(cmd, args, {"visual_type": args.visual_type, "required_metadata": "parameters, units, axes, scales, uncertainty, data source, solver settings"}, "Creates a figure audit record.", "A visualization should be reproducible from stored data and metadata.")
    elif cmd == "visualization-risk-score":
        score = args.axis_risk + args.uncertainty_risk + args.smoothing_risk + args.metadata_risk
        level = "high_review_priority" if score >= 8 else "moderate_review_priority" if score >= 4 else "low_review_priority"
        emit(cmd, args, {"risk_score": score, "review_level": level}, "Scores visualization review risk from common distortion channels.", "Risk score is a governance heuristic, not a statistical measure.")
    elif cmd == "uncertainty-band-note":
        notes = {
            "scenario_range": "Band shows selected scenario spread, not probability.",
            "confidence_interval": "Band claims statistical confidence and requires method documentation.",
            "sensitivity_envelope": "Band shows parameter sensitivity over a documented range."
        }
        emit(cmd, args, {"band_type": args.band_type, "note": notes.get(args.band_type, "Define the band before interpretation.")}, "Creates an uncertainty band interpretation note.", "The meaning of the band must be explained.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
