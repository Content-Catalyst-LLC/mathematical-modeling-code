#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable


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
    flat = {
        "calculator": payload.calculator,
        "interpretation": payload.interpretation,
        "warning": payload.warning,
        **{f"input_{k}": v for k, v in payload.inputs.items()},
        **{f"result_{k}": v for k, v in payload.result.items()},
    }
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)


def default_function(x: float) -> float:
    return x * x


def rate_equation(rate: float) -> Callable[[float, float], float]:
    return lambda _t, x: rate * x


def taylor_exp(x: float, order: int) -> float:
    return sum((x ** n) / math.factorial(n) for n in range(order + 1))


def calc_absolute_error(args: argparse.Namespace) -> CalculatorResult:
    error = args.true_value - args.approximation
    abs_error = abs(error)
    payload = CalculatorResult(
        "approximation-error",
        {"true_value": args.true_value, "approximation": args.approximation},
        {"signed_error": error, "absolute_error": abs_error},
        "Absolute error measures the size of the difference between reference and approximation.",
    )
    write_outputs("approximation_error", payload)
    return payload


def calc_relative_error(args: argparse.Namespace) -> CalculatorResult:
    abs_error = abs(args.true_value - args.approximation)
    if args.true_value == 0:
        rel_error = None
        warning = "Relative error is undefined when the true value is zero."
    else:
        rel_error = abs_error / abs(args.true_value)
        warning = ""
    payload = CalculatorResult(
        "relative-error",
        {"true_value": args.true_value, "approximation": args.approximation},
        {"absolute_error": abs_error, "relative_error": rel_error, "percent_error": None if rel_error is None else 100 * rel_error},
        "Relative error scales approximation error by the reference value.",
        warning,
    )
    write_outputs("relative_error", payload)
    return payload


def calc_taylor_exp(args: argparse.Namespace) -> CalculatorResult:
    partial = taylor_exp(args.x, args.order)
    reference = math.exp(args.x)
    abs_error = abs(reference - partial)
    rel_error = abs_error / abs(reference)
    payload = CalculatorResult(
        "taylor-exp",
        {"x": args.x, "order": args.order},
        {"approximation": partial, "reference_value": reference, "absolute_error": abs_error, "relative_error": rel_error},
        "Taylor truncation error should be interpreted with respect to order and distance from the center.",
        "" if abs(args.x) <= 2 else "Evaluation is far from the expansion center; review local validity.",
    )
    write_outputs("taylor_exp", payload)
    return payload


def calc_truncation_sweep(args: argparse.Namespace) -> CalculatorResult:
    rows = []
    reference = math.exp(args.x)
    for order in range(args.max_order + 1):
        approx = taylor_exp(args.x, order)
        abs_error = abs(reference - approx)
        rows.append({"order": order, "approximation": approx, "absolute_error": abs_error, "relative_error": abs_error / abs(reference)})
    ensure_output_dir()
    with (OUTPUT_DIR / "truncation_sweep.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["order", "approximation", "absolute_error", "relative_error"])
        writer.writeheader()
        writer.writerows(rows)
    payload = CalculatorResult(
        "truncation-sweep",
        {"x": args.x, "max_order": args.max_order, "function": "exp(x)"},
        {"rows_written": len(rows), "final_approximation": rows[-1]["approximation"], "final_absolute_error": rows[-1]["absolute_error"], "final_relative_error": rows[-1]["relative_error"]},
        "A truncation sweep shows how retained order changes approximation error.",
    )
    write_outputs("truncation_sweep_summary", payload)
    return payload


def calc_derivative_step(args: argparse.Namespace) -> CalculatorResult:
    derivative = (default_function(args.x + args.h) - default_function(args.x - args.h)) / (2 * args.h)
    reference = 2 * args.x
    payload = CalculatorResult(
        "derivative-step",
        {"x": args.x, "h": args.h, "function": "x^2"},
        {"central_difference": derivative, "reference_value": reference, "absolute_error": abs(reference - derivative)},
        "Central finite differences approximate local rate of change; step size affects error.",
    )
    write_outputs("derivative_step", payload)
    return payload


def calc_integral_step(args: argparse.Namespace) -> CalculatorResult:
    h = (args.b - args.a) / args.steps
    total = 0.5 * (default_function(args.a) + default_function(args.b))
    for i in range(1, args.steps):
        total += default_function(args.a + i * h)
    integral = total * h
    reference = (args.b**3 - args.a**3) / 3.0
    payload = CalculatorResult(
        "integral-step",
        {"a": args.a, "b": args.b, "steps": args.steps, "function": "x^2"},
        {"trapezoid_integral": integral, "reference_value": reference, "absolute_error": abs(reference - integral)},
        "The trapezoid rule approximates accumulated change; grid size affects error.",
    )
    write_outputs("integral_step", payload)
    return payload


def ode_steps(method: str, x0: float, rate: float, dt: float, steps: int) -> list[dict]:
    f = rate_equation(rate)
    t = 0.0
    x = x0
    rows = [{"step": 0, "t": t, "x": x}]
    for step in range(1, steps + 1):
        if method == "euler":
            x = x + dt * f(t, x)
        elif method == "rk4":
            k1 = f(t, x)
            k2 = f(t + dt / 2, x + dt * k1 / 2)
            k3 = f(t + dt / 2, x + dt * k2 / 2)
            k4 = f(t + dt, x + dt * k3)
            x = x + dt * (k1 + 2*k2 + 2*k3 + k4) / 6
        else:
            raise ValueError(method)
        t += dt
        rows.append({"step": step, "t": t, "x": x})
    return rows


def calc_ode(args: argparse.Namespace, method: str) -> CalculatorResult:
    rows = ode_steps(method, args.x0, args.rate, args.dt, args.steps)
    exact = args.x0 * math.exp(args.rate * args.dt * args.steps)
    payload = CalculatorResult(
        method,
        {"x0": args.x0, "rate": args.rate, "dt": args.dt, "steps": args.steps, "equation": "dx/dt = rate*x"},
        {"final_x": rows[-1]["x"], "reference_value": exact, "absolute_error": abs(exact - rows[-1]["x"]), "rows_written": len(rows)},
        f"{method.upper()} approximates repeated change in a simple exponential growth/decay model.",
    )
    write_outputs(method, payload)
    ensure_output_dir()
    with (OUTPUT_DIR / f"{method}_trajectory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["step", "t", "x"])
        writer.writeheader()
        writer.writerows(rows)
    return payload


def calc_logistic(args: argparse.Namespace) -> CalculatorResult:
    x = args.initial
    rows = [{"step": 0, "x": x}]
    for step in range(1, args.steps + 1):
        x = x + args.rate * x * (1 - x / args.carrying_capacity)
        rows.append({"step": step, "x": x})
    payload = CalculatorResult(
        "logistic",
        {"initial": args.initial, "carrying_capacity": args.carrying_capacity, "rate": args.rate, "steps": args.steps},
        {"final_x": rows[-1]["x"], "rows_written": len(rows)},
        "The logistic calculator demonstrates bounded growth and stepwise approximation.",
    )
    write_outputs("logistic", payload)
    ensure_output_dir()
    with (OUTPUT_DIR / "logistic_trajectory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["step", "x"])
        writer.writeheader()
        writer.writerows(rows)
    return payload


def calc_finite_diff(args: argparse.Namespace) -> CalculatorResult:
    values = [float(v.strip()) for v in args.values.split(",") if v.strip()]
    diffs = [values[i+1] - values[i] for i in range(len(values)-1)]
    payload = CalculatorResult("finite-diff", {"values": values}, {"differences": diffs, "count": len(diffs)}, "Finite differences approximate discrete change between adjacent observations.")
    write_outputs("finite_diff", payload)
    return payload


def calc_sensitivity(args: argparse.Namespace) -> CalculatorResult:
    if args.samples < 2:
        raise ValueError("samples must be at least 2")
    step = (args.parameter_max - args.parameter_min) / (args.samples - 1)
    rows = []
    for i in range(args.samples):
        p = args.parameter_min + i * step
        response = p / (1 + p)
        rows.append({"sample": i + 1, "parameter": p, "response": response})
    payload = CalculatorResult("sensitivity", {"parameter_min": args.parameter_min, "parameter_max": args.parameter_max, "samples": args.samples}, {"min_response": rows[0]["response"], "max_response": rows[-1]["response"], "rows_written": len(rows)}, "Sensitivity sweeps show how model response changes across a parameter range.")
    write_outputs("sensitivity", payload)
    ensure_output_dir()
    with (OUTPUT_DIR / "sensitivity_sweep.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sample", "parameter", "response"])
        writer.writeheader()
        writer.writerows(rows)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Article calculator layer for approximation error, truncation, and local validity.")
    sub = parser.add_subparsers(dest="command", required=True)

    ae = sub.add_parser("approximation-error")
    ae.add_argument("--true-value", type=float, required=True)
    ae.add_argument("--approximation", type=float, required=True)

    re = sub.add_parser("relative-error")
    re.add_argument("--true-value", type=float, required=True)
    re.add_argument("--approximation", type=float, required=True)

    te = sub.add_parser("taylor-exp")
    te.add_argument("--x", type=float, default=1.0)
    te.add_argument("--order", type=int, default=10)

    ts = sub.add_parser("truncation-sweep")
    ts.add_argument("--x", type=float, default=1.0)
    ts.add_argument("--max-order", type=int, default=12)

    d = sub.add_parser("derivative-step")
    d.add_argument("--x", type=float, default=2.0)
    d.add_argument("--h", type=float, default=1e-2)

    integ = sub.add_parser("integral-step")
    integ.add_argument("--a", type=float, default=0.0)
    integ.add_argument("--b", type=float, default=1.0)
    integ.add_argument("--steps", type=int, default=100)

    for name in ("euler", "rk4"):
        ode = sub.add_parser(name)
        ode.add_argument("--x0", type=float, default=1.0)
        ode.add_argument("--rate", type=float, default=0.5)
        ode.add_argument("--dt", type=float, default=0.1)
        ode.add_argument("--steps", type=int, default=10)

    logi = sub.add_parser("logistic")
    logi.add_argument("--initial", type=float, default=10.0)
    logi.add_argument("--carrying-capacity", type=float, default=100.0)
    logi.add_argument("--rate", type=float, default=0.25)
    logi.add_argument("--steps", type=int, default=20)

    fd = sub.add_parser("finite-diff")
    fd.add_argument("--values", type=str, default="1,2,4,7,11")

    sens = sub.add_parser("sensitivity")
    sens.add_argument("--parameter-min", type=float, default=0.1)
    sens.add_argument("--parameter-max", type=float, default=1.0)
    sens.add_argument("--samples", type=int, default=10)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "approximation-error":
        payload = calc_absolute_error(args)
    elif args.command == "relative-error":
        payload = calc_relative_error(args)
    elif args.command == "taylor-exp":
        payload = calc_taylor_exp(args)
    elif args.command == "truncation-sweep":
        payload = calc_truncation_sweep(args)
    elif args.command == "derivative-step":
        payload = calc_derivative_step(args)
    elif args.command == "integral-step":
        payload = calc_integral_step(args)
    elif args.command == "euler":
        payload = calc_ode(args, "euler")
    elif args.command == "rk4":
        payload = calc_ode(args, "rk4")
    elif args.command == "logistic":
        payload = calc_logistic(args)
    elif args.command == "finite-diff":
        payload = calc_finite_diff(args)
    elif args.command == "sensitivity":
        payload = calc_sensitivity(args)
    else:
        raise ValueError(args.command)

    print(json.dumps(asdict(payload), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
