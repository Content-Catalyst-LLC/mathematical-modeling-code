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

def equilibrium_value(input_rate: float, loss_rate: float) -> float:
    return input_rate / loss_rate

def linear_rate(state: float, input_rate: float, loss_rate: float) -> float:
    return input_rate - loss_rate * state

def analytical_solution(time: float, initial: float, input_rate: float, loss_rate: float) -> float:
    eq = equilibrium_value(input_rate, loss_rate)
    return eq + (initial - eq) * math.exp(-loss_rate * time)

def euler_step(state: float, input_rate: float, loss_rate: float, dt: float) -> float:
    return state + dt * linear_rate(state, input_rate, loss_rate)

def euler_series(initial: float, input_rate: float, loss_rate: float, dt: float, steps: int) -> list[dict]:
    y = initial
    rows = []
    for n in range(steps + 1):
        t = n * dt
        analytical = analytical_solution(t, initial, input_rate, loss_rate)
        rows.append({"step": n, "time": t, "analytical_state": analytical, "euler_state": y, "absolute_error": abs(analytical - y), "rate": linear_rate(y, input_rate, loss_rate)})
        y = euler_step(y, input_rate, loss_rate, dt)
    return rows

def write_series(name: str, rows: list[dict]) -> None:
    ensure_output_dir()
    (OUTPUT_DIR / f"{name}_series.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    with (OUTPUT_DIR / f"{name}_series.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def emit(command: str, args, result: dict, interpretation: str, warning: str = ""):
    payload = CalculatorResult(command, vars(args), result, interpretation, warning)
    write_outputs(command.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("linear-rate")
    p.add_argument("--state", type=float, default=20.0)
    p.add_argument("--input-rate", type=float, default=12.0)
    p.add_argument("--loss-rate", type=float, default=0.4)

    p = sub.add_parser("equilibrium")
    p.add_argument("--input-rate", type=float, default=12.0)
    p.add_argument("--loss-rate", type=float, default=0.4)

    p = sub.add_parser("analytical-solution")
    p.add_argument("--time", type=float, default=2.0)
    p.add_argument("--initial", type=float, default=20.0)
    p.add_argument("--input-rate", type=float, default=12.0)
    p.add_argument("--loss-rate", type=float, default=0.4)

    p = sub.add_parser("euler-step")
    p.add_argument("--state", type=float, default=20.0)
    p.add_argument("--input-rate", type=float, default=12.0)
    p.add_argument("--loss-rate", type=float, default=0.4)
    p.add_argument("--dt", type=float, default=0.1)

    p = sub.add_parser("compare-euler")
    p.add_argument("--initial", type=float, default=20.0)
    p.add_argument("--input-rate", type=float, default=12.0)
    p.add_argument("--loss-rate", type=float, default=0.4)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=20)

    return parser

def main():
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "linear-rate":
        rate = linear_rate(args.state, args.input_rate, args.loss_rate)
        emit(cmd, args, {"rate": rate}, "Computes dy/dt = input - loss*y.", "Assumes proportional loss and additive input.")
    elif cmd == "equilibrium":
        eq = equilibrium_value(args.input_rate, args.loss_rate)
        emit(cmd, args, {"equilibrium": eq}, "Computes the balance point input/loss.", "Equilibrium is conditional on constant input and loss.")
    elif cmd == "analytical-solution":
        value = analytical_solution(args.time, args.initial, args.input_rate, args.loss_rate)
        emit(cmd, args, {"state": value}, "Computes y(t)=I/k+(y0-I/k)exp(-kt).", "Assumes constant input and proportional loss.")
    elif cmd == "euler-step":
        next_state = euler_step(args.state, args.input_rate, args.loss_rate, args.dt)
        emit(cmd, args, {"next_state": next_state}, "Computes one explicit Euler update.", "Euler error depends on step size.")
    elif cmd == "compare-euler":
        rows = euler_series(args.initial, args.input_rate, args.loss_rate, args.dt, args.steps)
        write_series("compare_euler_linear_first_order", rows)
        emit(cmd, args, {"final_analytical_state": rows[-1]["analytical_state"], "final_euler_state": rows[-1]["euler_state"], "final_absolute_error": rows[-1]["absolute_error"], "records": len(rows)}, "Compares analytical solution and explicit Euler approximation.", "Check step-size sensitivity before interpretation.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
