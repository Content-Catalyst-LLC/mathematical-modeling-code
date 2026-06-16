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

def parse_numbers(text: str) -> list[float]:
    return [float(item.strip()) for item in text.split(",") if item.strip()]

def logistic(t: float, x0: float, r: float, k: float) -> float:
    return k / (1 + ((k - x0) / x0) * math.exp(-r * t))

def data_points():
    return [(0.0, 10.0), (2.0, 17.5), (4.0, 29.2), (6.0, 44.1), (8.0, 60.5), (10.0, 74.0), (12.0, 83.2)]

def candidate_loss(r: float, k: float):
    residuals = []
    for t, observed in data_points():
        predicted = logistic(t, 10.0, r, k)
        residuals.append(observed - predicted)
    loss = sum(x * x for x in residuals)
    abs_values = [abs(x) for x in residuals]
    return loss, sum(abs_values) / len(abs_values), max(abs_values)

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("residual")
    p.add_argument("--observed", type=float, required=True)
    p.add_argument("--predicted", type=float, required=True)

    p = sub.add_parser("squared-loss")
    p.add_argument("--residuals", default="1.0,-0.5,0.25")

    p = sub.add_parser("logistic-prediction")
    p.add_argument("--time", type=float, default=8.0)
    p.add_argument("--growth-rate", type=float, default=0.34)
    p.add_argument("--carrying-capacity", type=float, default=105.0)
    p.add_argument("--initial-value", type=float, default=10.0)

    p = sub.add_parser("candidate-loss")
    p.add_argument("--growth-rate", type=float, default=0.34)
    p.add_argument("--carrying-capacity", type=float, default=105.0)

    sub.add_parser("grid-search")

    p = sub.add_parser("calibration-warning")
    p.add_argument("--pattern", default="validation")

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "residual":
        res = args.observed - args.predicted
        emit(cmd, args, {"residual": res, "squared_residual": res * res}, "Computes an observed-minus-predicted residual.", "Residuals should be inspected as a pattern, not only summarized.")
    elif cmd == "squared-loss":
        residuals = parse_numbers(args.residuals)
        loss = sum(x * x for x in residuals)
        emit(cmd, args, {"loss": loss, "residual_count": len(residuals)}, "Computes sum of squared residuals.", "Loss-function choice affects calibration interpretation.")
    elif cmd == "logistic-prediction":
        pred = logistic(args.time, args.initial_value, args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"predicted_value": pred}, "Computes a logistic-model prediction for one parameter set.", "Prediction from calibrated parameters is not validation.")
    elif cmd == "candidate-loss":
        loss, mar, mx = candidate_loss(args.growth_rate, args.carrying_capacity)
        emit(cmd, args, {"loss": loss, "mean_absolute_residual": mar, "max_absolute_residual": mx}, "Computes candidate calibration loss against synthetic teaching data.", "Candidate loss does not prove model validity.")
    elif cmd == "grid-search":
        rows = []
        for r in [0.22, 0.26, 0.30, 0.34, 0.38, 0.42]:
            for k in [85.0, 95.0, 105.0, 115.0, 125.0]:
                loss, mar, mx = candidate_loss(r, k)
                rows.append({"growth_rate": r, "carrying_capacity": k, "loss": loss, "mean_absolute_residual": mar, "max_absolute_residual": mx})
        rows.sort(key=lambda row: row["loss"])
        write_series("grid_search", rows)
        emit(cmd, args, {"records": len(rows), "best_growth_rate": rows[0]["growth_rate"], "best_carrying_capacity": rows[0]["carrying_capacity"], "best_loss": rows[0]["loss"]}, "Runs a simple calibration grid search.", "Grid search depends on tested bounds and resolution.")
    elif cmd == "calibration-warning":
        notes = {
            "validation": "Calibration is not validation; held-out or independent evidence is still required.",
            "identifiability": "A best-fit value may be poorly identifiable if many values fit similarly.",
            "overfitting": "Excellent calibration fit can reflect noise rather than generalizable structure.",
            "bounds": "Parameter bounds can drive results and should be documented."
        }
        emit(cmd, args, {"pattern": args.pattern, "note": notes.get(args.pattern, "Document the calibration limitation and narrow the claim.")}, "Creates a calibration interpretation warning.", "Calibration should improve transparency, not hide uncertainty.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
